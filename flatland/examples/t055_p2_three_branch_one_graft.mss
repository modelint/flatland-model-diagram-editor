// t052_rbranch_vert_corner.mss – Vertical rut branch with a corner and two bends
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // Node placement examples
    // Aircraft 3,2     :: Node named "Aircraft" positioned at row 3, column 2
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 3,2
    Helicopter 1,1
    Fixed Wing 3,4
    Hybrid Wing 4,4
    X Wing 6,2
    Tie Fighter 5,1
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
    -R1 : b|Aircraft { t|Helicopter } { l|Fixed Wing : L3R-1 } { l|Hybrid Wing>, b|X Wing, b|Tie Fighter }