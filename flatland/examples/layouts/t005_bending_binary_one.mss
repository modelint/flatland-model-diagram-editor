// t005_bending_binary_one.mss – Two nodes with a bending binary bending once
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 4,1
    Pilot 3,3
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1.2 : -/1 b|Aircraft : +/1 l|Pilot