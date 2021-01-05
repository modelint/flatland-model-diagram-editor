// t035_2bend_tertiary_top.mss – Tertiary is right of a multiple bend connector
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 1,1
    Pilot 2,4
    Flight 3,4
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1.2 : +/1 t|Aircraft : -/1 l|Pilot, l|Flight : L3 L3 L2
