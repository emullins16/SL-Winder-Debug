# Computes required mandrel and carriage positions to execute winds

import math

import definitions
import winder



def planWind(schedule, machine: winder.Winder):

    machine.moveHome()
    # Set location as zero
    machine.zero()
    # Set default feed rate
    #machine.setFeedRate(0.5)

    for layer in schedule:
        if (layer.getType() == definitions.WindType.HOOP):
            planHoopWind(layer, machine)
        elif (layer.getType() == definitions.WindType.HELICAL):
            planHelicalWind(layer, machine)
        else:
            print('Error: layer not recognized as a valid type')

    return machine.getGcode()            


def planHoopWind(layer, machine):
    # TODO: implement logic for a hoop wind
    return

def planHelicalWind(layer: definitions.HelicalWind, machine: winder.Winder):
    # --- Retrieve basic properties ---
    mandrelCircumference = math.pi * machine.getDiameter()   # [inches]
    windLength = layer.getWindLength()                       # [inches]
    towWidth = layer.getWidth()                              # [inches]
    windAngleDeg = layer.getWindAngle()                     # DEGREES (from JSON)
    numStarts = layer.getNumStarts()                        # integer
    lockAngleDeg = layer.getLockAngle()                     # DEGREES (used directly in G-code)
    skipInitialLock = layer.doSkipInitialLock()             # boolean


    effectiveTowWidth = towWidth / math.cos(math.radians(windAngleDeg))


    numCircuits = math.ceil(mandrelCircumference / effectiveTowWidth)

  
    passStepAngle = 360 / numCircuits 

    passAngle = (windLength * math.tan(math.radians(windAngleDeg))) * (360 / mandrelCircumference)
   
    numPatterns = int(numCircuits / numStarts)

    # --- Validation ---
    if (numCircuits % numStarts != 0):
        print('Invalid combination of number of circuits and number of starts.')
        print('Please use the calculator to compute valid start numbers for your wind angle and tow.')
        print('-------------------------------------------------------------------------------------')
        print('This layer will be skipped.')
        return


    if (not skipInitialLock):
        machine.moveBy(dx=0, dz=lockAngleDeg)  

    # --- Loop over patterns and starts ---
    for i in range(numPatterns):
        machine.setAxes(x=machine.X, z=0)  # reset Z for each pattern
        for j in range(numStarts):
            machine.pushComment(f"Pattern: {i}/{numPatterns} Circuit: {j}/{numStarts}")
            
            # Wind down the mandrel
            machine.moveBy(dx=windLength, dz=passAngle)  # passAngle in DEGREES

            # Perform lock wind
            machine.moveBy(dx=0, dz=(lockAngleDeg - (passAngle % 360)))

            # Wind up the mandrel
            machine.moveBy(dx=-windLength, dz=passAngle)

            # Perform another lock wind
            machine.moveBy(dx=0, dz=(lockAngleDeg - (passAngle % 360)))

            # Move to next start position
            machine.moveBy(dx=0, dz=(passStepAngle * numCircuits / numStarts))

        # Move to the next pattern location
        machine.moveBy(dx=0, dz=passStepAngle)

    
