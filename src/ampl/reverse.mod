set NODE_CLASSES;
set nodes {NODE_CLASSES};
set NODES = union {i in NODE_CLASSES} nodes[i];
set EDGES within {NODES, NODES};

param NodeState {NODES} >= 0, <= 1;
param EdgeState {u in NODES, v in NODES: (u,v) in EDGES} =
		if NodeState[u] = 0 and NodeState[v] = 1 then 1 else 0;

var Flow {EDGES} >= 0;
var Capacity {EDGES} >= 0, <= 100;

var Distance {EDGES, EDGES};
var Min_Distance;

maximize Diversity: Min_Distance;

subject to FlowSat {v in NODES}:
		sum {u in NODES: (u,v) in EDGES} Flow[u,v] - sum {w in NODES: (v,w) in EDGES} Flow[v,w];

subject to CapacitySat {e in EDGES}:
		Flow[e] <= Capacity[e];

subject to ComplementarySlackness1 {e in EDGES}:
		EdgeState[e] * (Capacity[e] - Flow[e]) = 0;

subject to ComplementarySlackness2 {u in NODES, v in NODES: (u,v) in EDGES}:
		Flow[u,v] * (NodeState[v] - NodeState[u] + EdgeState[u,v]) = 0;

subject to Distance1 {e in EDGES, f in EDGES: e <> f}:
		Distance[e,f] >= Capacity[e] - Capacity[f];

subject to Distance2 {e in EDGES, f in EDGES: e <> f}:
		Distance[e,f] >= Capacity[f] - Capacity[e];

subject to Bound_Distance {e in EDGES, f in EDGES: e <> f}:
		Min_Distance <= Distance[e,f]
