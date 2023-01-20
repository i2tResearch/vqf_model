% Modelo en MiniZinc para el Proyecto VQF
% Grupo i2T, Universidad Icesi

%%%%%%%%%%%%%%%%%%%% Variables de Entrada %%%%%%%%%%%%%%%%%%%%

% Número de estaciones base e índice
int: N;
set of int: i = 1..N;

% Número de puntos en los que se harán mediciones de señal e índice
int: M;
set of int: k = 1..M;

% Distancia entre la i-ésima estación base y el k-ésimo punto de medición
array[i, k] of float: d_ik;

% Población que demanda servicio en el punto k
array[k] of int: pob_k;

% Índice de antenas
set of int: j = 1..3*N;

% Indica si dos antenas comparten el mismo Bloque de Recursos. 
array[i, j] of 0..1: cocan_ij;

% Cantidad recursos asignados a la radiobase i
array[i] of int: channels;

% Número de Sectores disponibles para prestar el servicio
int: maxSol;

% Número mínimo de sectores que deberían poder atender el servicio
int: minSol;

% Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm
float: UmbCob;

% Mínimo nivel permitido para la relación portadora interferencia (SINR) para cada servicio
float: UmbInterf;

% Número de antenas por estación base e índice
int: P;
set of int: h = 1..P;

% Peso del objetivo Cantidad de población atendida
int: W1 = 1;

% Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
int: W2 = 1;

%%%%%%%%%%%%%%%%%%%% Estructuras de Datos %%%%%%%%%%%%%%%%%%%%

% Flag que indica si el punto k tiene cobertura de alguna radiobase
array[k] of 0..1: C_k;

% Indica si la radiobase i cubre el punto k
array[i, k] of 0..1: lRbs_ik;

% Si lRbs_ik, indica el índice h de la antena que lo cubre
array[i, k] of int: lAnt_ik;

% Nivel de señal que desde la antena lAnt_ik llega al punto
array[i, k] of float: lSig_ik;

% Indica si lSig_ik supera el umbral de cobertura
array[i, k] of 0..1: lFlgCob_ik;

% Ángulo de azimut con el que la antena lAnt_ik incide en el punto k
array[i, k] of float: lAz_ik;

% Ángulo de elevación con el que la antena lAnt_ik incide en el punto k
array[i, k] of float: lEl_ik;

% Índice de la radiobase que brinda el nivel de señal más alto en el punto k
array[k] of int: indDesSig_k;

%%%%%%%%%%%%%%%%%%%% Variables de Decisión %%%%%%%%%%%%%%%%%%%%

% Azimuth de la h-ésima antena
array[i, h] of var 0..359: AzAnt_ih;

% Elevación de la h-ésima antena. Positivo hacia abajo
array[i, h] of var -10..45: ElAnt_ih;

% Potencia de la h-ésima antena
array[i, h] of var float: Pot_ih;

%%%%%%%%%%%%%%%%%%%% Restricciones %%%%%%%%%%%%%%%%%%%%

% Radiobase cubre el punto
constraint forall(_i in i, _k in k)
  (lRbs_ik[_i, _k] = 1 <-> lSig_ik[_i, _k] > UmbCob);

% Señal deseada en el punto k. El nivel de señal correspondiente al índice de la señal deseada debe ser el mayor de ellos
constraint forall(_k in k)
  (indDesSig_k[_k] = arg_max(lSig_ik[.., _k]));

% Sector cubre punto si y solo si el nivel de señal que de él llega al punto supera el umbral
constraint forall(_i in i, _k in k)
  (lFlgCob_ik[_i, _k] = 1 <-> lSig_ik[_i, _k] > UmbCob);

% Cardinalidad del active set: total de puntos cubiertos
constraint sum(_i in i, _k in k)(lFlgCob_ik[_i, _k]) <= maxSol;

constraint forall(_k in k)
  (min(lFlgCob_ik[.., _k]) = 1 <-> (sum(_i in i)(lFlgCob_ik[_i, _k]) >= minSol));

% Restricción de azimut por sector de antena
constraint forall(_i in i)
  (AzAnt_ih[_i, 1] >= 0 /\ AzAnt_ih[_i, 1] <= 119);
constraint forall(_i in i)
  (AzAnt_ih[_i, 2] >= 120 /\ AzAnt_ih[_i, 2] <= 239);
constraint forall(_i in i)
  (AzAnt_ih[_i, 3] >= 240 /\ AzAnt_ih[_i, 3] <= 359);

%%%%%%%%%%%%%%%%%%%% Función objetivo %%%%%%%%%%%%%%%%%%%%

% Total población atendida
var int: total_pob = sum(_k in k)(C_k[_k] * pob_k[_k]);
% Total puntos con cobertura superior al mínimo definido
var int: total_kcob = sum(_k in k)(min(lFlgCob_ik[.., _k]));
% Objetivo con pesos
solve maximize W1 * total_pob + W2 * total_kcob;
