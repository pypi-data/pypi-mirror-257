#!/usr/bin/env python3

"""
{{docstring}}
"""

from .event_type import EventType


class Event:
    """
        {{docstring}}
    """
    box_id: str
    coordinate: float
    is_slab: bool
    is_adjacent_slab: bool
    type: EventType

    def __init__(self,
                 box_id: str,
                 coordinate: float,
                 is_slab: bool,
                 is_adjacent_slab: bool,
                 event_type: EventType) -> None:
        self.box_id = box_id
        self.coordinate = coordinate
        self.is_slab = is_slab
        self.is_adjacent_slab = is_adjacent_slab
        self.type = event_type

    @property
    def key(self) -> str:
        """
            {{docstring}}
        """
        return f"{str(self.box_id)}{self.coordinate}"
