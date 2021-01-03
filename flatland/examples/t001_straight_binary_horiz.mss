// t001_straight_binary_horiz.mss – Two nodes and a single horizontal binary connector, 2-line wrap
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
    -R1 : +/1 r|Aircraft : +/2 l*|Pilot