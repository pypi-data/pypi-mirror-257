#!/usr/bin/env python3

"""
{{docstring}}
"""

from copy import deepcopy
import random

from pytictoc import TicToc
from removeoverlap import measure
from removeoverlap import Edge
from removeoverlap import EventPool

from removeoverlap import HRectangle
from removeoverlap import remove_overlap
from removeoverlap import list_has_overlap


MIN_EDGE_LENGHTH = 5
RANGE_START = 0
RANGE_END = 100

MAX_DIMENSION_COUNT = 10
MIN_DIMENSION_COUNT = 2

MIN_BOX_COUNT = 2
MAX_BOX_COUNT = 15


def create_edge(start_range: float, end_range: float, gap: int):
    """
    return an edge with in a range
    """
    if start_range == (end_range - gap):
        start = start_range
    else:
        start = random.uniform(start_range, end_range - gap)
    if end_range == start + gap:
        end = end_range
    else:
        end = random.uniform(start + gap, end_range)

    return Edge(start, end)


def create_bound_box(dimssion_count: int):
    """
    return a boundbox with randomly created edges
    """
    edges = []
    for _ in range(dimssion_count):
        edge = create_edge(RANGE_START, RANGE_END, MIN_EDGE_LENGHTH + 1)
        edges.append(edge)

    return HRectangle(edges)


def create_box(bounding_box: HRectangle):
    """
    return a boundbox with randomly created edges
    """
    edges = []
    for edge in bounding_box.edges:
        edges.append(create_edge(edge.start, edge.end, MIN_EDGE_LENGHTH))

    return HRectangle(edges)


def create_boxes(count: int, bounding_box: HRectangle) -> list[HRectangle]:
    """
    return a boundbox with randomly created edges
    """
    boxes = []
    for _ in range(count):
        boxes.append(create_box(bounding_box))

    return boxes


def create_test_data():
    """
        Creat
    """
    configuration = []
    for dimssion_count in range(MIN_DIMENSION_COUNT, MAX_DIMENSION_COUNT + 1):
        bounding_box = create_bound_box(dimssion_count)
        for box_count in range(MIN_BOX_COUNT, MAX_BOX_COUNT + 1):
            boxes_list = create_boxes(box_count, bounding_box)
            config = {}
            config['bounding_box'] = bounding_box
            config['box_list'] = boxes_list
            config['box_count'] = box_count
            config['dimssion_count'] = dimssion_count
            configuration.append(config)

    return configuration


def get_size(boxes: list[HRectangle]):
    """
        {{docstring}}
    """
    size = 0
    for box in boxes:
        size = size + box.size
    return size


def compare():
    """
    {{docstring}}
    """
    configuration = create_test_data()
    time = TicToc()
    for config in configuration:
        boxes_list = config['box_list']
        box_count = config['box_count']
        dimssion_count = config['dimssion_count']

        boxes = {box.box_id: box for box in boxes_list}
        event_pool = EventPool(boxes)
        bounding_box = config['bounding_box']

        chan_boxes = deepcopy(boxes)
        chan_event_pool = deepcopy(event_pool)
        chan_bounding_box = deepcopy(bounding_box)
        # read size before change
        bb_size = chan_bounding_box.size

        time.tic()
        disjoint_boxes = remove_overlap(boxes, bounding_box, event_pool)
        remove_overlap_time = time.tocvalue(True)

        time.tic()
        complement_size = measure(
            chan_boxes,
            chan_bounding_box,
            chan_event_pool
        )
        chan_time = time.tocvalue(True)

        disjoint_boxes_size = format(get_size(disjoint_boxes), ".2f")
        unoin_size = format(bb_size - complement_size, ".2f")

        print(f"""
                Equal : {disjoint_boxes_size == unoin_size}
                Overlap : {list_has_overlap(disjoint_boxes)} 
                Chan Volume : {unoin_size} 
                Our Volume : {disjoint_boxes_size} 
                Box count : {box_count} 
                Fragments : {len(disjoint_boxes)}
                Dimssion count : {dimssion_count}
                Our time : {remove_overlap_time}
                Chan time : {chan_time}
        """)
        print('------------------------------------')


compare()
