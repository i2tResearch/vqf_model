import logging

logging.basicConfig(filename="vqf_logs.log", level=logging.DEBUG)

from minizinc import Instance, Model, Solver

model = Model("../../minizinc/models/vqf.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

#################### Variables de entrada ####################

# Número de estaciones base; índice i. int
instance["N"] = 2
# Número de puntos en los que se harán mediciones de señal; índice k. int
instance["M"] = 5
# Distancia entre la i-ésima estación base y el k-ésimo punto de medición. float
instance["d_ik"] = [[1.5, 2.0, 3.0, 4.3, 5.1], [5.4, 4.0, 3.1, 2.9, 1.8]]
# Población que demanda servicio en el punto k. int
instance["pob_k"] = [100, 90, 20, 50, 80]
# Indica si dos antenas comparten el mismo Bloque de Recursos. j {1..3N}. bool
instance["cocan_ij"] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# Cantidad recursos asignados a la radiobase i. int
instance["channels"] = [20, 20]
# Número de Sectores disponibles para prestar el servicio. int
instance["maxSol"] = 8
# Cardinalidad mínima deseada para el active set, se busca que en la mayoría 
# de puntos de medición la superen sin que no hacerlo represente infactibilidad. 
# Corresponde al número mínimo de sectores que deberían poder atender el servicio. int
instance["minSol"] = 1
# Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm. float
instance["UmbCob"] = -70.1
# Umbral que define el mínimo nivel permitido para la relación portadora 
# interferencia (SINR) para cada servicio. float
instance["UmbInterf"] = 1
# Número de antenas por estación base. int
instance["P"] = 3
# Peso del objetivo Cantidad de población atendida
instance["W1"] = 1
# Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
instance["W2"] = 1

result = instance.solve()