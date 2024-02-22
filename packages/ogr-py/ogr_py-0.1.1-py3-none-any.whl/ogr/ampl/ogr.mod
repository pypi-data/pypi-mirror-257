# Linear Programming model of a hardcoded order 3 golomb ruler.

# Tasks for generalization:
# express the distance variables as an upper triangualar matrix?

param upper_bound;
param order;

set N = {1..order};
set V = {1..upper_bound};
set pairs = {i in N, j in (i + 1)..order};
set pairs_consecutive = {i in 1..order - 1, j in (i + 1)..order};

var d {pairs} >= 1;
var e {pairs, V} binary;

minimize total_length: d[1, order];

subject to distance_assignment {(i, j) in pairs}:
    sum{v in V} e[i, j, v] = 1;

subject to distance_uniqueness {v in V}:
    sum {(i, j) in pairs} e[i, j, v] <= 1;

subject to distance_definition {(i, j) in pairs}:
    sum {v in V} v * e[i, j, v] = d[i, j];

subject to distance_identity {(i, j) in pairs_consecutive}:
    sum {k in i..j - 1} d[k, k + 1] = d[i, j];