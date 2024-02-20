# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from autograd import make_jvp, jacobian as autograd_jac
import autograd.numpy as np,sys
from noload.optimization.specifications import Spec
from noload.optimization.iterationHandler import Iterations
from noload.optimization.Tools import *
from noload.optimization.ExportToXML import resultsToXML

'''Used to store results'''
class Results:
    """
    objectives  = list : objective values
    eq_cstr = class StructList : equality constraints values
    ineq_cstr = class StructList : inequality constraints values
    """
    objectives  = []  #valeurs des objectifs
    eq_cstr: StructList = None  # valeurs des contraintes d'équalité
    ineq_cstr: StructList = None  # valeurs des contraintes d'inégalités
    def __init__(self, results, shape,x, spec:Spec, jac):
        self.jac = jac # si le résultat est un calcul de jacobien ou non
        results = StructList(results, 'flattened', shape) # les résultats
        # sont sous la forme "aplatie" (fobjectif + contraintes)
        results1 = results.unflatten() # on remet les résultats sous forme
        # "normale" pour pouvoir après les exploiter
        nans_vars=[]
        for vars in spec.oNames: # si il y a des Nans dans les sorties
            try:
                if np.all(np.isnan(results1[spec.oNames.index(vars)])):
                    raise ValueError(vars)
            except ValueError:
                nans_vars.append(vars)
        if nans_vars != []:
            x_denorm = denormalize(x, spec.bounds)
            if len(spec.iNames) == 1 and len(x) != 1:
                nans_inputs = dict(zip(spec.iNames, [x_denorm]))
            elif spec.xinit_sh != [0]*len(spec.iNames) and spec.xinit_sh != []:
                var = StructList(x_denorm, 'flattened', spec.xinit_sh)
                nans_inputs = dict(zip(spec.iNames, var.unflatten()))
            else:
                nans_inputs = dict(zip(spec.iNames,x_denorm))
            print('Warning :', nans_vars, 'is Nan')
            if self.jac:
                print('in Gradient Computation')
            print('with inputs :',nans_inputs)
            sys.exit(0)
        t1 = len(spec.objectives) # nombre de fonctions objectives
        t2 = len(spec.eq_cstr) # nombre de contraintes d'égalité
        t3 = len(spec.ineq_cstr) # nombre de contraintes d'inégalité
        self.objectives = np.array(results1[:t1]) # les t1 premiers éléments
        # de results1 sont les fonctions objectives
        sh = np.shape(self.objectives) # taille des fonctions objectives
        if (t1 == 1) and len(sh) > 1 and sh[0] == 1:
            self.objectives = self.objectives[0]
        if t2 != 0: # s'il y a au moins une contrainte d'égalité
            self.eq_cstr = StructList(results1[t1:t1 + t2]) # les éléments
            # allant de t1 à t1+t2 sont les contraintes d'égalité
            sh = self.eq_cstr.shape # taille des contraintes d'égalité
            if (t2 == 1) and len(sh) > 1 and sh[0] == 1:
                self.eq_cstr.List = self.eq_cstr.List[0]
        if t3 != 0: # s'il y a au moins une contrainte d'inégalité
            self.ineq_cstr = StructList(results1[-t3:]) # les t3 derniers
            # éléments sont les contraintes d'inégalité
            sh = self.ineq_cstr.shape # taille des contraintes d'inégalité
            if (t3 == 1) and len(sh) > 1 and sh[0] == 1:
                self.ineq_cstr.List = self.ineq_cstr.List[0]

        # if t2 != 0:
        #     self.eq_cstr    = self.normalizeEq(results[t1:t1+t2],
        #     spec.eq_cstr_val)
        # if t3 != 0:
        #     self.ineq_cstr  = self.normalizeIneq(results[-t3:],
        #     spec.ineq_cstr_bnd)

    def normalizeEq(self, values, limits):
        """
        Puts the values of equality constraints between the limits
        given in inputs.
        :param values: values wished for the equality constraints
        :param limits: limits wished for the equality constraints
        :return: the values normalized of the equality constraints
        """
        # if limits!=0:
        #     results = (values.T  / limits).T
        # else:
        results = values
        for i in range(len(limits)):
            if limits[i] != 0:
                results[i] = values[i] / limits[i]
        return results
    def normalizeIneq(self, values, bounds):
        """
        Puts the values of inequality constraints between the limits
        given in inputs.
        :param values: values wished for the inequality constraints
        :param limits: limits wished for the inequality constraints
        :return: the values normalized of the inequality constraints
        """

        min = np.array([bnd[0] for bnd in bounds])  #TODO gérer des
        # variables plus complexes comme des vecteurs d'inconnus
        max = np.array([bnd[1] for bnd in bounds])
        # min = bounds[0]
        # max = bounds[1]
        if (self.jac):
            results = values
        else:
            results = ((values.T - min).T).T    #TODO gerer les None
        results = (results.T / (abs(max-min))).T
        return results

