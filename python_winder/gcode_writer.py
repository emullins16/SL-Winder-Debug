import os


class GCodeWriter:
    def __init__(self, filename: str):
        self.filename = filename

    def write(self, gcode: list[str]) -> None:
        dirpath = os.path.dirname(self.filename)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with open(self.filename, "w") as f:
            for line in gcode:
                f.write(line + "\n")
