// t021_bending_binary_vert.mss – Two nodes with a bending binary following a vertical path
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 1,1
    Pilot 3,1
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1.2 : -/1 r|Aircraft : +/1 r|Pilot : L2