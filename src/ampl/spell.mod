set NODE_CLASSES;
set nodes {NODE_CLASSES} dimen 2;
set NODES = union {i in NODE_CLASSES} nodes[i];
set EDGES within {NODES, NODES};

param EdgeWeight {i in NODE_CLASSES, j in NODE_CLASSES} >= 0, <= 100;

var NodeState {NODES} >= 0;
var EdgeState {EDGES} >= 0;

minimize Total_Cost:
		sum {i in NODE_CLASSES, j in NODE_CLASSES, u in nodes[i], v in nodes[j]: u <> v} EdgeWeight[i,j] * EdgeState[u,v];

subject to StateTransfer {u in NODES, v in NODES: (u,v) in EDGES}:
		NodeState[v] - NodeState[u] <= EdgeState[u,v];
