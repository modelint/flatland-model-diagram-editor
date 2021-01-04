// t056_p3_single_branch_graft_float.mss – Pattern 3
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // Node placement examples
    // Aircraft 3,2     :: Node named "Aircraft" positioned at row 3, column 2
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 4,2
    Helicopter 3,1
    Fixed Wing 1,2
    Hybrid Wing 1,3
    X Wing 5,3
    Tie Fighter 3,4
connectors
    // Binary connector examples:
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    //
    // Trunk connector examples:
    //
    // +R1 : b|Aircraft { t|Helicopter, t|Fixed Wing : L1R-2 } { l|Hybrid Wing : L3 }
    // Connector name R1 on right side, node named "Aircraft" is the trunk node connecting from bottom face center
    // first branch: two nodes connected on center top faces with branch running through lane 1, rut -2
    // second branch: one node connected on center left face with branch running through lane 3 center
    //
    -R1 : b|Aircraft { r|Helicopter>, t|Fixed Wing, t|Hybrid Wing, b+1|X Wing, l*|Tie Fighter }