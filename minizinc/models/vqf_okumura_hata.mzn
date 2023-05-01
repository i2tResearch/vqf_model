% Modelo en MiniZinc para el Proyecto VQF
% Grupo i2T, Universidad Icesi

%%%%%%%%%%%%%%%%%%%% Modelo de propagación Okumura-Hata %%%%%%%%%%%%%%%%%%%%

function float: cost231_okumura_hata(float: freq, float: tx_height, float: rx_height, float: distance, float: city_size_factor) =
  46.3 + 33.9 * log10(freq) - 13.82 * log10(tx_height)
  - (1.1 * log10(freq) - 0.7) * rx_height
  - (44.9 - 6.55 * log10(tx_height)) * log10(distance)
  + city_size_factor;

%%%%%%%%%%%%%%%%%%%% Variables de Entrada. Parámetros que no dependen del escenario %%%%%%%%%%%%%%%%%%%%

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
% Número de Sectores disponibles para prestar el servicio
int: maxSol;
% Número mínimo de sectores que deberían poder atender el servicio
int: minSol;
% Umbral a partir del cual se puede definir si un punto tiene o no cobertura, dado en dBm
float: UmbCob;
% Número de antenas por estación base e índice
int: P;
set of int: h = 1..P;
% Peso del objetivo Cantidad de población atendida
int: W1 = 1;
% Peso del objetivo Cantidad de puntos con cobertura superior al mínimo definido
int: W2 = 1;
% Potencia máxima permitida
float: maxPot;
% Altura del terminal de usuario
float: pobHeight;
% Factor de tamaño de ciudad para el modelo de propagación
float: citySizeFactor;

%%%%%%%%%%%%%%%%%%%% Escenario inicial tomado de Celgis %%%%%%%%%%%%%%%%%%%%

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
% Índice de la radiobase que brinda el nivel de señal más alto en el punto k
array[k] of int: indDesSig_k;
% Frecuencia de la antena de índice h en la radiobase k
array[i, h] of float: lFreq_ih;
% Altura de la antena de índice h en la radiobase k
array[i, h] of float: lHeight_ih;
% Azimuth de la h-ésima antena
array[i, h] of 0.0..359.0: AzAnt_ih;
% Elevación de la h-ésima antena. Positivo hacia abajo
array[i, h] of -10.0..45.0: ElAnt_ih;
% Potencia de la h-ésima antena
array[i, h] of float: Pot_ih;
% Total población atendida
int: total_pob_inicial = sum(K in k)(C_k[K] * pob_k[K]);
% Total puntos con cobertura superior al mínimo definido
int: total_kcob_inicial = sum(K in k)(min(lFlgCob_ik[.., K]));
% Objetivo con pesos
float: objetivo_inicial = W1 * total_pob_inicial + W2 * total_kcob_inicial;

% %%%%%%%%%%%%%%%%%%%% Cálculos del modelo de propagación. Comunes a todos los escenarios %%%%%%%%%%%%%%%%%%%%

array[i, h, k] of float: pathLoss = array3d(i, h, k, [
  (cost231_okumura_hata(lFreq_ih[I, H], lHeight_ih[I, H], pobHeight, d_ik[I, K], citySizeFactor))
  | I in i, H in h, K in k]);

% %%%%%%%%%%%%%%%%%%%% Cálculos teóricos del escenario inicial. Marcados con _a %%%%%%%%%%%%%%%%%%%%

array[i, h, k] of float: lSig_ihk_a = array3d(i, h, k, [(Pot_ih[I, H] - pathLoss[I, H, K]) | I in i, H in h, K in k]);
array[i, k] of float: lSig_ik_a = array2d(i, k, [max(lSig_ihk_a[I, .., K]) | I in i, K in k]);
array[i, k] of 0..1: lRbs_ik_a = array2d(i, k, [if lSig_ik_a[I, K] > UmbCob then 1 else 0 endif | I in i, K in k]);
array[k] of 0..1: C_k_a = [max(lRbs_ik_a[.., K]) | K in k];
array[i, k] of 0..1: lFlgCob_ik_a = array2d(i, k, [if lSig_ik_a[I, K] > UmbCob then 1 else 0 endif | I in i, K in k]);
int: total_pob_a = sum(K in k)(C_k_a[K] * pob_k[K]);
int: total_kcob_a = sum(K in k)(min(lFlgCob_ik_a[.., K]));
float: objetivo_a = W1 * total_pob_a + W2 * total_kcob_a;

