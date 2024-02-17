#!/usr/bin/env python3

"""
{{docstring}}
"""

from uuid import UUID, uuid1
import numpy as np

from .edge import Edge



class HRectangle:
    """
        {{docstring}}
    """

    box_id: UUID
    edges: list[Edge]

    def __init__(self, edges: list[Edge]) -> None:
        """
            {{docstring}}
        """

        self.box_id = uuid1()
        self.edges = edges

    @property
    def size(self) -> float:
        """
            {{docstring}}
        """
        return np.prod([edge.len for edge in self.edges])
