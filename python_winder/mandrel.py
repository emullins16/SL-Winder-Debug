import math


class Mandrel:
    def __init__(self, diameter: float, length: float):
        self.diameter = diameter
        self.length = length

    def circumference(self) -> float:
        return math.pi * self.diameter
