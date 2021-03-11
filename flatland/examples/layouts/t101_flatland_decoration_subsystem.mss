// t100_flatland_node_subsystem.mss
diagram class
notation Starr
presentation default
orientation landscape
sheet tabloid
padding 130 230 10 10 // left, bottom, top, right diagram padding between canvas margin to avoid frame overlap
frame OS Engineer
frame_presentation default
nodes
    Decoration 6,2
    Label 4,1
    Symbol 4,3
    Compound Symbol 2-3,2-3
    Simple Symbol 2-3,5
    Symbol Stack Placement 1-2,4
    Arrow Symbol 3,7 >left
    Circle Symbol 2,7 >left
    Cross Symbol 1,7 >left
connectors
    +R104 : b|Decoration { t|Label, t|Symbol }
    +R103 : b|Symbol { t|Compound Symbol, t|Simple Symbol }
    -R100 : r|Simple Symbol { l|Arrow Symbol, l|Circle Symbol, l|Cross Symbol }
    +R101 : +/1 r|Compound Symbol : +/1 l*|Simple Symbol, t|Symbol Stack Placement