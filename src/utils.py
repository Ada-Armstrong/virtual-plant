"""
Random utility classes and functions.
"""

class ValueRange:
    def __init__(self, minimum: int, maximum: int):
        self.minimum = minimum
        self.maximum = maximum

    def __contains__(self, item: int):
        return self.minimum <= item <= self.maximum

