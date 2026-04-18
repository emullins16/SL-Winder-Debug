import json
import math


# =========================================================
# CONFIG
# =========================================================
def load_config(path="machine_config.json"):
    with open(path, "r") as f:
        return json.load(f)


# =========================================================
# MACHINE (EXECUTION ONLY)
# =========================================================
class Winder:
    def __init__(self, config):
        self.length = config["mandrel_length"]
        self.diameter = config["mandrel_diameter"]
        self.x_limit = config["x_limit"]

        self.circumference = math.pi * self.diameter
        self.feedrate = config.get("defaultFeedRate", 100)

        self.gcode = ["G20", "G90"]

    def move(self, x, s):
        if x < 0 or x > self.x_limit:
            raise ValueError(f"X out of bounds: {x} (limit {self.x_limit})")

        self.gcode.append(
            f"G01 X{round(x,4)} Z{round(s,4)} F{self.feedrate}"
        )

    def comment(self, msg):
        self.gcode.append(f"({msg})")

    def export(self):
        return self.gcode


# =========================================================
# HELICAL SOLVER (NO REVERSAL MODEL)
# =========================================================
class HelicalSolver:
    def __init__(self, config, layer):
        self.theta = math.radians(layer["windAngle"])
        self.tan_theta = math.tan(self.theta)

        self.tow = layer["towWidth"]
        self.num_starts = layer.get("numStarts", 1)

        self.length = config["mandrel_length"]
        self.circumference = math.pi * config["mandrel_diameter"]

    def band_spacing(self):
        effective = self.tow / math.cos(self.theta)
        bands = math.ceil(self.circumference / effective)
        spacing = self.circumference / bands
        return bands, spacing


# =========================================================
# PURE HELICAL GENERATION (NO BACKTRACKING)
# =========================================================
def solve_helical(machine, config, layer):

    solver = HelicalSolver(config, layer)

    L = solver.length
    tan_t = solver.tan_theta

    starts = layer.get("numStarts", 1)
    passes = layer.get("passes", 10)  # <-- this now actually matters

    steps_per_pass = 300  # higher resolution = real composite winding

    total_steps = passes * steps_per_pass

    dx = L / steps_per_pass
    dz = dx * tan_t

    machine.comment("=== AIRFRAME CONTINUOUS HELICAL WIND ===")
    machine.comment(f"Starts={starts}, Passes={passes}")

    for s in range(starts):

        machine.comment(f"START {s+1}/{starts}")

        # phase shift for multi-start winding
        x = 0.0
        z = s * (solver.circumference / starts)

        direction = 1

        for i in range(total_steps):

            # X oscillates continuously
            if direction == 1:
                x += dx
                if x >= L:
                    x = L
                    direction = -1
            else:
                x -= dx
                if x <= 0:
                    x = 0
                    direction = 1

            # Z ALWAYS increases (this is the key fix)
            z += abs(dz)

            machine.move(x, z)

# =========================================================
# RUN SOLVER
# =========================================================
def run(config):

    machine = Winder(config)

    for layer in config["layers"]:

        if layer["windType"] != "helical":
            raise ValueError("This solver is helical-only")

        solve_helical(machine, config, layer)

    return machine.export(), machine


# =========================================================
# SAVE / REBOOT SYSTEM
# =========================================================
def save_session(config, machine, path="winder_session.json"):
    state = {
        "config": config,
        "machine_state": {
            "length": machine.length,
            "diameter": machine.diameter,
            "x_limit": machine.x_limit,
            "feedrate": machine.feedrate,
        },
        "gcode": machine.gcode
    }

    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def load_session(path="winder_session.json"):
    with open(path, "r") as f:
        return json.load(f)


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":

    config = load_config("machine_config.json")

    gcode, machine = run(config)

    with open("output.gcode", "w") as f:
        for line in gcode:
            f.write(line + "\n")

    # SAVE STATE FOR NEXT CHAT / CONTINUATION
    save_session(config, machine)

    print("✔ Helical winding complete")
    print("✔ Session saved → winder_session.json")