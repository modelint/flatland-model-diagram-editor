"""
geometry_domain.py

A small library of 1D measurements that can be applied to the Canvas and Grid.
This makes it possible to apply the same type of logic to horizontal and vertical distances without
the need to differentiate between the two.

"""
from flatland.datatypes.geometry_types import Position
from typing import Set
scale = 2  # For float rounding errors (change to 3 or 4 if errors are visible on drawings)

def nearest_parallel_segment(psegs: Set[tuple], point: Position, ascending: bool) -> float:
    """
    Given a set of parallel segments a point and a +/- direction, find the segment that yields the
    shortest perpendicular segment in the indicated direction to the point. If the parallel segments
    are vertical, each will share the same x value, y otherwise. This shared value represents the segment
    axis. Distance from the axis to the point is relative to the corresponding coordinate. Thus the
    distance from the point's x coordinate is measured relative to each segment x if the segments are vertical.
    
    :param psegs: Set of parallel segments
    :param point: Find perpendicular segment to this point
    :param ascending: If true, each parallel segment axis is higher than the point x or y coordinate
    :return: x if vertical segs or or y if horizontal of closest intersecting parallel segment
    """
    s = list(psegs)[0]  # Select arbitary segment so we can determine axis orientation (they must all be the same)
    vertical_axis = (s[0].x == s[1].x)  # If two x's in a segment are the same, it's a vertical segmenet
    # Establish the axis and extend coordinates based on orientation
    # 0 and 1 are indices that match the x and y components of the Position tuple that defines each point
    axis_coord, extent_coord = (0,1) if vertical_axis else (1,0)  # So basically, swap 'x' and 'y' based on orientation
    if ascending:
        # Facing segs are those less than the point's axis coordinate (to the left or below the point)
        fsegs = [s for s in psegs if s[0][axis_coord] > point[axis_coord]]
    else:
        # Facing segs are greater (above or the right)  Remember we assume Cartesian coordinates throughout
        fsegs = [s for s in psegs if s[0][axis_coord] < point[axis_coord]]
    isegs = []  # Those segments that overlap the point along the axis (so that a normal segment will intersect)
    for s in fsegs:
        a, b = sorted([s[0][extent_coord], s[1][extent_coord]])  # Order all segment extents along axis low to high
        if a <= point[extent_coord] <= b:
            isegs.append(s)  # It's possible to intersect the point from this segment
    if ascending:  # Now select the closest axis value to the point
        axis_value = min({s[0][axis_coord] for s in isegs})
    else:
        axis_value = max({s[0][axis_coord] for s in isegs})
    return axis_value



def step_edge_distance(num_of_steps, extent, step):
    """
    You have a line segment with a given extent (length). In distance coordinates such as points, 0 is at the
    beginning of the segment increasing to the extent at the other end. A number line is defined with step
    increment 0 at the center of the line segment. Steps increase positively toward the extent and negatively toward
    the 0 coordinate. There is no step increment defined at either boundary (0 or the extent).

    Let's say the line segment is 100 pt long and we want 5 steps.  The zero step will be at coordinate 50.
    All negative steps will have a value less than 50 and all positive steps will be greater than 50.
    To make this work we divide the line segment into equally spaced increments by dividing the extent by the total
    number of steps plus one. With 5 steps then, we get 6 increments each 20 pt wide. There will be three on each
    side of the zero step. This means the number line will be -2, -1, 0, 1, 2 giving US our five step positions.

    Given a step number, return the distance coordinate. In our example, step 0 will return 50 pt.
    Step -1 will return 30 pt and so on. Note that no step will return either the extent or 0 pt since
    the whole idea is to avoid stepping to the edge of the line segment.

    :param num_of_steps: Line segment is divided into this number of steps
    :param extent: Length of line segment
    :param step: You want the distance of this step from the beginning of the line segment
    :return: Distance from edge of extent
    """
    # divide the face into equal size steps, 5 anchor positions = 6 steps
    stem_step_size = extent / (num_of_steps + 1)
    # add distance from center going away in either direction based on +/- anchor position
    return extent / 2 + step * stem_step_size


def expand_boundaries(boundaries, start_boundary, expansion):
    """Push boundaries out by exapnsion from starting boundary"""
    return boundaries[:start_boundary] + [b + expansion for b in boundaries[start_boundary:]]


def span(boundaries, from_grid_unit, to_grid_unit):
    """Returns the distance between two grid_unit"""
    assert to_grid_unit >= from_grid_unit > 0, "Grid unit number out of range"
    return boundaries[to_grid_unit] - boundaries[from_grid_unit - 1]


def align_on_axis(axis_alignment: int, boundaries, from_grid_unit, to_grid_unit, from_padding, to_padding,
                  node_extent) -> float:
    """Compute distance from from_boundary of the node edge (resulting in either a lower left x or y delta)

    Parameters
    ---
    axis_alignment: axis relative alignment of low:0, middle:1 or high:2 from vert/horiz align enums
    boundaries : an ascending list of grid boundaries on the x or y axis
    from_grid_unit : a row or column number
    to_grid_unit : a row or column number >= than the from number (must be on same axis as from_grid_unit)
    from_padding : the padding after the from bondary
    to_padding : the padding before the to boundary
    node_extent : drawn extent of the node placed in the cell without any padding
    """
    assert len(boundaries) > 1, "Empty grid"
    assert to_grid_unit >= from_grid_unit, "Grid units in wrong order?"
    assert to_padding >= 0, "Negative padding"
    assert from_padding >= 0, "Negative padding"
    assert node_extent > 0, "Missing node size"
    assert 0 <= axis_alignment <= 2

    cell_extent = boundaries[to_grid_unit] - boundaries[from_grid_unit - 1]
    leftover_space = round(cell_extent - from_padding - to_padding - node_extent, scale)
    if leftover_space:
        if axis_alignment == 1:  # middle alignment
            return cell_extent/2 - node_extent/2 + boundaries[from_grid_unit - 1]
        elif axis_alignment == 0:  # left or bottom alignment
            return boundaries[from_grid_unit - 1] + from_padding
        elif axis_alignment == 2:  # right or top alignment
            return boundaries[to_grid_unit] - node_extent - to_padding
    else:
        return from_padding + boundaries[from_grid_unit -1]


if __name__ == "__main__":
    segs = {
        (Position(1,0), Position(1,15)),
        (Position(5, 15), Position(5, 25)),
        (Position(10, 7), Position(10, 25)),
        (Position(12, 2), Position(12, 11)),
        (Position(13, 20), Position(13, 29)),
        (Position(20, 7), Position(20, 17)),
        (Position(25, 20), Position(25, 32)),
        (Position(30, 7), Position(30, 27)),
    }
    v = nearest_parallel_segment(psegs=segs, point=Position(15,17), ascending=False)
    print(v)