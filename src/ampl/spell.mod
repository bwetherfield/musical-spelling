set ID;
set PITCHNUM;
set SHARP_OR_DOUB;

param EdgeWeight {ID, PITCHNUM, SHARP_OR_DOUB, ID, PITCHNUM, SHARP_OR_DOUB} >= 0, <= 100;

var Indicator {ID, PITCHNUM, SHARP_OR_DOUB} >= 0, <= 1;
var Edge {ID, PITCHNUM, SHARP_OR_DOUB, ID, PITCHNUM, SHARP_OR_DOUB} >= 0, <= 1;

minimize Total_Cost:
		sum {i1 in ID, p1 in PITCHNUM, s1 in SHARP_OR_DOUB, i2 in ID, p2 in PITCHNUM, s2 in SHARP_OR_DOUB}
				EdgeWeight[i1,p1,s1,i2,p2,s2] * Edge[i1,p1,s1,i2,p2,s2];

subject to Include1 {i1 in ID, p1 in PITCHNUM, s1 in SHARP_OR_DOUB, i2 in ID, p2 in PITCHNUM, s2 in SHARP_OR_DOUB}:
		Indicator[i1,p1,s1] - Idicator[i2,p2,s1] <= Edge[i1,p1,s1,i2,p2,s2];

subject to Include2 {i1 in ID, p1 in PITCHNUM, s1 in SHARP_OR_DOUB, i2 in ID, p2 in PITCHNUM, s2 in SHARP_OR_DOUB}:
		Indicator[i2,p2,s1] - Idicator[i1,p1,s1] <= Edge[i1,p1,s1,i2,p2,s2];
