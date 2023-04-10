##############################################################
# Grupo i2t. Universidad Icesi                               #
# Módulo Python para interactura con el                      #
# modelo de optimización ODISEO                              #
##############################################################

#################### Configurar logs ####################

import logging
logging.basicConfig(filename="vqf_logs.log", level=logging.DEBUG)

#################### Conexión del modelo ####################

from minizinc import Instance, Model, Solver

model = Model("../../minizinc/models/vqf_simplified.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

#################### Variables de entrada ####################

# Número de estaciones base; índice i. int
instance["N"] = 2
# Número de puntos en los que se harán mediciones de señal; índice k. int
instance["M"] = 5
# Población que demanda servicio en el punto k. int
instance["pob_k"] = [100, 100, 100, 100, 100]
# Número de Sectores disponibles para prestar el servicio. int
instance["maxSol"] = 6
# Cardinalidad mínima deseada para el active set, se busca que en la mayoría 
# de puntos de medición la superen sin que no hacerlo represente infactibilidad. 
# Corresponde al número mínimo de sectores que deberían poder atender el servicio. int
instance["minSol"] = 1
# Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm. float
instance["UmbCob"] = -70.1
# Número de antenas por estación base. int
instance["P"] = 3
# Peso del objetivo Cantidad de población atendida
instance["W1"] = 1
# Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
instance["W2"] = 1

#################### Estructuras de datos ####################

# Estas estructuras de datos se construyen a partir de los resultados de Celgis

# Flag que indica si el punto k tiene cobertura de alguna radiobase. bool
instance["C_k"] = [1, 0, 0, 1, 0]
# Indica si la radiobase i cubre el punto k
instance["lRbs_ik"] = [[0, 0, 0, 1, 0], [1, 0, 0, 1, 0]]
# Si lRbs_ik, indica el índice h de la antena que lo cubre
instance["lAnt_ik"] = [[0, 0, 0, 2, 0], [3, 0, 0, 2, 0]]
# Nivel de señal que desde la antena lAnt_ik llega al punto
instance["lSig_ik"] = [[-100.0, -100.0, -100.0, -50.0, -100.0], [-20.0, -100.0, -100.0, -80.0, -100.0]]
# Indica si lSig_ik supera el umbral de cobertura
instance["lFlgCob_ik"] = [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0]]
# Índice de la radiobase que brinda el nivel de señal más alto en el punto k
instance["indDesSig_k"] = [1, 0, 0, 2, 0]

#################### Solución del modelo ####################

result = instance.solve()
