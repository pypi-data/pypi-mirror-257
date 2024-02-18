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
    name: str

    def __init__(self, start: float, end: float, name:str = '') -> None:
        """
            {{docstring}}
        """
        self.start = start
        self.end = end
        self.name = name

    @property
    def len(self) -> float:
        """
            {{docstring}}
        """
        return self.end - self.start
