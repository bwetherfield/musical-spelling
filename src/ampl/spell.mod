set NODE_CLASSES;
set node {NODE_CLASSES};
set NODES = union {p in NODE_CLASSES} node[p];
set EDGES within {NODES, NODES}

param EdgeWeight {p in NODE_CLASSES, q in NODE_CLASSES} >= 0, <= 100;
param BigM;

var NodeState {NODES} >= 0, <= 1;
var EdgeState {EDGES} >= 0, <= 1;

minimize Total_Cost:
		sum {p in NODE_CLASSES, q in NODE_CLASSES, i in node[p], j in node[q]: i <> j} EdgeWeight[p,q] * EdgeState[i,j];

subject to StateTransfer {i in NODES, j in NODES: (i,j) in EDGES}:
		NodeState[j] - NodeState[i] <= EdgeState[i,j];
