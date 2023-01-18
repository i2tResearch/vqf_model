% MiniZinc model for the VQF project

%%%%%%%%%%%%%%%%%%%% Variables de Entrada %%%%%%%%%%%%%%%%%%%%

% Número de estaciones base
int: N;
% Índice de estaciones base
set of int: i = 1..N;

% Número de puntos en los que se harán mediciones de señal
int: M;
% Índice de puntos de medición
set of int: k = 1..M;

% Distancia entre la i-ésima estación base y el k-ésimo punto de medición
array[i, k] of float: d_ik;

% Población que demanda servicio en el punto k
array[k] of int: pob_k;

% Índice de antenas
set of int: j = 1..3*N;
% Indica si dos antenas comparten el mismo Bloque de Recursos
array[i, j] of int: cocan_ij;

% Cantidad recursos asignados a la radiobase i
array[i] of int: channels;

% Número de Sectores disponibles para prestar el servicio
int: maxSol;

% Número mínimo de sectores que deberían poder atender el servicio
int: minSol;

% Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm
float: UmbCob;

% Umbral que define el mínimo nivel permitido para la relación portadora interferencia (SINR) para cada servicio
float: UmbInterf;

% Número de antenas por estación base
int: P;
% Índice de antenas
set of int: h = 1..P;

% Peso del objetivo Cantidad de población atendida
int: W1 = 1;

% Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido para el active set
int: W2 = 1;

%%%%%%%%%%%%%%%%%%%% Variables de Decisión %%%%%%%%%%%%%%%%%%%%

% Flag que indica si el punto k tiene cobertura de alguna radiobase
array[k] of var int: C_k;

% Azimuth de la h-ésima antena
array[i, h] of var float: AzAnt_ih;

% Elevación de la h-ésima antena
array[i, h] of var float: ElAnt_ih;

% Potencia de la h-ésima antena
array[i, h] of var float: Pot_ih;

% Cantidad de población por Sector
array[i] of var int: Pob_j;

%%%%%%%%%%%%%%%%%%%% Estructuras de Datos %%%%%%%%%%%%%%%%%%%%

% Indica si la radiobase i cubre el punto k
array[i, k] of var int: lRbs_ik;

% Si lRbs_ik, indica el índice h de la antena que lo cubre
array[i, k] of var int: lAnt_ik;

% Nivel de señal que desde la antena lAnt_ik llega al punto
array[i, k] of float: lSig_ik; % var float is not allowed in the constraint

% Indica si lSig_ik supera el umbral de cobertura
array[i, k] of var int: lFlgCob_ik;

% Ángulo de azimut con el que la antena lAnt_ik incide en el punto k
array[i, k] of var float: lAz_ik;

% Ángulo de elevación con el que la antena lAnt_ik incide en el punto k
array[i, k] of var float: lEl_ik;

% Índice de la radiobase que brinda el nivel de señal más alto en el punto k
array[k] of var int: indDesSig_k;

%%%%%%%%%%%%%%%%%%%% Restricciones %%%%%%%%%%%%%%%%%%%%

% Radiobase cubre el punto
constraint forall (ind_i in i, ind_k in k)
    (lRbs_ik[ind_i, ind_k] = if lSig_ik[ind_i, ind_k] > UmbCob then 1 else 0 endif);

% Señal deseada en el punto k. El nivel de señal correspondiente al índice de la señal deseada debe ser el mayor de ellos
constraint forall (ind_k in k)
    (indDesSig_k[ind_k] = arg_max(lSig_ik[.., ind_k]));

% Sector cubre punto si y solo si el nivel de señal que de él llega al punto supera el umbral
constraint forall (ind_i in i, ind_k in k)
    (lFlgCob_ik[ind_i, ind_k] = if lSig_ik[ind_i, ind_k] > UmbCob then 1 else 0 endif);

% Cardinalidad del active set: total de puntos cubiertos
constraint sum(ind_i in i, ind_k in k)(lFlgCob_ik[ind_i, ind_k]) <= maxSol;

constraint forall (ind_k in k)
    (min(lFlgCob_ik[.., ind_k]) = if sum(ind_i in i)(lFlgCob_ik[ind_i, ind_k]) >= minSol then 1 else 0 endif);

%%%%%%%%%%%%%%%%%%%% Función objetivo %%%%%%%%%%%%%%%%%%%%

solve maximize 
    W1 * sum(ind_k in k)(C_k[ind_k] * pob_k[ind_k]) + 
    W2 * sum(ind_k in k)(min(lFlgCob_ik[.., ind_k]));
