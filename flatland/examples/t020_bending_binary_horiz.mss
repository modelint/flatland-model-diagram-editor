// t020_bending_binary_horiz.mss – Two nodes with a bending binary following a path
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 1,1
    Pilot 1,3
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1.2 : -/1 t|Aircraft : +/1 t|Pilot : L2R-1