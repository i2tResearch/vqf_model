% Modelo en MiniZinc para el Proyecto VQF
% Grupo i2T, Universidad Icesi

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

%%%%%%%%%%%%%%%%%%%% Estado inicial del escenario. Tomado de Celgis %%%%%%%%%%%%%%%%%%%%

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

%%%%%%%%%%%%%%%%%%%% Datos del escenario modificado. Marcados con _b %%%%%%%%%%%%%%%%%%%%

% Flag que indica si el punto k tiene cobertura de alguna radiobase
array[k] of var 0..1: C_k_b;
% Indica si la radiobase i cubre el punto k
array[i, k] of var 0..1: lRbs_ik_b;
% Si lRbs_ik, indica el índice h de la antena que lo cubre
array[i, k] of var int: lAnt_ik_b;
% Nivel de señal que desde la antena lAnt_ik llega al punto
array[i, k] of var float: lSig_ik_b;
% Indica si lSig_ik supera el umbral de cobertura
array[i, k] of var 0..1: lFlgCob_ik_b;
% Índice de la radiobase que brinda el nivel de señal más alto en el punto k
array[k] of var int: indDesSig_k_b;

%%%%%%%%%%%%%%%%%%%% Variables de Decisión %%%%%%%%%%%%%%%%%%%%

% Azimuth de la h-ésima antena
array[i, h] of var 0.0..359.0: AzAnt_ih_b = AzAnt_ih;
% Elevación de la h-ésima antena. Positivo hacia abajo
array[i, h] of var -10.0..45.0: ElAnt_ih_b = ElAnt_ih;
% Potencia de la h-ésima antena
array[i, h] of var float: Pot_ih_b = Pot_ih;

%%%%%%%%%%%%%%%%%%%% Restricciones %%%%%%%%%%%%%%%%%%%%

% Radiobase cubre el punto
constraint forall(I in i, K in k)
  (lRbs_ik_b[I, K] = 1 <-> lSig_ik_b[I, K] > UmbCob);

% Señal deseada en el punto k. 
% El nivel de señal correspondiente al índice de la señal deseada debe ser el mayor de ellos
constraint forall(I in i, K in k)
  (indDesSig_k_b[K] = I <-> max(lSig_ik_b[.., K]) = lSig_ik_b[I, K]);

% Sector cubre punto si y solo si el nivel de señal que de él llega al punto supera el umbral
constraint forall(I in i, K in k)
  (lFlgCob_ik_b[I, K] = 1 <-> lSig_ik_b[I, K] > UmbCob);

% Cardinalidad del active set: total de puntos cubiertos
constraint sum(I in i, K in k)(lFlgCob_ik_b[I, K]) <= maxSol;

constraint forall(K in k)
  (min(lFlgCob_ik_b[.., K]) = 1 <-> (sum(I in i)(lFlgCob_ik_b[I, K]) >= minSol));

% Restricción de azimut por sector de antena
array[int] of float: az_min = [0.0, 120.0, 240.0];
array[int] of float: az_max = [119.0, 239.0, 359.0];
constraint forall(I in i, H in h)
  (if H <= 3 then AzAnt_ih_b[I, H] >= az_min[H] /\ AzAnt_ih_b[I, H] <= az_max[I] else true endif);

% Restricción de potencia
constraint forall(I in i, H in h)
  (Pot_ih_b[I, H] >= UmbCob /\ Pot_ih_b[I, H] <= maxPot);

%%%%%%%%%%%%%%%%%%%% Modelo de propagación Okumura-Hata que ayuda a estimar el escenario B %%%%%%%%%%%%%%%%%%%%

function float: cost231_okumura_hata(float: freq, float: tx_height, float: rx_height, float: distance, float: city_size_factor) =
  46.3 + 33.9 * log10(freq) - 13.82 * log10(tx_height)
  - (1.1 * log10(freq) - 0.7) * rx_height
  - (44.9 - 6.55 * log10(tx_height)) * log10(distance)
  + city_size_factor;

array[i, h, k] of var float: pathLoss = array3d(i, h, k, [
  (
    cost231_okumura_hata(lFreq_ih[I, H], lHeight_ih[I, H], pobHeight, d_ik[I, K], citySizeFactor)
  ) | I in i, H in h, K in k]);

array[i, h, k] of var float: lSig_ihk = array3d(i, h, k, [(pathLoss[I, H, K] + Pot_ih_b[I, H]) | I in i, H in h, K in k]);

constraint forall(I in i, H in h, K in k)
  (lFlgCob_ik_b[I, K] = 1 <-> max(lSig_ihk[I, H, ..]) > UmbCob);

%%%%%%%%%%%%%%%%%%%% Función objetivo %%%%%%%%%%%%%%%%%%%%

% Total población atendida
var int: total_pob_final = sum(K in k)(C_k_b[K] * pob_k[K]);
% Total puntos con cobertura superior al mínimo definido
var int: total_kcob_final = sum(K in k)(min(lFlgCob_ik_b[.., K]));
% Objetivo con pesos
var float: objetivo_final = W1 * total_pob_final + W2 * total_kcob_final;

constraint objetivo_final > objetivo_inicial;

solve maximize objetivo_final;

output["Objetivo: \(objetivo_final)"];