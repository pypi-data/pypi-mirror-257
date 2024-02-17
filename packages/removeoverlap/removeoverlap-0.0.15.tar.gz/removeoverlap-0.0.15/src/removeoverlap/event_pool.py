#!/usr/bin/env python3

"""
{{docstring}}
"""


from copy import deepcopy

from removeoverlap.edge import Edge
from .event import Event
from .event_type import EventType
from .hrectangle import HRectangle


class EventPool:
    """
        {{docstring}}
    """
    dimension_count: int
    events: list[list[Event]]
    coordinate_to_event: list[dict[str, int]]
    i_axis: int
    j_axis: int

    def __init__(self, boxes: dict[str, HRectangle]) -> None:
        """
            {{docstring}}
        """

        self.dimension_count = len(list(boxes.values())[0].edges)
        self.events = [[]] * self.dimension_count
        self.coordinate_to_event = [{}] * self.dimension_count

        for axis_index in range(self.dimension_count):
            axis_events: list[Event] = []
            for box in boxes.values():
                start = box.edges[axis_index].start
                end = box.edges[axis_index].end
                start_event = Event(box.box_id, start, False,
                                    False, EventType.START)
                end_event = Event(box.box_id, end, False, False, EventType.END)
                axis_events.append(start_event)
                axis_events.append(end_event)

            axis_events.sort(key=lambda x: x.coordinate)
            self.events[axis_index] = axis_events
            self.build_dict(axis_index)

        self.i_axis = 0
        self.j_axis = 1

    @property
    def count(self) -> int:
        """
            {{docstring}}
        """
        return len(self.events)

    def build_dict(self, axis_index: int):
        """
            {{docstring}}
        """
        axes_events = self.events[axis_index]
        # use box index for duplicated values
        self.coordinate_to_event[axis_index] = {
            self.event_key(value.box_id, value.type): index for index,
            value in enumerate(axes_events)
        }

    def event_key(self, box_id: str, event_type: EventType):
        """
            {{docstring}}
        """
        return f"{box_id}{event_type.value}"

    def get_event(self, axis_index: int, box_id: str, event_type: EventType) -> Event:
        """
            {{docstring}}
        """
        index = self.get_event_index(axis_index, box_id, event_type)
        return self.events[axis_index][index]

    def get_event_index(self, axis_index: int, box_id: str, event_type: EventType) -> Event:
        """
            {{docstring}}
        """
        event_key = self.event_key(box_id, event_type)

        return self.coordinate_to_event[axis_index][event_key]

    def mark_slab(self, axis_index: int, box_id: str) -> None:
        """
            {{docstring}}
        """
        start_event = self.get_event(axis_index, box_id, EventType.START)
        end_event = self.get_event(axis_index, box_id, EventType.END)

        start_event.is_slab = True
        end_event.is_slab = True

    def mark_adjacent_slab(self, axis_index: int, box_id: str) -> None:
        """
            {{docstring}}
        """
        start_event = self.get_event(axis_index, box_id, EventType.START)
        end_event = self.get_event(axis_index, box_id, EventType.END)

        start_event.is_adjacent_slab = True
        end_event.is_adjacent_slab = True

    def renumber_axes(self):
        """
            {{docstring}}
        """
        self.j_axis = self.i_axis
        self.i_axis = self.dimension_count - 1 if self.i_axis == 0 else self.i_axis - 1

    def shrink(self, bounding_box: HRectangle):
        """
            {{docstring}}
        """
        for axis_index in range(self.dimension_count):

            start = bounding_box.edges[axis_index].start
            end = bounding_box.edges[axis_index].end

            # filter events by bounding box
            self.events[axis_index] = [
                value for value in self.events[axis_index]
                # just to avoid float errors
                if start - 1 <= value.coordinate <= end + 1
            ]

            # rebuild dictionary after event indexs changed
            self.build_dict(axis_index)

    def update_event_index(self, axis_index: int, event: Event, event_index: int) -> None:
        """
            {{docstring}}
        """
        axix_dict = self.coordinate_to_event[axis_index]
        key = self.event_key(event.box_id, event.type)
        axix_dict[key] = event_index

    def update_box_events(self,
                          box: HRectangle,
                          bbox: HRectangle) -> bool:
        """
            {{docstring}}
        """

        for axis_index in range(self.dimension_count):
            bedge = box.edges[axis_index]
            bbedge = bbox.edges[axis_index]

            start_event = self.get_event(
                axis_index, box.box_id, EventType.START
            )

            end_event = self.get_event(
                axis_index, box.box_id, EventType.END
            )

            new_start = max(bbedge.start, bedge.start)
            new_end = min(bbedge.end, bedge.end)

            start_event.coordinate = new_start
            end_event.coordinate = new_end

            # update box coordinates too
            bedge.start = new_start
            bedge.end = new_end

    def remove_slabs(self,
                     bounding_box: HRectangle,
                     boxes: dict[str, HRectangle]
                     ) -> tuple[dict[str, HRectangle], HRectangle]:
        """
            {{docstring}}
        """

        for axis_index, axis_events in enumerate(self.events):

            value_to_remove = 0
            events_to_remove: list[int] = []
            last_coordinate = 0
            opened = 0

            for event_index, event in enumerate(axis_events):
                if opened > 0:
                    value_to_remove += event.coordinate - last_coordinate

                last_coordinate = event.coordinate

                if event.is_slab:
                    opened += 1 if event.type == EventType.START else -1
                    events_to_remove.append(event_index)
                # events of a deleted box on other axis not marked as slabs
                elif event.box_id not in boxes:
                    events_to_remove.append(event_index)
                elif value_to_remove > 0:
                    event.coordinate -= value_to_remove
                    box_edge = boxes[event.box_id].edges[axis_index]

                    if event.type == EventType.END:
                        boxes[event.box_id].edges[axis_index].end = event.coordinate
                    else:
                        boxes[event.box_id].edges[axis_index].start = event.coordinate
                        # keep track of start event so we can delete after
                        self.update_event_index(axis_index, event, event_index)

                    if box_edge.end == box_edge.start:
                        start_event_index = self.get_event_index(
                            axis_index, event.box_id, EventType.START
                        )
                        events_to_remove.append(event_index)
                        events_to_remove.append(start_event_index)
                        # box is covered by slabs
                        del boxes[event.box_id]

            # complexity of sorting is ignored
            for event_index in sorted(events_to_remove, reverse=True):
                del axis_events[event_index]

            bounding_box.edges[axis_index].end -= value_to_remove
            self.build_dict(axis_index)

        return (boxes, bounding_box)

    def remove_adjacent_slabs(self,
                              bounding_box: HRectangle,
                              boxes: dict[str, HRectangle]
                              ) -> tuple[dict[str, HRectangle], list[HRectangle], HRectangle]:
        """
            {{docstring}}
        """

        slabs = []
        for axis_index, axis_events in enumerate(self.events):

            bounding_box_edge = bounding_box.edges[axis_index]

            adjacent_slabs_end_events = [
                event.coordinate
                for event in axis_events
                if event.type == EventType.END and
                event.is_adjacent_slab and
                event.coordinate < bounding_box_edge.end
            ]

            adjacent_slabs_start_events = [
                event.coordinate
                for event in axis_events
                if event.type == EventType.START and
                event.is_adjacent_slab and
                event.coordinate > bounding_box_edge.start
            ]

            max_adjacent_end = max(
                adjacent_slabs_end_events, default=bounding_box_edge.start
            )
            min_adjacent_start = min(
                adjacent_slabs_start_events, default=bounding_box_edge.end
            )

            slabs_end_events = [
                boxes[event.box_id].edges[axis_index].end
                for event in axis_events
                if event.box_id in boxes and
                event.type == EventType.START and
                event.is_slab and
                event.coordinate <= max_adjacent_end
            ]

            slabs_start_events = [
                boxes[event.box_id].edges[axis_index].start
                for event in axis_events
                if event.box_id in boxes and
                event.type == EventType.END and
                event.is_slab and
                event.coordinate >= min_adjacent_start
            ]

            max_slabs_end = max(
                slabs_end_events, default=bounding_box_edge.start
            )

            min_slabs_start = min(
                slabs_start_events, default=bounding_box_edge.end
            )

            max_end = max(max_adjacent_end, max_slabs_end)
            min_start = min(min_adjacent_start, min_slabs_start)

            # slabs are covering the bounding box
            if min_start <= max_end:
                # don't forget to return slabs too
                return ({}, slabs + [bounding_box], bounding_box)

            if min_start < bounding_box_edge.end:
                bottom_slab = deepcopy(bounding_box)
                bottom_slab.edges[axis_index].start = min_start
                slabs.append(bottom_slab)
                # shrink bounding box
                bounding_box_edge.end = min_start

            if max_end > bounding_box_edge.start:
                top_slab = deepcopy(bounding_box)
                top_slab.edges[axis_index].end = max_end
                slabs.append(top_slab)
                # shrink bounding box
                bounding_box_edge.start = max_end

            for box in list(boxes.values()):
                box_edge = box.edges[axis_index]
                box_edge.start = max(box_edge.start, max_end)
                box_edge.end = min(box_edge.end, min_start)

                if box_edge.start >= box_edge.end:
                    del boxes[box.box_id]

            self.build_dict(axis_index)

        return (boxes, slabs, bounding_box)



    def get_intial_bounding_box(self) -> HRectangle:
        """
            {{docstring}}
        """
        edges = []

        for axis_events in self.events:
            edges.append(
               Edge(axis_events[0].coordinate,axis_events[-1].coordinate)
            )

        return HRectangle(edges)
