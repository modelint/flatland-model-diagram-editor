// t036_2bend_tertiary_top.mss – Tertiary is left of a multiple bend connector
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 3,1
    Pilot 1,4
    Flight 4,3
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    -R1.3 : +/1 r|Aircraft : -/1 l|Pilot, b|Flight : L2 L2 L3R+1
