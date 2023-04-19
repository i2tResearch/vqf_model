##############################################################
# Grupo i2t. Universidad Icesi                               #
# Módulo Python para interactura con el                      #
# modelo de optimización ODISEO                              #
##############################################################

from minizinc import Instance, Model, Solver
from models import Project


class Optimizer:

    def __init__(self, project: Project, model_path: str, solver: str):
        self.project = project
        self.model_path = model_path
        self.solver = solver

        self.c_k = []
        self.lrbs_ik = []
        self.lant_ik = []
        self.lsig_ik = []
        self.lflgcob_ik = []
        self.inddessig_k = []

        self.build_parameters()

    def optimize(self, max_sol: int, min_sol: int):
        model = Model(self.model_path)
        gecode = Solver.lookup(self.solver)
        instance = Instance(gecode, model)

        # Número de estaciones base; índice i. int
        instance["N"] = len(self.project.sites)
        # Número de puntos en los que se harán mediciones de señal; índice k. int
        instance["M"] = self.project.number_of_points()
        # Población que demanda servicio en el punto k. int
        instance["pob_k"] = [1] * self.project.number_of_points()
        # Número de Sectores disponibles para prestar el servicio. int
        instance["maxSol"] = max_sol
        # Número mínimo de sectores que deberían poder atender el servicio. int
        instance["minSol"] = min_sol
        # Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm. float
        instance["UmbCob"] = self.project.threshold
        # Número de antenas por estación base. int
        # Supone que todos los sitios tienen el mismo número de antenas
        instance["P"] = len(self.project.sites[0].transmitters)
        # Peso del objetivo Cantidad de población atendida
        instance["W1"] = 1
        # Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
        instance["W2"] = 1
        # Flag que indica si el punto k tiene cobertura de alguna radiobase. bool
        instance["C_k"] = self.c_k
        # Indica si la radiobase i cubre el punto k
        instance["lRbs_ik"] = self.build_lRbs_ik()
        # Si lRbs_ik, indica el índice h de la antena que lo cubre
        instance["lAnt_ik"] = self.lant_ik
        # Nivel de señal que desde la antena lAnt_ik llega al punto
        instance["lSig_ik"] = self.lsig_ik
        # Indica si lSig_ik supera el umbral de cobertura
        instance["lFlgCob_ik"] = self.lflgcob_ik
        # Índice de la radiobase que brinda el nivel de señal más alto en el punto k
        instance["indDesSig_k"] = self.inddessig_k

    def build_parameters(self):
        c_k = []
        lrbs_ik = []
        lant_ik = []
        lsig_ik = []
        lflgcob_ik = []
        inddessig_k = []

        for row in self.project.distribution_matrix:
            for value in row:
                c_value = 1 if value >= 0 else 0
                c_k.append(c_value)
                inddessig_value = value if value >= 0 else -1
                inddessig_k.append(inddessig_value)

        for s in self.project.sites:  # cada sitio es una i
            lrbs_i = []
            lant_i = []
            lsig_i = []
            lflgcob_i = []
            for h, t in enumerate(s.transmitters):  # cada transmisor es una h
                for row in t.coverage_matrix:
                    for lsig_value in row:  # cada punto es una k con potencia lsig_value
                        lrsb_value = 1 if lsig_value > self.project.threshold else 0
                        lant_value = h if lrsb_value == 1 else -1
                        lflgcob_value = lrsb_value
                        lrbs_i.append(lrsb_value)
                        lant_i.append(lant_value)
                        lsig_i.append(lsig_value)
                        lflgcob_i.append(lflgcob_value)
            lrbs_ik.append(lrbs_i)
            lant_ik.append(lant_i)
            lsig_ik.append(lsig_i)
            lflgcob_ik.append(lflgcob_i)

        self.c_k = c_k
        self.lrbs_ik = lrbs_ik
        self.lant_ik = lant_ik
        self.lsig_ik = lsig_ik
        self.lflgcob_ik = lflgcob_ik
        self.inddessig_k = inddessig_k
