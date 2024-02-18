#!/usr/bin/env python3

"""
{{docstring}}
"""

from .hrectangle import HRectangle


def print_box_list(boxes: list[HRectangle]):
    """
        {{docstring}}
    """
    outtext = []
    for box in boxes:
        text = str.join(
            ',', [f'Edge({edge.start},{edge.end})' for edge in box.edges]
        )
        outtext.append(f'HRectangle([{text}])')

    print(str.join(',\n', outtext))
