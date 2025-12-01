import helper
import winder
import definitions
import load
import planner


def main():
    # Welcome message
    print("=================================================================")
    print("| Welcome to the Swamp Launch Filament Winder Gcode Generator   |")
    print("| Please enter a command, or type 'help' for a list of commands |")
    print("=================================================================")

    # Variables to track
    schedule = []
    defaultFeedRate = 0.005
    machine = None
    gcode = []

    # Take user input until quit
    userInput = ""
    quit = False
    while (not quit):
        try:
            userInput = input("(enter command or 'quit'): ")

            # Command tree
            if (userInput == "help"):
                helper.printHelpMenu()

            elif (userInput == "load"):
                [schedule, defaultFeedRate] = helper.loadWindFile()

            elif (userInput == "loadg"):
                print("loadg selected")
                # TODO: implement loadg

            elif (userInput == "generate"):
                print("DEBUG: Layers in schedule =", len(schedule))
                for layer in schedule:
                    print("\tLayer type:", layer.getType())

                machine = winder.Winder(defaultFeedRate)
                gcode = planner.planWind(schedule, machine)
                machine.setFeedRate(defaultFeedRate, force=True)  # <-- ensure F line is added
                print("DEBUG: G-code lines generated =", len(gcode))

            elif (userInput == "plot"):
                print("plot selected")
                # TODO: implement plot

            elif (userInput == "write"):
                with open('windGcode.nc', 'w') as writeFile:
                    for line in gcode:
                        writeFile.write(line + '\n')

            elif (userInput == "calculator"):
                helper.calculator()

            elif (userInput == "quit"):
                confirmation = input("Are you sure you want to quit? Any unsaved data will be lost. (y/n) ")
                if (confirmation == "y"):
                    quit = True
        except (KeyboardInterrupt, EOFError):
            quit = True
        

# Actually call main function
main()

