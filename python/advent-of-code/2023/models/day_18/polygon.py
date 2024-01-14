
def count_edges_above_pt(edges, pt):
    edge_count = 0
    for edge in edges:
        if pt_is_under_edge(pt, edge):
            edge_count += 1
    return edge_count


def count_edges_below_pt(edges, pt):
    edge_count = 0
    for edge in edges:
        if pt_is_above_edge(pt, edge):
            edge_count += 1
    return edge_count


def count_edges_left_of_pt(edges, pt):
    edge_count = 0
    for edge in edges:
        if pt_is_right_of_edge(pt, edge):
            edge_count += 1
    return edge_count


def count_edges_right_of_pt(edges, pt):
    edge_count = 0
    for edge in edges:
        if pt_is_left_of_edge(pt, edge):
            edge_count += 1
    return edge_count


def pt_is_above_edge(pt, edge):
    x, y = pt
    pt1, pt2 = edge
    e1x, e1y = pt1
    e2x, _ = pt2

    # Much faster than: min_x, max_x = sorted([e1x, e2x])
    min_x, max_x = (e1x, e2x) if e1x < e2x else (e2x, e1x)

    between_xs = min_x <= x <= max_x
    above_edge = y < e1y
    return between_xs and above_edge


def pt_is_under_edge(pt, edge):
    x, y = pt
    pt1, pt2 = edge
    e1x, e1y = pt1
    e2x, _ = pt2
    min_x, max_x = (e1x, e2x) if e1x < e2x else (e2x, e1x)

    between_xs = min_x <= x <= max_x
    under_edge = y > e1y
    return between_xs and under_edge


def pt_is_right_of_edge(pt, edge):
    x, y = pt
    pt1, pt2 = edge
    e1x, e1y = pt1
    _, e2y = pt2
    min_y, max_y = (e1y, e2y) if e1y < e2y else (e2y, e1y)

    between_ys = min_y <= y <= max_y
    right_of_edge = x > e1x
    return between_ys and right_of_edge


def pt_is_left_of_edge(pt, edge):
    x, y = pt
    pt1, pt2 = edge
    e1x, e1y = pt1
    _, e2y = pt2
    min_y, max_y = (e1y, e2y) if e1y < e2y else (e2y, e1y)

    between_ys = min_y <= y <= max_y
    left_of_edge = x < e1x
    return between_ys and left_of_edge
