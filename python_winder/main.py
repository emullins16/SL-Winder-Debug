from machine import Machine
from mandrel import Mandrel
from winder_job import WinderJob
from gcode_writer import GCodeWriter


def main():
    machine = Machine(
        lin_axis="X",
        rot_axis="Z",
        units="in",
        feed_rate=150,   # in/min
        lin_scale=1.0,
        rot_scale=1.0,
    )

    mandrel = Mandrel(diameter=6, length=20)  # inches

    job = WinderJob(machine, mandrel)
    job.add_layer(angle=80, passes=6)
    job.add_hoop_layer(passes=3)

    gcode = job.generate_gcode()

    for line in gcode:
        print(line)

    writer = GCodeWriter("generated_gcode/test_wind.gcode")
    writer.write(gcode)


if __name__ == "__main__":
    main()
