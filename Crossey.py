from random import *
import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 1234567890"

"""
This function takes an input of a String and outputs the String
without numbers and punctuation.
"""
def clean( input ):
  clean = ""
  for character in input:
    if character in alphabet:
      clean += character
  return clean.lower()

short_map = {
    "h" : "help",
    "n" : "north",
    "s" : "south",
    "e" : "east",
    "w" : "west",
    "l" : "look",
    "i" : "inventory"
}

def short( command ):
    command = clean(command)
    if command in short_map:
        return short_map[command]
    return command

scenes = {
    "Town_Square" : {
        "description" : "This is a town square. There are villagers milling about. There is a clock tower in the center.",
        "commands" : [ "north", "south", "east", "west", "look", "attack villager" ] ,
    },
    "hallway" : {
        "description" : "You find yourself in a long hallway. At the north end is a goblin, it may be dead already.",
        "commands" : [ "north", "south", "east", "west", "look", "attack" ],
    },
    "vault" : {
        "description" : "Behind the dead goblin, you find a big vault. The only interesting feature is a big button on the front that says \"Do not press me.\"",
        "commands" : [ "south", "press button" ],
    },
    "Great_Hall" : {
        "description" : "You are in the town's Great Hall. Inside is a long table with chairs all around it. At the head sits a depressed man, who seems to be a Baron. There are rooms all arund the hall.",
        "commands" : [ "north", "south", "east", "west", "look", "talk to baron", "explore" ],
    }
}

inventory = ["sword", "gold", "clothes"]

playerScene = "Town_Square"
playerHealth = (4*(randint(1, 8))) + 8
print(playerHealth)
playerPoints = 0
playerHasKilledGoblin = False
takePaperAllowed = False
hallExplored = True

# The brains of the operation
def runScene():

    # Make sure the player is alive
    if( playerHealth > 0 ):
        # Print the current scene's description
        print( scenes[playerScene]["description"] )
        print( "" )
        # Accept input from the user
        command = short(input("What would you like to do: "))
        print( "" )

        # If our command is help, print the list of commands available
        if( command == "help" ):
            print( scenes[playerScene]["commands"] )
            print( "" )
            print("Your health is " + playerHealth + ".")
            print( "" )
            runScene()
        elif(command == "inventory"):
            print(inventory)
            print("")
            runScene()
        # Check if the command is in the list of available commands, run it if it is
        elif( command in scenes[playerScene]["commands"] ):
            runCommand( playerScene, command )
        # Uh, we don't understand that command, let the player know and move on
        else:
            print("Sorry, this scene does not support that command.")
            print( "" )
            runScene()
    # Our player is dead
    else:
        print( "You've lost the game, you are terrible. And dead." )
        print( "" )

# Defining all the logic and command responses
def runCommand(scene,command):

    # These are global variables which we want to modify globally
    global playerScene, playerHealth, playerPoints, playerHasKilledGoblin, lose_health, takePaperAllowed, hallExplored

    # Our start scene and each command available
    if( scene == "Town_Square" ):
        if( command == "north" ):
            print( "You go north." )
            print( "" )
            playerScene = "Great_Hall"
            runScene()
        elif( command == "south" ):
            print( "You go south." )
            print( "" )
            playerScene = "wall1"
            runScene()
        elif( command == "west" ):
            print( "You go west." )
            print( "" )
            print( "You are stopped at the city wall, you can't go further. You return to the town square." )
            runScene()
        elif( command == "east" ):
            print( "You go east." )
            print( "" )
            playerScene = "inn"
            runScene()
        elif( command == "attack villager" ):
            print( "You attack the nearest villager." )
            lose_health = randint(1, 4)
            playerHealth = playerHealth - lose_health
            print("You lost " + str(lose_health) + " health! You killed the villager, and are arrested.")
            print("")
            sys.exit()
        elif( command == "look" ):
            print( "A massive duel was recently fought here. The clock tower shows the correct time, and does not seem our of the ordinary." )
            print( "" )
            runScene()
        elif( command == "inventory" ):
            print(inventory)
            print( "" )
            runScene()
    # The warehouse scene
    elif( scene == "warehouse" ):
        if( command == "south" ):
            print( "You approach an inn." )
            print( "" )
            playerScene = "inn"
            runScene()
        elif( command == "north" ):
            print( "You go north.")
            print("")
            playerScene = "wall2"
        elif( command == "attack" ):
            print( "Like a maniac you attack the goblin, it was an easy fight and you kill the goblin. You got 100 points!" )
            print( "" )
            playerHasKilledGoblin = True
            playerPoints = playerPoints + 100
            runScene()
        elif( command == "look" ):
            print( "You take your time to look around. While you sit there like an idiot, the goblin attacks and hurts you." )
            print( "" )
            playerHealth = playerHealth - 50
            runScene()

    # Great Hall
    elif( scene == "Great_Hall" ):
        if( command == "south" ):
            print( "You return to the town square." )
            print( "" )
            playerScene = "Town_Square"
            runScene()
        elif( command == "talk to baron" ):
            print( "You approach the depressed man. He seem to be a baron. He asks you for help. He needs someone to deliver a sealed message to the head of the Red Knights." )
            scenes["Great_Hall"]["commands"].append("take paper");
            takePaperAllowed = True
            print( "" )
            runScene()
        elif( command == "west" ):
            print( "You go west." )
            print( "" )
            print( "You are stopped at the city wall, you can't go further. You return to the town square." )
            runScene()
        elif( command == "north" ):
            print( "You go north to a windmill." )
            print( "" )
            playerScene = "mill"
            runScene()
        elif( command == "east" ):
            print( "You go east to a warehouse." )
            print( "" )
            playerScene = "warehouse"
            runScene()
        elif( command == "explore" ):
            print( "You walk around the Hall, peeking through doors and observing. You find in one room, a glowing knife, and some chalk." )
            scenes["Great_Hall"]["commands"].append("take chalk");
            scenes["Great_Hall"]["commands"].append("take knife");
            hallExplored = True
            print( "" )
            runScene()
        elif( command == "take chalk" ):
            if(hallExplored):
                inventory.append("chalk")
                print("You take the chalk.")
                runScene()
        elif( command == "take knife" ):
            if(hallExplored):
                inventory.append("magical knife")
                print("You take the knife.")
                runScene()
        elif( command == "take paper" ):
            if(takePaperAllowed):
                inventory.append("letter from baron")
                print("You take the paper.")
                runScene()
    else:
        print( "Scene not found, error." )

# The opening description for the game, along with some simple instructions
print("Welcome to Interactive Fiction Starter: The Game!\n\nYour task is to navigate through these rooms and discover all the secrets you can.")
print( "" )
print( "If you need help at any time, type help." )
print( "" )

# Let's go right into the game, this function is recursive and will keep calling itself until we win or lose
runScene()

# We broke out of the "game loop" so let's output the final score
print( "Your final score is: " + str(playerPoints) )
print( "" )
print( "Thanks for playing!" )
