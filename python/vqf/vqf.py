##############################################################
# Grupo i2t. Universidad Icesi                               #
# Módulo Python para interactura con el                      #
# modelo de optimización ODISEO                              #
##############################################################

from minizinc import Instance, Model, Solver
from models import Project
from geopy import distance
import random


class Optimizer:

    def __init__(self, project: Project, model_path: str, maxpow: float, randomize_pob: bool, minSol: int):
        self.project = project
        self.model_path = model_path
        self.maxpow = maxpow
        self.randomize_pob = randomize_pob
        self.minSol = minSol

        self.d_ik = []
        self.c_k = []
        self.lrbs_ik = []
        self.lant_ik = []
        self.lsig_ik = []
        self.lflgcob_ik = []
        self.inddessig_k = []

        self.azant_ih = []
        self.elant_ih = []
        self.gaant_ih = []
        self.pot_ih = []

        self.lfreq_ih = []
        self.lheight_ih = []

        self.build_parameters()

    def optimize(self, solver_name):
        model = Model(self.model_path)
        solver = Solver.lookup(solver_name)
        instance = Instance(solver, model)

        # Variables de entrada

        # Número de estaciones base; índice i. int
        instance["N"] = len(self.project.sites)
        # Número de puntos en los que se harán mediciones de señal; índice k. int
        instance["M"] = self.project.number_of_points()
        # Distancia entre la i-ésima estación base y el k-ésimo punto de medición
        instance["d_ik"] = self.d_ik
        # Población que demanda servicio en el punto k. int
        instance["pob_k"] = [random.randint(0, 100) for _ in range(self.project.number_of_points())] if self.randomize_pob else [1] * self.project.number_of_points()
        # Número de Sectores disponibles para prestar el servicio. int
        instance["maxSol"] = self.project.number_of_points()
        # Número mínimo de sectores que deberían poder atender el servicio. int
        instance["minSol"] = max(self.minSol, 1)
        # Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm. float
        instance["UmbCob"] = self.project.threshold
        # Número de antenas por estación base. int
        # Supone que todos los sitios tienen el mismo número de antenas
        instance["P"] = len(self.project.sites[0].transmitters)
        # Peso del objetivo Cantidad de población atendida
        instance["W1"] = 1
        # Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
        instance["W2"] = 1
        # Potencia máxima permitida
        instance["maxPot"] = self.maxpow
        # Altura del terminal de usuario
        instance["pobHeight"] = 3
        # Factor de tamaño de ciudad para el modelo de propagación
        instance["citySizeFactor"] = 0

        # Estado inicial del escenario

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
        # Frecuencia de la antena de índice h en la radiobase k
        instance["lFreq_ih"] = self.lfreq_ih
        # Altura de la antena de índice h en la radiobase k
        instance["lHeight_ih"] = self.lheight_ih
        # Azimuth de la h-ésima antena
        instance["AzAnt_ih"] = self.azant_ih
        # Elevación de la h-ésima antena. Positivo hacia abajo
        instance["ElAnt_ih"] = self.elant_ih
        # Ganancia de la h-ésima antena
        instance["GaAnt_ih"] = self.gaant_ih
        # Potencia de la h-ésima antena
        instance["Pot_ih"] = self.pot_ih

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
        azant_ih = []
        elant_ih = []
        gaant_ih = []
        pot_ih = []
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
            azant_i = []
            elant_i = []
            gaant_i = []
            pot_i = []
            lfreq_i = []
            lheight_i = []

            for h, t in enumerate(s.transmitters):  # cada transmisor es una h
                for x, row in enumerate(t.coverage_matrix):
                    # cada punto es una k con potencia lsig_k_value
                    for y, lsig_k_value in enumerate(row):
                        (lat, lon) = self.project.index_to_coordinates(x, y)
                        d_k_value = distance.distance(
                            (s.latitude, s.longitude), (lat, lon)).km

                        lrsb_k_value = 1 if lsig_k_value > self.project.threshold else 0
                        # MiniZinc usa arreglos de base 1
                        lant_k_value = h + 1 if lrsb_k_value == 1 else 0
                        lflgcob_k_value = lrsb_k_value

                        d_i.append(d_k_value)
                        lrbs_i.append(lrsb_k_value)
                        lant_i.append(lant_k_value)
                        lsig_i.append(lsig_k_value)
                        lflgcob_i.append(lflgcob_k_value)

                azant_i.append(t.azimuth)
                elant_i.append(t.tilt)
                gaant_i.append(t.gain)
                pot_i.append(t.power)
                lfreq_i.append(t.frequency)
                lheight_i.append(t.height)

            d_ik.append(d_i)
            lrbs_ik.append(lrbs_i)
            lant_ik.append(lant_i)
            lsig_ik.append(lsig_i)
            lflgcob_ik.append(lflgcob_i)

            azant_ih.append(azant_i)
            elant_ih.append(elant_i)
            gaant_ih.append(gaant_i)
            pot_ih.append(pot_i)
            lfreq_ih.append(lfreq_i)
            lheight_ih.append(lheight_i)

        self.d_ik = d_ik
        self.c_k = c_k
        self.lrbs_ik = lrbs_ik
        self.lant_ik = lant_ik
        self.lsig_ik = lsig_ik
        self.lflgcob_ik = lflgcob_ik
        self.inddessig_k = inddessig_k
        self.azant_ih = azant_ih
        self.elant_ih = elant_ih
        self.gaant_ih = gaant_ih
        self.pot_ih = pot_ih
        self.lfreq_ih = lfreq_ih
        self.lheight_ih = lheight_ih
