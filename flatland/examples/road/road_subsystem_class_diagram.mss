// Road Class Diagram
diagram class
notation Starr
presentation default
orientation landscape
sheet D
padding 130 230 10 10 // left, bottom, top, right diagram padding between canvas margin to avoid frame overlap
frame TRI Engineer
frame_presentation default
nodes
    Traffic Territory 1,1
    Country 1,3
    Road Map Specification 3,1
    Known Map Road 3,2
    Road 3,3
    Soft Division Transition 4,3
    Hard Division Transition 5,3
    Barrier Type 5,2
    Division Transition 4-5,5
    Lane Division_2 1,5
    Start of Lane 7-8,9
    End of Lane 6-7,9
    Lane 7,11
    Road Edge 1,7
    Left Road Edge/2 2,
    Right Road Edge/2
    Lateral Lane Boundary 7,3
connectors
    +R30 : r-2|Traffic Territory : l*|Country
    +R31 : t|Traffic Territory : b*|Road Map Specification
    +R32 : r|Road Map Specification : l*|Road, t|Known Map Road
