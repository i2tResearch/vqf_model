% MiniZinc model for the VQF project

% Input variables

int N; % Número de estaciones base
set of int: i = 1..N; % Índice de estaciones base

int M; % Número de puntos en los que se harán mediciones de señal
set of int: k = 1..M; % Índice de puntos de medición

array[i, k] of var float: d_ik; % Distancia entre la i-ésima estación base y el k-ésimo punto de medición

array[k] of var int: pob_k; % Población que demanda servicio en el punto k

set of int: j = 1..3*N; % Índice de antenas
array[i, j] of var bool: cocan_ij; % Indica si dos antenas comparten el mismo Bloque de Recursos

array[i] of var int: channels; % Cantidad recursos asignados a la radiobase i

int maxSol; % Número de Sectores disponibles para prestar el servicio

int minSol; % Número mínimo de sectores que deberían poder atender el servicio

float UmbCob; % Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm

float UmbInterf; %Umbral que define el mínimo nivel permitido para la relación portadora interferencia (SINR) para cada servicio

% Decision variables

int P; % Número de antenas por estación base
set of int: h = 1..P; % Índice de antenas

array[k] of var bool: C_k; % Flag que indica si el punto k tiene cobertura de alguna radiobase

array[i, h] of var float AzAnt_ih; % Azimuth de la h-ésima antena

array[i, h] of var float ElAnt_ih; % Elevación de la h-ésima antena

array[i, h] of var float Pot_ih; % Potencia de la h-ésima antena

array[i] of var int Pob_j; % Cantidad de población por Sector
