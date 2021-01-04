// t053_p1_rbranch_vertical.mss – Pattern 1: Vertical Rut Branch
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // Node placement examples
    // Aircraft 3,2     :: Node named "Aircraft" positioned at row 3, column 2
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 2,1
    Helicopter 3,3
    Fixed Wing 1,3
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
    -R1 : r|Aircraft { l-2|Helicopter, l|Fixed Wing : L2R+1 }