class Wrapper:
    """
    model = None : function of the model where we compute the objective
    and constraint functions
    p = dict : constant parameters of the model (optional)
    spec = class Spec : desired performances (objective functions, constraints)
    resultsHandler = list : allows to save the results as they come in
    (optional)
    ParetoList = list : used to display several Pareto Front in a graph
    constraints = list : vector of inequality constraints to be filled at
    each iteration
    xold = list : vector x "old" (not updated) for function evaluations
    xold_g = list : "old" x-vector (not updated) for gradient calculations
    results_val = class Results :values of objectives and constraints
    results_grad = class Results : gradients of objectives and constraints
    rawResults = dict : values of the model outputs
    resultsShape = list : shape of output vector (it "flattens" the results)
    """

    model  = None
    p      = None
    spec : Spec  = None
    resultsHandler = None
    ParetoList = [] # pour afficher plusieurs front de Pareto sur un graphe
    constraints = []
    xold   = None
    xold_g = None
    results_val : Results = None #valeurs des objectifs et contraintes
    results_grad : Results = None #gradients des objectifs et contraintes
    rawResults   = None #valeurs des sorties du model
    resultsShape = None #forme du vecteur de sortie (mise à plat des résultats
    # pour autograd)

    def __init__(self, model : 'function to compute',
                 specifications : Spec ,
                 parameters : 'a List of inputs that are not optimized' = [],
                 resultsHandler : "for real time plotting for instance" = None):
        self.model = model
        self.p = parameters
        self.spec = specifications
        # permet de sauvegarder les résultats au fur et à mesure (optionnel)
        if resultsHandler==True:
            self.resultsHandler = Iterations(self.spec,specifications.iNames,
                                             specifications.oNames,
                                             specifications.freeOutputs)
            self.ParetoList=[]
