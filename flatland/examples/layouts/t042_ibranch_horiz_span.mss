// t040_ibranch_horiz.mss – Horizontal interpolated branch with spanning tree node
diagram class
notation Starr
presentation default
orientation landscape
sheet letter
nodes
    Aircraft 3,1-2
    Helicopter 1,1
    Fixed Wing 1,2
connectors
    +R1 : b|Aircraft { t|Helicopter, t+1|Fixed Wing }
