// t023_bending_binary_twice.mss – Two nodes with a binary connector following a path with two bends
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 1,1
    Pilot 2,4
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1.2 : +/1 t|Aircraft : +/1 l|Pilot : L3R-2 L3