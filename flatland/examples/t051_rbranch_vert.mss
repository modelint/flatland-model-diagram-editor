// t051_rbranch_vert.mss – Vertical rut branch
diagram class
notation Starr
presentation diagnostic
orientation landscape
sheet letter
nodes
    // node [wrap] row,col align [ right | left ] [top | bottom]
    Aircraft 2,1
    Helicopter 3,4
    Fixed Wing 1,4
connectors
    // <side><connector name>[>bend] : <side><lines> <face><anchor>|<node> : <side><lines> <face><anchor>|<node>
    -R1 : r|Aircraft { l|Helicopter, l|Fixed Wing : L3R+1 }
