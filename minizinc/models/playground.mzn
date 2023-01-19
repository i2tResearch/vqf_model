% Use this editor as a MiniZinc scratch book

int: N = 2;
set of int: i = 1..N;
int:M = 5;
set of int: k = 1..M;

array[i, k] of float: d_ik;
d_ik = [| 1.5, 2.0, 3.0, 4.3, 5.1
        | 2.4, 4.0, 3.1, 5.9, 1.8 |];

array[k] of int: pob_k;
pob_k = [100, 90, 20, 50, 80];

var 1.0..10000.0: resp_d;
var 1..1000: resp_pob;
var int: resp_sum_a;
var int: resp_sum_b;
var int: resp_sum_c;
var int: resp_sum_d;
array[i] of var int: max_k_index;
array[k] of var int: max_i_index;
array[k] of var 0..1: iif;

constraint resp_d = sum(ind_i in i, ind_k in k)(d_ik[ind_i, ind_k]);

constraint resp_pob = sum(ind_k in k)(pob_k[ind_k]);

constraint forall(ind_i in i)
  (max_k_index[ind_i] = arg_max(d_ik[ind_i, ..]));
  
constraint forall(ind_k in k)
  (max_i_index[ind_k] = arg_max(d_ik[.., ind_k]));
  
constraint forall(ind_k in k)
  (iif[ind_k] = (ind_k > 2));
  
constraint resp_sum_a = (sum(ind_k in k)(pob_k[ind_k]) > 500);
constraint resp_sum_b = ((sum(ind_k in k)(pob_k[ind_k])) > 500);
constraint resp_sum_c = (sum(ind_k in k)(pob_k[ind_k]) < 500);
constraint resp_sum_d = ((sum(ind_k in k)(pob_k[ind_k])) < 500);

solve satisfy;