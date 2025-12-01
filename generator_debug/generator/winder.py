# Folder that simulates the winder
# Generates gcode commands from coordinates and compiles gcode commands

# Definitions:
#   - The x-axis will be defined as the carriage motion along the mandrel, in inches
#   - The z-axis will be defined as the rotation of the mandrel, in degrees
#   - The y-axis is currently unused, but could be employed in the future
#   - GRBL does not allow for additional rotational axes. For a future expansion to a four-axis machine,
#     a different firmware will likely be required.

import json


class Winder():

    ## Initializing the winder
    def __init__(self, defaultFeedrate):
        [self.mandrelDiameter, self.mandrelLength, self.xLimit] = Winder.loadMachineConfig()

        self.defaultFeedrate = defaultFeedrate

        self.X = 0
        self.Z = 0

        self.gcode = []

        # Automatically defining it as inches
        self.gcode.append("G20")


    # Loads information about the filament winder from a config file
    def loadMachineConfig():
        configFile = open('machine_config.json')

        machineData = json.load(configFile)

        mandrelDiameter = machineData['mandrel_diameter']
        mandrelLength = machineData['mandrel_length']
        xLimit = machineData['x_limit']

        return [mandrelDiameter, mandrelLength, xLimit]
    
    # G28 literally sends all of the axes to their predefined home position
    def moveHome(self):
        self.gcode.append("G28")


    # Set the axes to zero
    def zero(self):
        self.setAxes(0, 0)


    # Set the axes to the specified X and Z value
    # G92 literally sets the x/z point to whatever value they're at
    def setAxes(self, x, z) -> None:
        self.X = x
        self.Z = z

        command = "G92 X" + str(round(x, 3)) + " Z" + str(round(z, 3))
        self.gcode.append(command)


    # Actuates each axis by the specified amount
    # (G01 moves the steppers)
    def moveBy(self, dx, dz) -> None:
        if (self.outOfBounds(self.X + dx, self.Z + dz)):
            print("Error: Location is out of bounds")
            return
        
        self.X = self.X + dx
        self.Z = self.Z + dz

        command = "G01 X" + str(round(self.X, 3)) + " Z" + str(round(self.Z, 3))
        self.gcode.append(command)

        return


    # Moves to the specified location
    def moveTo(self, x, z) -> None:
        if (self.outOfBounds(x, z)):
            print("Error: Location is out of bounds")
            return
        
        self.X = x
        self.Z = z

        command = "G01 X" + str(round(self.X, 3)) + " Z" + str(round(self.Z, 3))
        self.gcode.append(command)

        return
    
    
    def setFeedRate(self, f, force=False):
    
        if force or self.currentFeedRate is None or f != self.currentFeedRate:
            self.gcode.append("G01 F" + str(round(f, 3)))
            self.currentFeedRate = f

    

    def pushComment(self, comment):
        self.gcode.append("(" + comment + ")")
    

    def getProperties(self):
        return {'diameter': self.mandrelDiameter,
                'length': self.mandrelLength,
                'xLimit': self.xLimit}
    

    def getGcode(self):
        return self.gcode
    

    def getDiameter(self) -> float:
        return self.mandrelDiameter
    

    # Checks if location is within winder movement area
    def outOfBounds(self, x, z) -> bool:
        return x < 0 or x > self.xLimit