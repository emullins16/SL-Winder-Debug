import math
from machine import Machine
from mandrel import Mandrel
from layer import Layer


class WinderJob:
    def __init__(self, machine: Machine, mandrel: Mandrel):
        self.machine = machine
        self.mandrel = mandrel
        self.layers: list[Layer] = []

    def add_layer(self, angle: float, passes: int) -> None:
        self.layers.append(Layer(angle, passes, "helical"))

    def add_hoop_layer(self, passes: int) -> None:
        self.layers.append(Layer(90, passes, "hoop"))

    def generate_gcode(self) -> list[str]:
        gcode = []

        if self.machine.units == "in":
            gcode.append("G20 ; units in inches")
        else:
            gcode.append("G21 ; units in mm")

        gcode.append("G90 ; absolute positioning")
        gcode.append(
            f"G92 {self.machine.lin_axis}0 {self.machine.rot_axis}0 ; set current position as zero"
        )
        gcode.append(
            f"G0 {self.machine.lin_axis}0 {self.machine.rot_axis}0"
        )

        current_rot = 0.0  # mandrel revolutions
        current_lin = 0.0  # carriage position

        for layer in self.layers:
            if layer.type == "helical":
                new_lines, current_rot, current_lin = self._generate_helical_layer(
                    layer, current_rot, current_lin
                )
            elif layer.type == "hoop":
                new_lines, current_rot, current_lin = self._generate_hoop_layer(
                    layer, current_rot, current_lin
                )
            else:
                continue
            gcode.extend(new_lines)

        gcode.append("M30 ; end program")
        return gcode

    def _generate_helical_layer(
        self, layer: Layer, current_rot: float, current_lin: float
    ) -> tuple[list[str], float, float]:
        lines = []

        theta = math.radians(abs(layer.angle))
        C = self.mandrel.circumference()
        L = self.mandrel.length

        # axial travel per mandrel revolution
        lead = C / math.tan(theta)

        # mandrel revolutions needed for one full carriage pass
        delta_rot = L / lead

        for p in range(1, layer.passes + 1):
            # alternate carriage endpoint each pass
            next_lin = L if p % 2 == 1 else 0.0

            current_rot += delta_rot
            current_lin = next_lin

            cmd_rot = current_rot * self.machine.rot_scale
            cmd_lin = current_lin * self.machine.lin_scale

            lines.append(
                f"G1 {self.machine.rot_axis}{cmd_rot:.4f}"
                f" {self.machine.lin_axis}{cmd_lin:.4f}"
                f" F{self.machine.feed_rate}"
            )

        return lines, current_rot, current_lin

    def _generate_hoop_layer(
        self, layer: Layer, current_rot: float, current_lin: float
    ) -> tuple[list[str], float, float]:
        lines = []

        for _ in range(layer.passes):
            current_rot += 1.0  # one mandrel revolution

            cmd_rot = current_rot * self.machine.rot_scale
            cmd_lin = current_lin * self.machine.lin_scale

            lines.append(
                f"G1 {self.machine.rot_axis}{cmd_rot:.4f}"
                f" {self.machine.lin_axis}{cmd_lin:.4f}"
                f" F{self.machine.feed_rate}"
            )

        return lines, current_rot, current_lin
