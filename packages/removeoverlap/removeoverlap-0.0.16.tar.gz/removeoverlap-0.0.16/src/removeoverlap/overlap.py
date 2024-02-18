#!/usr/bin/env python3

"""
{{docstring}}
"""

from itertools import combinations
from .edge import Edge
from .hrectangle import HRectangle


def edge_overlap(edge_a: Edge, edge_b: Edge) -> bool:
    """
        {{docstring}}
    """
    a_contain_b = edge_b.start >= edge_a.start and edge_b.end <= edge_a.end
    b_contain_a = edge_a.start >= edge_b.start and edge_a.end <= edge_b.end
    a_before_b = edge_a.start <= edge_b.start < edge_a.end
    b_before_a = edge_b.start <= edge_a.start < edge_b.end
    return a_contain_b or b_contain_a or a_before_b or b_before_a


def overlap(box_a: HRectangle, box_b: HRectangle) -> bool:
    """
        {{docstring}}
    """
    has_overlap = True

    for index, _ in enumerate(box_a.edges):
        if not edge_overlap(box_a.edges[index], box_b.edges[index]):
            has_overlap = False
            break

    return has_overlap


def list_has_overlap(boxes:HRectangle):
    """
        {{docstring}}
    """
    for box_a,box_b in combinations(boxes,2):

        if overlap(box_a,box_b):
            return True
    return False
