#!/usr/bin/env python3

"""
{{docstring}}
"""

from .cut_bounding_box import cut_bounding_box
from .event_pool import EventPool
from .hrectangle import HRectangle
from .split_boxes import split_boxes


def simplify(boxes: dict[str, HRectangle],
             bounding_box: HRectangle,
             event_pool: EventPool) -> tuple[dict[str, HRectangle], list[HRectangle], HRectangle]:
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
                non_covered_axes_count = non_covered_axes_count + 1
                non_covered_axis = axis

        if non_covered_axes_count == 0:
            # box is covering all axes therefore remove all boxes
            return ({}, [bounding_box], bounding_box)

        if non_covered_axes_count == 1:
            edge = box.edges[non_covered_axis]
            bounding_box_edge = bounding_box.edges[non_covered_axis]

            if bounding_box_edge.start == edge.start or bounding_box_edge.end == edge.end:
                # box is a adjacent slab
                del boxes[box.box_id]
                event_pool.mark_adjacent_slab(non_covered_axis, box.box_id)
            else:
                event_pool.mark_slab(non_covered_axis, box.box_id)

    return event_pool.remove_adjacent_slabs(bounding_box, boxes)


def remove_overlap(boxes: dict[str, HRectangle],
                   bounding_box: HRectangle,
                   event_pool: EventPool) -> list[HRectangle]:
    """
        {{docstring}}
    """

    if len(boxes) == 0:
        return []

    if len(boxes) == 1:
        return boxes.values()

    # new_bounding_box maybe be shrinked
    (new_boxes, slabs, new_bounding_box) = simplify(
        boxes, bounding_box, event_pool)

    if len(new_boxes.values()) == 0:
        return slabs
    if len(new_boxes.values()) == 1:
        return slabs + list(new_boxes.values())

    (lbbox, rbbox) = cut_bounding_box(new_boxes, new_bounding_box, event_pool)

    (left, right) = split_boxes(new_boxes, lbbox, rbbox, event_pool)

    (lboxes, levent_pool) = left
    (rboxes, revent_pool) = right

    output_boxes = slabs

    output_boxes += remove_overlap(rboxes, rbbox, revent_pool)
    output_boxes += remove_overlap(lboxes, lbbox, levent_pool)

    return output_boxes
