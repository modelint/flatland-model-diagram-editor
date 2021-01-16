// t006_reverse_straight_binary_horiz.mss – Connector stems don't match model, reversed to test recovery
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
    // These two stems are in the reversed order with respect to the model file, should be Aircraft, Pilot
    -R1 : +/2 l*|Pilot : +/1 r|Aircraft