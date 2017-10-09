set NODE_CLASSES;
set node {NODE_CLASSES};
set NODES = union {p in NODE_CLASSES} node[p];
set EDGES within {NODES, NODES}

param NodeState {NODES} >= 0, <= 1;
param EdgeState {i in NODES, j in NODES: (i,j) in EDGES} = NodeState[j] - NodeState[i];
