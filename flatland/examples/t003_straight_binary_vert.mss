// t003_straight_binary_vert.mss – Two nodes and a single horizontal binary connector, 2-line wrap
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
    -R1 : +/1 t|Aircraft : +/2 b*|Pilot