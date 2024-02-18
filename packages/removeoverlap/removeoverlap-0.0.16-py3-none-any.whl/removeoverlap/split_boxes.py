
#!/usr/bin/env python3

"""
{{docstring}}
"""

from copy import deepcopy
from .event_pool import EventPool
from .hrectangle import HRectangle
from .overlap import overlap


def split_boxes(boxes: dict[str, HRectangle],
                lbbox: HRectangle,
                rbbox: HRectangle,
                event_pool: EventPool
                ) -> tuple[tuple[dict[str, HRectangle], EventPool]]:
    """
        {{docstring}}
    """
    lboxes: dict[str, HRectangle] = {}
    rboxes: dict[str, HRectangle] = {}

    levent_pool = deepcopy(event_pool)
    revent_pool = deepcopy(event_pool)
    for box in boxes.values():

        if overlap(box, lbbox) and overlap(box, rbbox):
            lbox: HRectangle = deepcopy(box)
            rbox: HRectangle = deepcopy(box)

            lboxes[lbox.box_id] = lbox
            levent_pool.update_box_events(lbox, lbbox)

            rboxes[rbox.box_id] = rbox
            revent_pool.update_box_events(rbox, rbbox)

        elif overlap(box, lbbox):
            lboxes[box.box_id] = box
            levent_pool.update_box_events(box, lbbox)
        elif overlap(box, rbbox):
            rboxes[box.box_id] = box
            revent_pool.update_box_events(box, rbbox)

    # remove events that are outside range
    levent_pool.shrink(lbbox)
    revent_pool.shrink(rbbox)

    left = (lboxes, levent_pool)
    right = (rboxes, revent_pool)
    return (left, right)
