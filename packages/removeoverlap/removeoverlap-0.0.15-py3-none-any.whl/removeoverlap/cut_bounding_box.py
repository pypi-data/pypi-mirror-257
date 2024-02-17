#!/usr/bin/env python3

"""
{{docstring}}
"""

from copy import deepcopy

from .event_pool import EventPool
from .hrectangle import HRectangle


def cut_bounding_box(boxes: dict[str, HRectangle],
                     bounding_box: HRectangle,
                     event_pool: EventPool) -> tuple[HRectangle, HRectangle]:
    """
        {{docstring}}
    """

    x_coordinate: list[float] = []

    for box in boxes.values():
        x_coordinate.append(box.edges[event_pool.i_axis].start)
        x_coordinate.append(box.edges[event_pool.i_axis].end)

    bounding_box_start = bounding_box.edges[event_pool.i_axis].start
    bounding_box_end = bounding_box.edges[event_pool.i_axis].end

    intersecting_coordinates = [
        coordinate for coordinate in x_coordinate
        if coordinate not in (bounding_box_start, bounding_box_end)
    ]

    count = len(intersecting_coordinates)

    if count == 0:
        # this is will never be used in chan's algorithm since he remove all slabs
        # for us we may find a dimssion where all boxes are slabs
        event_pool.renumber_axes()
        return cut_bounding_box(boxes, bounding_box, event_pool)

    # sort here is just a quick way we can get it sorted using events
    intersecting_coordinates.sort()

    # midean and weighted midean are the same for us since it is the same weight for all coordinates
    m = 0 if count == 1 else round(count/2)

    x_m = intersecting_coordinates[m]

    lbounding_box = deepcopy(bounding_box)
    rbounding_box = deepcopy(bounding_box)
    lbounding_box.edges[event_pool.i_axis].end = x_m
    rbounding_box.edges[event_pool.i_axis].start = x_m

    event_pool.renumber_axes()
    return (lbounding_box, rbounding_box)
