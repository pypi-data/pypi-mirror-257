#!/usr/bin/env python3

"""
{{docstring}}
"""



class Edge:
    """
        {{docstring}}
    """

    start: float
    end: float

    def __init__(self, start: float, end: float) -> None:
        """
            {{docstring}}
        """
        self.start = start
        self.end = end

    @property
    def len(self) -> float:
        """
            {{docstring}}
        """
        return self.end - self.start
