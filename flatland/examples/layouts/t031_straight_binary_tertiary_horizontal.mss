// t031_straight_binary_tertiary_horizontal.mss
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 3,1
    Pilot 1,1
    Flight 2,2
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    -R1 : +/1 b|Aircraft : +/1 t*|Pilot, l|Flight