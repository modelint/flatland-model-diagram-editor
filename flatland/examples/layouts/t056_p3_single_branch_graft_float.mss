// t056_p3_single_branch_graft_float.mss – Pattern 3
diagram class
notation Starr
presentation default
orientation landscape
sheet letter
nodes
    Aircraft 4,2
    Helicopter 3,1
    Fixed Wing 1,2
    Hybrid Wing 1,3
    X Wing 5,3
    Tie Fighter 3,4
connectors
    -R1 : b|Aircraft { r|Helicopter>, t|Fixed Wing, t|Hybrid Wing, b+1|X Wing, l*|Tie Fighter }