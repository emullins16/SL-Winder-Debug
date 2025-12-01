# Composites_Filament_Winder

Repository for code and documentation for the filament winder.

## Project Structure
Currently, the project is organized into two folders.
1. generator: Program to be used on a desktop/laptop to create a configuration file that is transferred to the Arduino. This is where we will set wind angle, plies, and other settings.
2. documentation: Any documentation for the winder. (Right now, there is nothing.)

### Python files Within Generator:

There are currently seven files within the generator, working to varying degrees

> - definitions.py
> - gui.py
> - helper.py
> - load.py
> - main.py
> - planner.py
> - winder.py

However, there are only two files of actual use (in terms of outputting a GCODE file). 

> - gui.py (Updated version of main.py, greater functionality/usability)
>   - Modified to use tkinter window as a gui :)
> - main.py (Rylan's original code | WARNING: main.py doesn't set default feed rate.)

The rest can all be considered basic helper files. 

A breakdown of their functionality for debugging purposes is as folows.

### Helper Files:

#### definitions.py
Sets the internal definitions for the rest of the code to be used. 

        # Angle of the helical wind
        # Defined as the angle between the mandrel axis and the wind tow
        # i.e., a length of tow running straight from one end of the mandrel to the other would have an angle of zero degrees
        self.windAngle = float(windAngle)

        # Each circuit will perform a pass going down the mandrel and coming back. The next pass will not be started immediately adjacent 
        # to the previous pass, and will instead start at a new start position some angle off from the previous start position.
        # Once a pass has been completed at each start position, a "pattern" is completed. Subsequent patterns will be completed
        # to cover the mandrel completely (the number of patterns required is determined by tow width).
        # This parameter determines the number of start positions
        self.numStarts = int(numStarts)

        # The angle through which to turn the mandrel at the end of each pass. Usually 720 degrees
        self.lockAngle = int(lockAngle)

*Note: Rylan's documentation notes two different winds, Hoop and Helical. Supposedly, most of the work will be helical. This assumption is twofold. First, it comes off the fact that a hoop won't really help a filamnet winder. Second, there is no code written for hoops in "planner.py".*

#### helper.py
Prints the much of the text used when the main.py is ran inputted to a CLI. This code defines most of the functions that are considered "usable at the moment". 
- Help
- Load
- Generate
- Calculate

#### load.py
External code written pretty much purely to load information from a .json file.

*Note: This version varies drastically from the original provided in Rylans code, as the prior version had a rather vigorous debate between using a dictionary or a class to load the .json information.*

#### planner.py
This file is in charge of much of the internal math that goes into writing the generator code. If there is an issue in the outputted math of the file, this should probably be the first place to check.

For the most part, it seems to be written to behave precisely how Rylan's earlier comments had stated.

#### winder.py

From Rylan's code:

>"Folder that simulates the winder, Generates gcode commands from coordinates and compiles gcode commands" 
>
> Definitions:
> - The x-axis will be defined as the carriage motion along the mandrel, in inches
> - The z-axis will be defined as the rotation of the mandrel, in degrees
> - The y-axis is currently unused, but could be employed in the future

Lovely.

Most of the file can be interpreted line-by-line, as they almost all correspond to a line in G-Code.

For brevity, the line outputs are as follows:
> - G20 | Sets the GCODE to inches, could be tweaked to G21 for mm.
> - G01 F100.0 | Notably absent when ran from main.py? Sets the "output" wind speed.
> - G92 X0 Z0 | Defines the axis of movement
> - G01 X0 Z0 | G01 is a movement function
> - G92 X0 Z0 | Resetting axis, not sure why but the code has always done this.