#        elif resultsHandler != None:
#            self.resultsHandler = resultsHandler
        #else : no resultHandler => no iteration history

        self.init()

    def init(self):
        self.constraints=[]
        if len(self.spec.eq_cstr) != 0:
            self.constraints.append({'type': 'eq',
                 'fun' : self.eq_cstr_val,
                 'jac' : self.eq_cstr_grad})
        if len(self.spec.ineq_cstr) != 0:
            self.constraints.append({'type': 'ineq',
                 'fun' : self.ineq_cstr_val,
                 'jac' : self.ineq_cstr_grad})
        self.xold = None
        self.xold_g = None
        self.results_val = None
        self.results_grad = None
        self.rawResults = None

    ## 3 fonctions pour récupérer les VALEURS des objectifs et contraintes
    def f_val(self, x):
        """
        Gets the value of the objective function evaluated in x according to
        the compute_model method.
        :param x: the vector of optimization variables
        :return: the value of the objective function evaluated in x
        """
        if self.spec.debug:
            x_denorm=denormalize(x,self.spec.bounds)
            if len(self.spec.iNames) == 1 and len(x_denorm) != 1:
                dict_var = dict(zip(self.spec.iNames, [x_denorm]))
            elif self.spec.xinit_sh != [0] * len(self.spec.iNames) and \
                    self.spec.xinit_sh != []:
                var = StructList(x, 'flattened', self.spec.xinit_sh)
                dict_var = dict(zip(self.spec.iNames, var.unflatten()))
            else:
                dict_var = dict(zip(self.spec.iNames,x_denorm))
            print('x=',dict_var)
        if (not np.array_equal(self.xold,x)):
            self.results_val=Results(self.compute_model(x), self.resultsShape,
                                     x,self.spec, jac = False)
            self.xold=np.array(x, copy=True)
        if self.spec.debug:
            print('fobj=',dict(zip(self.spec.objectives,
                                   self.results_val.objectives)))
        if len(self.spec.bounds)>0.: #normalisation de la fonction objective
            self.results_val.objectives[0]=(self.results_val.objectives[0]-
              self.spec.objectives_val[0])/(self.spec.objectives_val[1]-
                                            self.spec.objectives_val[0])
        return self.results_val.objectives

    def eq_cstr_val(self, x):
        """
        Returns the values of the equality constraints of the model evaluated
        in x according to the compute_model method.
        Handles mixed constraints (scalar + vector).
        :param x: the vector of optimization variables
        :return: returns the vector containing the subtraction between the
        equality constraints evaluated in x and the
        desired constraints given in the specifications class
        """
        if (not np.array_equal(self.xold,x)):
            self.results_val = Results(self.compute_model(x), self.resultsShape,
                                       x,self.spec, jac = False)
            self.xold=np.array(x, copy=True)
        #il faut bien se mettre en dehors du if car le calcul du model aura pu
        # être fait dans une autre fonction.
        if self.spec.debug and self.spec.eq_cstr_val.List != []:
            print('eq_cstr=',dict(zip(self.spec.eq_cstr,
                                      self.results_val.eq_cstr.List)))
        if (self.spec.eq_cstr_val.List != []): # s'il y a au moins une
            # contrainte d'égalité
            eq_val_flatten=np.array(self.spec.eq_cstr_val.flatten())
            self.results_val.eq_cstr.List = \
                np.array(self.results_val.eq_cstr.flatten()) -eq_val_flatten #-1
            for i in range(len(self.results_val.eq_cstr.List)):
                if eq_val_flatten[i]!=0.: # normalisation contraintes égalité
                    self.results_val.eq_cstr.List[i]/=eq_val_flatten[i]
            # pour calculer les contraintes d'égalité, on fait la soustraction
            # entre les contraintes calculées et les spécifications désirées
            # qui sont aplaties pour gérer les contraintes complexes (scalaires
            # + vectorielles) -> pour l'algorithme, il faudra que la
            # soustraction soit nulle pour que les contraintes d'égalité soient
            # respectées
        return self.results_val.eq_cstr.List # on renvoie les valeurs
        # des contraintes d'égalité

    def ineq_cstr_val(self, x):
        """
        Returns the values of the different inequality constraints of the model
        evaluated in x according to the compute_model method.
        Handles mixed constraints (scalar + vector).
        :param x: the vector of optimization variables
        :return: returns the vector containing the subtraction between the
        inequality constraints evaluated in x and the
        desired constraints given in the specifications class
        """
        if (not np.array_equal(self.xold,x)):
            res=self.compute_model(x)
            self.results_val = Results(res, self.resultsShape,x, self.spec,
                                       jac = False)
            self.xold=np.array(x, copy=True)
        constraints=self.results_val.ineq_cstr.List
        if (self.spec.ineq_cstr_bnd.List != []):  # s'il y a au moins une
            # contrainte d'inégalité
            constraints = [] # on initialise le vecteur constraints
            for i, cstr in enumerate(self.spec.ineq_cstr_bnd.List): # on fait
                # la liste de toutes les différentes contraintes
                # d'inégalité (scalaires et vectorielles) et de leurs positions
                # dans le vecteur "specifications"
                if isinstance(cstr[0], (int, float)) or cstr[0]==None \
                        or cstr[1]==None: # si la contrainte est scalaire
                    if (cstr[0] != None): # s'il y a une borne inf
                        if cstr[1]==None:
                            constraints.append((self.results_val.ineq_cstr.List
                             [i]-cstr[0])/(1000.-cstr[0]))
                               # borne inf = 0 après normalisation
                        # on ajoute au vecteur constraints la soustraction entre
                        # la valeur de la contrainte d'inégalité obtenue et
                        # la borne inf
                        elif (cstr[1] != None): # s'il y a une borne sup en plus
                            constraints.append((cstr[1]-self.results_val.
                                ineq_cstr.List[i])/(cstr[1]-cstr[0]))
                            # sup = 1 si normalisé
                            # on ajoute au vecteur constraints la soustraction
                            # entre la borne sup et la valeur de la
                            # contrainte d'inégalité obtenue
                    else:  # on suppose que sup est différent de None ! Par
                        # contre il n'y a pas de borne inf
                        constraints.append((cstr[1]-self.results_val.
                            ineq_cstr.List[i])/(cstr[1]+1000.))
                        # sup = 1 si normalisé
                        # on ajoute au vecteur constraints la soustraction
                        # entre la borne sup et la valeur de la
                        # contrainte d'inégalité obtenue
                else: # si la contrainte est vectorielle
                    for j in range(len(cstr)): # on parcourt les différentes
                        # composantes de cette contrainte vectorielle
                        if (cstr[j][0]!= None): # s'il y a une borne inf
                            if cstr[j][1]==None:
                                constraints.append((self.results_val.ineq_cstr.
                                   List[i][j]-cstr[j][0])/(1000.-cstr[j][0])
                                )  # borne inf = 0 après normalisation
                            # on ajoute au vecteur constraints la soustraction
                            # entre la valeur de la contrainte d'inégalité
                            # obtenue et la borne inf
                            elif (cstr[j][1] != None):  # s'il y a une borne sup
                                # en plus
                                constraints.append((cstr[j][1]-self.results_val.
                                  ineq_cstr.List[i][j])/(cstr[j][1]-cstr[j][0]))
                                # sup = 1 si normalisé
                                # on ajoute au vecteur constraints la
                                # soustraction entre la borne sup et la
                                # valeur de la contrainte d'inégalité obtenue
                        else:  # on suppose que sup est différent de None !
                            # Par contre il n'y a pas de borne inf
                            constraints.append((cstr[j][1]-self.results_val.
                                ineq_cstr.List[i][j])/(cstr[j][1]+1000.))
                            # sup = 1 si normalisé
                            # on ajoute au vecteur constraints la soustraction
                            # entre la borne sup et la valeur de la
                            # contrainte d'inégalité obtenue
        if self.spec.debug and self.spec.ineq_cstr_bnd.List !=[]:
            print('ineq_cstr=',dict(zip(self.spec.ineq_cstr,
                                        self.results_val.ineq_cstr.List)))
        return np.array(constraints) # on renvoie les valeurs des contraintes
        # d'inégalité

    ## 3 fonctions pour récupérer les GRADIENTS des objectifs et contraintes
    def f_grad(self, x):
        """
        Returns the gradient of the objective function evaluated in x according
        to the Jacobian of the compute_model method. (reverse mode)
        :param x: the vector of optimization variables
        :return: the gradient of the objective function evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)):
            grad = autograd_jac(self.compute_model)(x)
            self.results_grad = Results(grad, self.resultsShape, x,self.spec,
                                        jac = True)
            self.xold_g=np.array(x, copy=True)
        if self.spec.debug:
            print('fobj_grad=',dict(zip(self.spec.objectives,
                                        [self.results_grad.objectives])))
        if len(self.spec.bounds)>0.: # normalisation gradients objectifs
            for i in range(len(self.results_grad.objectives)):
                self.results_grad.objectives[i]=self.results_grad.objectives[i]/\
                    (self.spec.objectives_val[1]-self.spec.objectives_val[0])
        return self.results_grad.objectives
    # Autre methode de calcul du Jacobien, à utiliser si il la dimension en
    # sortie est plus grande qu'en entrée
    def f_grad_using_make_jvp(self, x):
        """
        Returns the gradient of the objective function evaluated in x according
        to the Jacobian of the compute_model method. (forward mode)
        :param x: the vector of optimization variables
        :return: the gradient of the objective function evaluated in x
        """
        if (not np.array_equal(self.xold_g, x)):
            a = np.array([1])
            basis = np.pad(a, [(0, len(x) - 1)], mode='constant')  # create
            # first vector basis (1, 0, 0, ...)
            val_of_f, jac = (make_jvp(self.compute_model)(x))(basis)
            lines=len(jac)
            for i in range(1, len(x)):
                basis = np.roll(basis, 1)
                val_of_f, col_of_jacobian = \
                    (make_jvp(self.compute_model)(x))(basis)
                jac=np.append(jac, col_of_jacobian, axis = 0)
            jac =np.reshape(jac,(len(x),lines)).T
            self.results_grad = Results(jac, self.resultsShape, self.spec,
                                        jac = True)
            self.xold_g=np.array(x, copy=True)
        return self.results_grad.objectives

    def eq_cstr_grad(self, x):
        """
        Returns the gradient of the different equality constraints of the model
        evaluated in x according to the Jacobian of the compute_model method.
        Handles mixed constraints (scalar + vector).
        :param x: the vector of optimization variables
        :return: the vector of gradient equality constraints evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)):
            self.results_grad = Results(autograd_jac(self.compute_model)(x),
                                    self.resultsShape, x,self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        res=self.results_grad.eq_cstr.List
        if (self.spec.eq_cstr_val.List != []):
            res = [] # on va aplatir les gradients des contraintes complexes
        # (scalaires + vectorielles)
            for i in range(len(self.results_grad.eq_cstr.List)): # on parcourt
            # le résultat obtenu (gradient de contraintes d'égalité)
                if isinstance(self.spec.eq_cstr_val.List[i],(int,float)):# si la
                # contrainte est scalaire
                    res.append(self.results_grad.eq_cstr.List[i]) # on ajoute
                # simplement son gradient dans la nouvelle liste res
                elif isinstance(self.spec.eq_cstr_val.List[i], list): # si la
                # contrainte est vectorielle
                    for j in range(len(self.results_grad.eq_cstr.List[i])): # on
                    # parcourt chaque élément de son gradient
                        res.append(self.results_grad.eq_cstr.List[i][j])# on les
                    # ajoute un par un à la liste res

            res=np.array(res) # normalisation gradients contraintes inégalité
            eq_val_flatten=np.array(self.spec.eq_cstr_val.flatten())
            if np.shape(res)==(1,):
                res=np.array([res])
            for k in range(len(res)):
                if eq_val_flatten[k]!=0.:
                    res[k,:]=res[k,:]/eq_val_flatten[k]
        if self.spec.debug and self.spec.eq_cstr_val.List != []:
            print('eq_cstr_grad=',dict(zip(self.spec.eq_cstr,
                                           self.results_grad.eq_cstr.List)))
        return res # on renvoie les gradients des contraintes d'égalité

    def ineq_cstr_grad(self, x):
        """
        Returns the gradient of the different inequality constraints of the
        model evaluated in x according to the Jacobian of the compute_model
        method.
        Handles mixed constraints (scalar + vector).
        :param x: the vector of optimization variables
        :return:  the vector of gradient inequality constraints evaluated in x
        """
        if (not np.array_equal(self.xold_g,x)):
            self.results_grad = Results(autograd_jac(self.compute_model)(x),
                                    self.resultsShape, self.spec, jac = True)
            self.xold_g=np.array(x, copy=True)
        # on duplique les contraintes d'inégalité qui on une borne supérieure:
        res=self.results_grad.ineq_cstr.List
        if (self.spec.ineq_cstr_bnd.List != []): # s'il y a au moins une
            # contrainte d'inégalité
            res = [] # on initialise le vecteur res (gradients des contraintes
            # d'inégalité)
            for i, cstr in enumerate(self.spec.ineq_cstr_bnd.List): # on fait
                # la liste de toutes les différentes contraintes
                # d'inégalité (scalaires et vectorielles) et de leurs positions
                # dans le vecteur "specifications"
                if isinstance(cstr[0], (int, float)) or cstr[0]==None: # si la
                    # contrainte est scalaire
                    if (cstr[0] != None): # s'il y a une borne inf
                        if cstr[1]==None:
                            res.append(self.results_grad.ineq_cstr.List[i]/
                                (1000.-cstr[0]))# on ajoute le résultat tel quel
                        elif (cstr[1] != None): # s'il y a une borne sup en plus
                            res.append(-self.results_grad.ineq_cstr.List[i]/
                                        (cstr[1]-cstr[0]))
                            # on ajoute l'opposé du résultat car par défaut
                            # SLSQP : ctr>0
                    else:  # on suppose que sup est différent de None ! Par
                        # contre il n'y a pas de borne inf
                        res.append(- self.results_grad.ineq_cstr.List[i]/
                                   (cstr[1]+1000.))
                else: # si la contrainte est vectorielle
                    for j in range(len(cstr)):  # on parcourt les différentes
                        # composantes de cette contrainte vectorielle
                        if (cstr[j][0] != None):  # s'il y a une borne inf
                            if cstr[j][1]==None:
                                res.append(np.array(
                                  self.results_grad.ineq_cstr.List[i][j])/
                                  (1000.-cstr[j][0]))
                                # on ajoute le résultat tel quel
                            elif (cstr[j][1] != None): # s'il y a une borne sup
                                # en plus
                                res.append(-np.array(
                                    self.results_grad.ineq_cstr.List[i][j])/
                                           (cstr[j][1]-cstr[j][0]))
                                # on ajoute l'opposé du résultat car par défaut
                                # SLSQP : ctr>0
                        else:   # on suppose que sup est différent de None !
                            # Par contre il n'y a pas de borne inf
                            res.append(-np.array(
                                self.results_grad.ineq_cstr.List[i][j])/
                                       (cstr[j][1]+1000.))
        if self.spec.debug and self.spec.ineq_cstr_bnd.List!=[]:
            print('ineq_cstr_grad=',dict(zip(self.spec.ineq_cstr,
                                             self.results_grad.ineq_cstr.List)))
        return res # on renvoie les gradients des contraintes d'inégalité

    # fonction utilisée par minimize de scipy
    def f_val_grad(self, x):
        """
        Function used by scipy minimize.
        :param x: the vector of optimization variables
        :return: a tuple including the evaluation of the objective function
        evaluated in x and its gradient
        """
        return (self.f_val(x), self.f_grad(x))

    # wrapper permettant d'être selectif sur les sorties du modèles,
    # en particulier pour le calcul du Jacobien
    def compute_model(self, x):
        """
        Computes the model outputs (objective function + constraints) in x. 
        Stores the results (optimization variables + model outputs) got at
        each iteration.
        :param x: the vector of optimization variables
        :return: returns a "flattened" vector out including the model outputs
        """
        if len(self.spec.bounds)>0.:
            x = denormalize(x, self.spec.bounds)
        if len(self.spec.iNames)==1 and len(x)!=1:   #TODO, patch for 1 array
            # variable, to do more general
            xList = dict(zip(self.spec.iNames, [x]))
        elif self.spec.xinit_sh != [0] * len(self.spec.iNames) \
                and self.spec.xinit_sh!=[]:
            var = StructList(x, 'flattened', self.spec.xinit_sh)
            xList = dict(zip(self.spec.iNames, var.unflatten()))
        else:
            xList = dict(zip(self.spec.iNames, x))  #TODO, verifier que ça
            # fonctionne pour une liste d'entrée scalaire et vectorielle
            # (uniquement le premier élement du vecteur ?)
        if self.p != []:
            res = self.model(**xList, **self.p)
        else:
            res = self.model(**xList)
        dico = {k: v for k, v in res.__iter__()}  # conversion en dictionnaire
        out=[]
        for vars in self.spec.oNames:
            try:
                if vars not in list(dico.keys()):
                    raise KeyError(vars) #si la variable du cahier des charges
            except KeyError: # n'appartient pas aux sorties du modèle
                print('Warning :',vars,'is not in model')
                pass
            else:
                out.append(dico[vars])
        for i in range(len(out)):
            if (type(out[i]) == np.numpy_boxes.ArrayBox):
                if (type(out[i]._value)==np.ndarray):
                    out[i]=list(out[i])
        if (type(x[0]) != np.numpy_boxes.ArrayBox):
            self.rawResults = dico
            if self.spec.freeOutputs !=[]:
                fData= [dico[vars] for vars in self.spec.freeOutputs]
            else:
                fData=[]
            if (self.resultsHandler!=None):
                if self.spec.xinit_sh != [0] * len(self.spec.iNames):
                    var = StructList(x, 'flattened', self.spec.xinit_sh)
                    self.resultsHandler.updateData(var.unflatten(), out,fData)
                else:
                    self.resultsHandler.updateData(x, out,fData)
        out = StructList(out) # on récupère les sorties du modèle
        self.resultsShape = out.shape
        out2 = out.flatten() # on aplatit les sorties du modèle
        return np.array(out2) # renvoie la sortie sous forme de jax.numpy array

    def f_penalty(self,x):
        """
        Returns a weighted function with the objectives and the constraints
        for stochastic algorithm of Scipy.
        :param x: the vector of optimization variables
        :return: the scalar weighted function
        """
        if (not np.array_equal(self.xold,x)):
            res=self.compute_model(x)
            self.results_val = Results(res, self.resultsShape, self.spec,
                                       jac = False)
            self.xold=np.array(x, copy=True)
            #construction de la fonction de penalité
        fobj = (self.results_val.objectives[0]-self.spec.objectives_val[0])/\
               (self.spec.objectives_val[1]-self.spec.objectives_val[0])
        if (self.spec.eq_cstr != []):
            for i in range(len(self.spec.eq_cstr)):
                if isinstance(self.spec.eq_cstr_val.List[i],(int,float)):
                    fobj = fobj + 1000.*abs(self.results_val.eq_cstr.List[i]-
                            self.spec.eq_cstr_val.List[i])
                else:
                    for j in range(len(self.spec.eq_cstr_val.List[i])):
                        fobj=fobj+1000.*abs(self.results_val.eq_cstr.List[i][j]
                            -self.spec.eq_cstr_val.List[i][j])
        if (self.spec.ineq_cstr != []):
            for i in range(len(self.spec.ineq_cstr)):
                if isinstance(self.spec.ineq_cstr_bnd.List[i][0],list):
                    for j in range(len(self.spec.ineq_cstr_bnd.List[i])):
                        if self.spec.ineq_cstr_bnd.List[i][j][1]!=None:
                            fobj = fobj + 1000.*max(self.results_val.ineq_cstr.
                             List[i][j]-self.spec.ineq_cstr_bnd.List[i][j][1],0)
                        if self.spec.ineq_cstr_bnd.List[i][j][0] != None:
                            fobj = fobj + 1000. * max(self.spec.ineq_cstr_bnd.
                             List[i][j][0]-self.results_val.ineq_cstr.List[i]
                             [j],0)
                else:
                    if self.spec.ineq_cstr_bnd.List[i][1]!=None:
                        fobj = fobj + 1000. * max(self.results_val.ineq_cstr.
                            List[i]-self.spec.ineq_cstr_bnd.List[i][1] , 0)
                    if self.spec.ineq_cstr_bnd.List[i][0] != None:
                        fobj = fobj + 1000. * max(self.spec.ineq_cstr_bnd.
                            List[i][0]-self.results_val.ineq_cstr.List[i] , 0)
        return fobj
    def solution(self):
        """
        Returns the model inputs computed at the last iteration of the
        algorithm.
        :return: list of model inputs
        """
        if self.spec.xinit_sh != [0] * len(self.spec.iNames):
            return self.resultsHandler.solutions[-1].iData
        return self.resultsHandler.solutions[-1].iData.tolist()

    def getLastInputs(self):
        """
        Returns the model inputs computed at the last iteration of the
        algorithm.
        :return: dictionary containing the model inputs
        """
        lastSol = self.resultsHandler.solutions[-1]
        if len(self.resultsHandler.iNames)==1:
            dico = {self.resultsHandler.iNames[0]:
                        np.array(lastSol.iData).tolist()}
        else:
            dico = {self.resultsHandler.iNames[i]: lastSol.iData[i]
                    for i in range(len(self.resultsHandler.iNames))}
        return dico

    def getLastOutputs(self):
        """
        Returns the outputs of the model computed at the last iteration of
        the algorithm.
        :return: dictionary containing the model outputs
        """
        lastSol = self.resultsHandler.solutions[-1]
        dico = {self.resultsHandler.oNames[i]: lastSol.oData[i]
                for i in range(len(self.resultsHandler.oNames))}
        if self.spec.freeOutputs !=[]:
            dico.update({self.resultsHandler.fNames[i]: lastSol.fData[i]
                         for i in range(len(self.resultsHandler.fNames))})
        return dico

    def printResults(self):
        """
        Displays the inputs and outputs of the model computed at the last
        iteration of the algorithm.
        :return: /
        """
        print(self.getLastInputs())
        print(self.getLastOutputs())

    def printAllResults(self):
        """
        Displays the inputs and outputs of the model computed at each iteration
         of the algorithm.
        :return: /
        """
        sols = self.resultsHandler.solutions
        for sol in sols:
            if len(self.resultsHandler.iNames)==1:
                dico = {self.resultsHandler.iNames[0]:
                            np.array(sol.iData).tolist()}
            else:
                dico = {self.resultsHandler.iNames[i]:
                   sol.iData[i] for i in range(len(self.resultsHandler.iNames))}
            print(dico)

    def getIteration(self,iternum):
        '''
        Returns the inputs and the outputs of the model computed at the number
        of iteration given in parameter.
        :param iternum: the number of iteration
        :return: dictionnaries containing the inputs and outputs
        '''
        sols=self.resultsHandler.solutions
        sol=sols[iternum-1]
        if len(self.resultsHandler.iNames)==1:
            iData={self.resultsHandler.iNames[0] : np.array(sol.iData).tolist()}
        else:
            iData={self.resultsHandler.iNames[i] : sol.iData[i]
                   for i in range(len(self.resultsHandler.iNames))}
        oData={self.resultsHandler.oNames[i] : sol.oData[i]
               for i in range(len(self.resultsHandler.oNames))}
        if self.spec.freeOutputs != []:
            fData={self.resultsHandler.fNames[i] : sol.fData[i]
                   for i in range(len(self.resultsHandler.fNames))}
            return iData,oData,fData
        else:
            return iData,oData

    def exportToXML(self, fileName):
        """
        Return an XMLfile compatible with CADES. This can be used to plot
        geometry in GeomMaker.
        :param fileName: the filename to save XML tree
        :return: /
        """
        return resultsToXML(self.resultsHandler, fileName)

    def plotResults(self,outputs_names=[]):
        """
        Displays the results (inputs + outputs) graphically.
        :return: /
        """

        import noload.gui.plotIterations as pltIter
        pltIter.plotIO(self.resultsHandler,self.spec,outputs_names)

    def addParetoList(self,*args):
        '''
        Allows to display several Pareto Front in one graph.
        :param args: several result class
        :return:  /
        '''
        for result in args:
            self.ParetoList.append(result.resultsHandler)
        self.ParetoList.append(self.resultsHandler)

    def plotPareto(self,legend,title="Pareto front",nb_annotation = 5,
                   joinDots=True):
        """
        Plots a Pareto Front for a bi-objective optimization problem.
        :param legend: legend of the graph
        :param title: title of the graph
        :param nb_annotation: number of annotations
        :param joinDots: if True, do an interpolation spline.
        :return: /
        """
        import noload.gui.plotPareto as pp
        if self.ParetoList==[]:
            self.ParetoList.append(self.resultsHandler)
        pp.plot(self.ParetoList,self.spec.objectives,legend,title,
                self.spec,nb_annotation,joinDots)

    def plotNormalizedSolution(self):
        """
        Displays the "normalized" solution (values between 0 and 1) graphically.
        :return: /
        """
        bnd=np.transpose(self.spec.bounds)
        sols = self.solution()
        x = list(range(0,len(sols)))
        #normalize :
        mean = (bnd[1]+bnd[0])/2
        init = self.spec.xinit
        solsN = (sols-init)/(bnd[1]-bnd[0])

        import matplotlib.pyplot as plt
        plt.bar(x, solsN)
        plt.show()

    def openGUI(self):
        from noload.gui.OpenGUI import openGUI
        openGUI(self.resultsHandler)
