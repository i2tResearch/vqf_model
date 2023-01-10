% MiniZinc model for the VQF project

%%%%%%%%%% Input variables %%%%%%%%%%

% Número de estaciones base
int N; 
% Índice de estaciones base
set of int: i = 1..N; 

% Número de puntos en los que se harán mediciones de señal
int M; 
% Índice de puntos de medición
set of int: k = 1..M; 

% Distancia entre la i-ésima estación base y el k-ésimo punto de medición
array[i, k] of var float: d_ik; 

% Población que demanda servicio en el punto k
array[k] of var int: pob_k; 

% Índice de antenas
set of int: j = 1..3*N; 
% Indica si dos antenas comparten el mismo Bloque de Recursos
array[i, j] of var bool: cocan_ij; 

% Cantidad recursos asignados a la radiobase i
array[i] of var int: channels; 

% Número de Sectores disponibles para prestar el servicio
int maxSol; 

% Número mínimo de sectores que deberían poder atender el servicio
int minSol; 

% Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm
float UmbCob; 

%Umbral que define el mínimo nivel permitido para la relación portadora interferencia (SINR) para cada servicio
float UmbInterf; 

%%%%%%%%%% Decision variables %%%%%%%%%%

% Número de antenas por estación base
int P;
% Índice de antenas
set of int: h = 1..P;

% Flag que indica si el punto k tiene cobertura de alguna radiobase
array[k] of var bool: C_k;

% Azimuth de la h-ésima antena
array[i, h] of var float AzAnt_ih;

% Elevación de la h-ésima antena
array[i, h] of var float ElAnt_ih;

% Potencia de la h-ésima antena
array[i, h] of var float Pot_ih;

% Cantidad de población por Sector
array[i] of var int Pob_j;

%%%%%%%%%% Data structures %%%%%%%%%%

% Indica si la radiobase i cubre el punto k
array[i, k] of var bool lRbs_ik;
% Si lRbs_ik, indica el índice de la antena que lo cubre
array[i, k] of var int lAnt_ik;
% Nivel de señal que desde la antena lAnt_ik llega al punto
array[i, k] of var float lSig_ik;
% Indica si lSig_ik supera el umbral de cobertura
array[i, k] of var bool lFlgCob_ik;
% Ángulo de azimut con el que la antena lAnt_ik incide en el punto k
array[i, k] of var bool lAz_ik;
% Ángulo de elevación con el que la antena lAnt_ik incide en el punto k
array[i, k] of var bool lEl_ik;
% Índice de la radiobase que brinda el nivel de señal más alto en el punto k
array[k] of var bool indDesSig_ik;

%%%%%%%%%% Constraints %%%%%%%%%%
