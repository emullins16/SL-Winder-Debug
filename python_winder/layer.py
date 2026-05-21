class Layer:
    def __init__(self, angle: float, passes: int, layer_type: str = "helical"):
        self.angle = angle        # winding angle in degrees
        self.passes = passes      # number of passes
        self.type = layer_type
