#!/usr/bin/env python3

"""
{{docstring}}
"""

from .event_pool import EventPool
from .hrectangle import HRectangle
from .cut_bounding_box import cut_bounding_box
from .split_boxes import split_boxes


def simplify(boxes: dict[str, HRectangle],
             bounding_box: HRectangle,
             event_pool: EventPool) -> tuple[HRectangle, dict[str, HRectangle]]:
    """
        {{docstring}}
    """

    for box in list(boxes.values()):

        non_covered_axes_count: int = 0
        non_covered_axis: int = -1

        for axis, edge in enumerate(box.edges):

            diffrent_start = edge.start != bounding_box.edges[axis].start
            diffrent_end = edge.end != bounding_box.edges[axis].end

            if diffrent_start or diffrent_end:
                non_covered_axes_count += 1
                non_covered_axis = axis

        if non_covered_axes_count == 0:
            # box is covering all axes therefore remove all boxes
            # return the box so bounding_box.size - box.size = 0
            return ({box.box_id: box}, bounding_box)

        if non_covered_axes_count == 1:
            # box is a slab
            del boxes[box.box_id]
            edge = box.edges[non_covered_axis]
            event_pool.mark_slab(non_covered_axis, box.box_id)

    return event_pool.remove_slabs(bounding_box, boxes)


def measure(boxes: dict[str, HRectangle],
            bounding_box: HRectangle,
            event_pool: EventPool) -> int:
    """
        {{docstring}}
    """

    if len(boxes) == 0:
        return bounding_box.size
    if len(boxes) == 1:
        return bounding_box.size - list(boxes.values())[0].size

    (boxes, bounding_box) = simplify(boxes, bounding_box, event_pool)

    if len(boxes) == 0:
        return bounding_box.size
    if len(boxes) == 1:
        return bounding_box.size - list(boxes.values())[0].size

    (lbbox, rbbox) = cut_bounding_box(boxes, bounding_box, event_pool)

    (left, right) = split_boxes(boxes, lbbox, rbbox, event_pool)
    (lboxes, levent_pool) = left
    (rboxes, revent_pool) = right

    left_size = measure(lboxes, lbbox, levent_pool)
    right_size = measure(rboxes, rbbox, revent_pool)

    return left_size + right_size
