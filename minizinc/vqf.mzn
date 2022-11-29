% MiniZinc model for the VQF project

% ########## INPUT VARIABLES ##########

int N; % Número de estaciones base
set of int: i = 0..N; % Índice de estaciones base

int M; % Número de puntos en los que se harán mediciones de señal
set of int: k = 0..M; % Índice de puntos de medición

array[i, k] of var float: d_ik; % Distancia entre la i-esima estación base y el k-esimo punto de medición

array[k] of var int: pob_k; % Población que demanda servicio en el punto k

set of int: j = 0..3*N; % Índice de antenas
array[i, j] of var bool: cocan_ij; % Indica si dos antenas comparten el mismo Bloque de Recursos

array[i] of var int: channels; % Cantidad recursos asignados a la radiobase i

int maxSol; % Número de Sectores disponibles para prestar el servicio

int minSol; % Número mínimo de sectores que deberían poder atender el servicio

float UmbCob; % Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm

float UmbInterf; %Umbral que define el mínimo nivel permitido para la relación portadora interferencia (SINR) para cada servicio
