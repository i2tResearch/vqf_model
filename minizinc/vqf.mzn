% MiniZinc model for the VQF project

int: n;
var 1..n: x;
var 1..n: y;
constraint x+y > n;
solve satisfy;