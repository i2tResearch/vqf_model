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

        self.d_ik = []
        self.c_k = []
        self.lrbs_ik = []
        self.lant_ik = []
        self.lsig_ik = []
        self.lflgcob_ik = []
        self.inddessig_k = []

        self.lfreq_ih = []
        self.lheight_ih = []

        self.build_parameters()

    def optimize(self, max_sol: int, min_sol: int):
        model = Model(self.model_path)
        gecode = Solver.lookup(self.solver)
        instance = Instance(gecode, model)

        # Variables de entrada

        # Número de estaciones base; índice i. int
        instance["N"] = len(self.project.sites)
        # Número de puntos en los que se harán mediciones de señal; índice k. int
        instance["M"] = self.project.number_of_points()
        # Distancia entre la i-ésima estación base y el k-ésimo punto de medición
        instance["d_ik"] = self.d_ik
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

        # Estructuras de datos. TODO: Entregar las estructuras desde Celgis. Hacer llamado dinámico a celgis

        # Flag que indica si el punto k tiene cobertura de alguna radiobase. bool
        instance["C_k"] = self.c_k
        # Indica si la radiobase i cubre el punto k
        instance["lRbs_ik"] = self.lrbs_ik
        # Si lRbs_ik, indica el índice h de la antena que lo cubre
        instance["lAnt_ik"] = self.lant_ik
        # Nivel de señal que desde la antena lAnt_ik llega al punto
        instance["lSig_ik"] = self.lsig_ik
        # Indica si lSig_ik supera el umbral de cobertura
        instance["lFlgCob_ik"] = self.lflgcob_ik
        # Índice de la radiobase que brinda el nivel de señal más alto en el punto k
        instance["indDesSig_k"] = self.inddessig_k

        # Hata model
        instance["lFreq_ih"] = self.lfreq_ih
        instance["lHeight_ih"] = self.lheight_ih
        instance["pobHeight"] = 3
        instance["citySizeFactor"] = 2

        result = instance.solve()
        return result

    def build_parameters(self):
        d_ik = []
        c_k = []
        lrbs_ik = []
        lant_ik = []
        lsig_ik = []
        lflgcob_ik = []
        inddessig_k = []
        lfreq_ih = []
        lheight_ih = []

        for row in self.project.distribution_matrix:
            for value in row:
                c_value = 1 if value >= 0 else 0
                c_k.append(c_value)
                inddessig_value = value if value >= 0 else -1
                inddessig_k.append(inddessig_value)

        for s in self.project.sites:  # cada sitio es una i
            d_i = []
            lrbs_i = []
            lant_i = []
            lsig_i = []
            lflgcob_i = []
            lfreq_i = []
            lheight_i = []

            for h, t in enumerate(s.transmitters):  # cada transmisor es una h
                for row in t.coverage_matrix:
                    for lsig_k_value in row:  # cada punto es una k con potencia lsig_k_value
                        d_i.append(t.height) # TODO: calculate distance
                        lrsb_k_value = 1 if lsig_k_value > self.project.threshold else 0
                        lant_k_value = h + 1 if lrsb_k_value == 1 else 0  # MiniZinc usa arreglos de base 1
                        lflgcob_k_value = lrsb_k_value
                        lrbs_i.append(lrsb_k_value)
                        lant_i.append(lant_k_value)
                        lsig_i.append(lsig_k_value)
                        lflgcob_i.append(lflgcob_k_value)

                lfreq_i.append(t.frequency)
                lheight_i.append(t.height)

            d_ik.append(d_i)
            lrbs_ik.append(lrbs_i)
            lant_ik.append(lant_i)
            lsig_ik.append(lsig_i)
            lflgcob_ik.append(lflgcob_i)

            lfreq_ih.append(lfreq_i)
            lheight_ih.append(lheight_i)

        self.d_ik = d_ik
        self.c_k = c_k
        self.lrbs_ik = lrbs_ik
        self.lant_ik = lant_ik
        self.lsig_ik = lsig_ik
        self.lflgcob_ik = lflgcob_ik
        self.inddessig_k = inddessig_k
        self.lfreq_ih = lfreq_ih
        self.lheight_ih = lheight_ih
