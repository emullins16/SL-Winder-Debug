# Helper functions for top-level functionality

import math

import definitions
import winder
import load


def printHelpMenu():
    # Prints the help menu
    
    print("=================================================================")
    print("Available commands:")
    print(" load - load a wind file")
    print(" loadg - load a gcode file")
    print(" generate - generate gcode from a wind file")
    print(" plot - plot a gcode file")
    print(" write - save a gcode file")
    print(" calculator - run wind parameter utility")
    print(" quit - terminate this session")
    print("=================================================================")


# Loads the wind file that specifies the layup schedule
def loadWindFile(log_fn=print):
    log_fn("Loading from file...")
    data, file_path = load.get_data()
    if data is None:
        return None, None  # prevents unpack error

    print("Loading from", file_path)
    print("---")

    length = float(data["length"])
    defaultFeedRate = float(data["defaultFeedRate"])

    schedule = []
    for layer in data["layers"]:
        if layer["windType"] == "hoop":
            schedule.append(definitions.HoopWind(
                length, layer["towWidth"], layer["towThickness"], layer["terminal"]))
        elif layer["windType"] == "helical":
            schedule.append(definitions.HelicalWind(
                length, layer["towWidth"], layer["towThickness"], layer["windAngle"],
                layer["numStarts"], layer["skipIndex"], layer["lockAngle"],
                layer["leadInLength"], layer["leadOutLength"], layer["skipInitialLock"]))
        else:
            print("\tInvalid wind type:", layer["windType"])


    print("Layer Information:")
    for layer in schedule:
        if layer.getType() == definitions.WindType.HOOP:
            print("\tLAYER TYPE: HOOP")
            print("\t\tTow Width: \t" + str(layer.getWidth()))
            print("\t\tTow Thickness: \t" + str(layer.getThickness()))
        elif layer.getType() == definitions.WindType.HELICAL:
            print("\tLAYER TYPE: HELICAL")
            print("\t\tTow Width: \t" + str(layer.getWidth()))
            print("\t\tTow Thickness: \t" + str(layer.getThickness()))
            print("\t\tWind Angle: \t" + str(layer.getWindAngle()))

    return [schedule, defaultFeedRate]


def generateWind(schedule, defaultFeedRate):
    machine = winder.Winder()

def calculator():
    print("===============================================================================================")
    print("This calculator utility will compute valid wind settings for a given tow width and wind angle.")
    print("Note: units must match if not specified.")
    print("-----------------------------------------------------------------------------------------------")

    mandrelDiameter = float(input("Mandrel diameter: "))
    towWidth = float(input("Tow width: "))
    windAngle = float(input("Wind angle [deg]: "))

    mandrelCircumference = math.pi * mandrelDiameter
    effectiveTowWidth = towWidth / math.cos(math.radians(windAngle))
    numCircuits = math.ceil(mandrelCircumference / effectiveTowWidth)

    print("-----------------------------------------------------------------------------------------------")
    print("Number of circuits: " + str(numCircuits))
    print("Valid start position quantities:")

    for i in range(1, numCircuits+1):
        if (numCircuits % i == 0):
            print("     " + str(i))

    print("===============================================================================================")


