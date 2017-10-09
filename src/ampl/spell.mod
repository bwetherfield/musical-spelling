set NODE_CLASSES;
set node {NODE_CLASSES};
set NODES = union {i in NODE_CLASSES} node[i];
set EDGES within {NODES, NODES};

param EdgeWeight {i in NODE_CLASSES, j in NODE_CLASSES} >= 0, <= 100;

var NodeState {NODES} >= 0;
var EdgeState {EDGES} >= 0;

minimize Total_Cost:
		sum {i in NODE_CLASSES, j in NODE_CLASSES, u in node[i], v in node[j]: u <> v} EdgeWeight[i,j] * EdgeState[u,v];

subject to StateTransfer {u in NODES, v in NODES: (u,v) in EDGES}:
		NodeState[v] - NodeState[u] <= EdgeState[u,v];
