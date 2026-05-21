class Machine:
    def __init__(
        self,
        lin_axis: str,
        rot_axis: str,
        units: str,
        feed_rate: float,
        lin_scale: float = 1.0,
        rot_scale: float = 1.0,
    ):
        self.lin_axis = lin_axis    # carriage axis label (e.g. "X")
        self.rot_axis = rot_axis    # mandrel axis label (e.g. "Z")
        self.units = units          # "in" or "mm"
        self.feed_rate = feed_rate  # in/min or mm/min
        self.lin_scale = lin_scale  # axis scaling (better handled in firmware)
        self.rot_scale = rot_scale