% %%%%%%%%%%%%%%%%%%%% Cálculos del escenario modificado. Marcados con _b %%%%%%%%%%%%%%%%%%%%

array[i, h, k] of var float: lSig_ihk_b = array3d(i, h, k, [(Pot_ih_b[I, H] - pathLoss[I, H, K]) | I in i, H in h, K in k]);
array[i, k] of var float: lSig_ik_b = array2d(i, k, [max(lSig_ihk_b[I, .., K]) | I in i, K in k]);
array[i, k] of var 0..1: lRbs_ik_b = array2d(i, k, [if lSig_ik_b[I, K] > UmbCob then 1 else 0 endif | I in i, K in k]);
array[k] of var 0..1: C_k_b = [max(lRbs_ik_b[.., K]) | K in k];
array[i, k] of var 0..1: lFlgCob_ik_b = array2d(i, k, [if lSig_ik_b[I, K] > UmbCob then 1 else 0 endif | I in i, K in k]);
var int: total_pob_b = sum(K in k)(C_k_b[K] * pob_k[K]);
var int: total_kcob_b = sum(K in k)(min(lFlgCob_ik_b[.., K]));
var float: objetivo_b = W1 * total_pob_b + W2 * total_kcob_b;

% %%%%%%%%%%%%%%%%%%%% Variables de Decisión %%%%%%%%%%%%%%%%%%%%

% Azimuth de la h-ésima antena
% array[i, h] of var 0.0..359.0: AzAnt_ih_b = AzAnt_ih;
% Elevación de la h-ésima antena. Positivo hacia abajo
% array[i, h] of var -10.0..45.0: ElAnt_ih_b = ElAnt_ih;
% Potencia de la h-ésima antena
array[i, h] of var UmbCob..maxPot: Pot_ih_b;

%%%%%%%%%%%%%%%%%%%% Restricciones %%%%%%%%%%%%%%%%%%%%

constraint objetivo_b > objetivo_a;

%%%%%%%%%%%%%%%%%%%% Otros resultados de validación %%%%%%%%%%%%%%%%%%%%

var float: max_lSig_ik = max(lSig_ik[.., ..]);
var float: min_lSig_ik = min(lSig_ik[.., ..]);

var float: max_lSig_ik_a = max(lSig_ik_a[.., ..]);
var float: min_lSig_ik_a = min(lSig_ik_a[.., ..]);

var float: max_lSig_ik_b = max(lSig_ik_b[.., ..]);
var float: min_lSig_ik_b = min(lSig_ik_b[.., ..]);

output ["Resultados"] ++ 
  ["\nValor objetivo inicial: \(objetivo_inicial). Pob: \(total_pob_inicial). Puntos: \(total_kcob_inicial)"] ++
  ["\nValor objetivo teorico inicial: \(objetivo_a). Pob: \(total_pob_a). Puntos: \(total_kcob_a)"] ++
  ["\nValor objetivo final: \(objetivo_b). Pob: \(total_pob_b). Puntos: \(total_kcob_b)"] ++
  ["\nPotencias iniciales: "] ++ [show_float(0, 2, Pot_ih[I, H]) | I in i, H in h] ++
  ["\nPotencias finales: "] ++ [show_float(0, 2, Pot_ih_b[I, H]) | I in i, H in h] ++
  ["\nMáximos (inicial, teórico y final): "] ++ ["\(max_lSig_ik), \(max_lSig_ik_b), \(max_lSig_ik_b)"] ++
  ["\nMínimos (inicial, teórico y final): "] ++ ["\(min_lSig_ik), \(min_lSig_ik_b), \(min_lSig_ik_b)"]
  ;
