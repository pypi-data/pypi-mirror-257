#!/usr/bin/env python3

"""
{{docstring}}
"""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from .hrectangle import HRectangle


def plot_on_axes(boxes: dict[str, HRectangle],
                 bounding_box: HRectangle,
                 axis: plt.Axes,
                 ax1: int,
                 ax2: int):
    """
        {{docstring}}
    """

    axis.add_patch(Rectangle((bounding_box.edges[ax1].start,
                              bounding_box.edges[ax2].start),
                             bounding_box.edges[ax1].len,
                             bounding_box.edges[ax2].len,
                             facecolor='green'
                             ))

    for box in list(boxes.values()):
        axis.add_patch(Rectangle(
            (box.edges[ax1].start,
             box.edges[ax2].start),
            box.edges[ax1].len,
            box.edges[ax2].len,
            facecolor='none',
            edgecolor='red',
            lw=3)
        )



def plot_boxes(boxes: dict[str, HRectangle], bounding_box: HRectangle):
    """
        {{docstring}}
    """
    _, axes = plt.subplots()

    axes.plot([0, 20], [0, 20])

    plot_on_axes(boxes, bounding_box,  axes, 0, 1)

    plt.show()
