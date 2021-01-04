// t040_ibranch_horiz.mss – Horizontal interpolated branch
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 3,2
    Helicopter 1,1
    Fixed Wing 1,3
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    +R1 : b|Aircraft { t|Helicopter, t+1|Fixed Wing }
