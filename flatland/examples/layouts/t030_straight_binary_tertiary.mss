// t030_straight_binary_tertiary.mss – Horizontal straight with tertiary above
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 1,1
    Pilot 1,3
    Flight 2,2
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    -R1 : +/1 r|Aircraft : +/1 l*|Pilot, b|Flight