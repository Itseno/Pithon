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
    "warehouse" : {
        "description" : "You approach a warehouse, There is only one entry, it seems to be locked.",
        "commands" : [ "south", "press button" ],
    },
    "Great_Hall" : {
        "description" : "You are in the town's Great Hall. Inside is a long table with chairs all around it. At the head sits a depressed man, who seems to be important. There are rooms all around the hall.",
        "commands" : [ "north", "south", "east", "west", "look", "talk to baron", "explore" ],
    },
    "mill" : {
        "description" : "You enter a mill, it reeks of wheat and barley. There is a circular staircase in fron of you that is locked by a gate. There are tables spread out in the room, and a man working the grindstone.",
        "commands" : [ "south", "east", "west", "look", "talk to Miller" ],
    },
    "inn" : {
        "description" : "You enter an inn. Almost every table is full. You friend Criaf sits at the bar. A mysterious looking man leans against the wall in the corner.",
        "commands" : [ "north", "south", "west", "look", "talk to Criaf", "explore", "approach man", "buy a drink" ],
    },
    "church" : {
        "description" : "You enter a church.",
        "commands" : [ "north", "south", "west", "look", "talk to Criaf", "explore", "approach man", "buy a drink" ],
    },
    "camp" : {
        "description" : "You approach the camp of the Red Knights.",
        "commands" : [ "north", "south", "west", "look", "talk to Criaf", "explore", "approach man", "buy a drink" ],
    },
    "jail" : {
        "description" : "You enter a jail. A guard sits at the desk",
        "commands" : [ "north", "south", "west", "look", "talk to Criaf", "explore", "approach man", "buy a drink" ],
    },
    "docks" : {
        "description" : "You stand on the docks of the city. ",
        "commands" : [ "north", "south", "west", "look", "talk to Criaf", "explore", "approach man", "buy a drink" ],
    },
    "wall_e" : {
        "description" : "You approach the city wall, and West gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "dance", "attack guard", "climb wall", "talk to guard"],
    },
    "wall_s" : {
        "description" : "You approach the city wall, and South gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "dance", "attack guard", "climb wall", "talk to guard"],
    },
    "wall_w" : {
        "description" : "You approach the city wall, and East gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "dance", "attack guard", "climb wall", "talk to guard"],
    }
}
inventory = ["sword", "gold", "clothes"]

playerScene = "Town_Square"
playerHealth = (4*(randint(1, 8))) + 8
print(playerHealth)
playerPoints = 0
playerHasKilledGoblin = False
takePaperAllowed = False
hallExplored = False
millExplored = False
tookPaper = False
tookChalk = False

# The brains of the operation
def runScene():
    global playerScene, playerHealth, playerPoints, playerHasKilledGoblin, tookChalk, lose_health, takePaperAllowed, hallExplored, millExplored, tookPaper
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
            print("Your health is " + str(playerHealth) + ".")
            print( "" )
            runScene()
        elif(command == "inventory"):
            print(inventory)
            print("")
            runScene()
        elif(command == "draw circle"):
            if(tookChalk):
                print("You draw a circle on the ground with your chalk. You stand in it, and are teleported away!!!!")
                print("")
                playerScene = "warehouse"
                runScene()
            else:
                print("Sorry, this scene does not support that command.")
                print( "" )
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
    global playerScene, playerHealth, playerPoints, playerHasKilledGoblin, tookChalk, lose_health, takePaperAllowed, hallExplored, millExplored, tookPaper

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
            playerScene = "wall_s"
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
            print("The game is over, you lose.")
            sys.exit()
        elif( command == "look" ):
            print( "A massive duel was recently fought here. The clock tower shows the correct time, and does not seem our of the ordinary." )
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
            scenes["Great_Hall"]["commands"].append("take letter");
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
                tookChalk = True
                print( "" )
                runScene()
        elif( command == "take knife" ):
            if(hallExplored):
                inventory.append("magical knife")
                print("You take the knife.")
                print( "" )
                runScene()
        elif( command == "take letter" ):
            if(takePaperAllowed):
                inventory.append("letter from baron")
                print("You take the letter.")
                tookPaper = True
                print( "" )
                runScene()
    elif( scene == "inn" ):
        if( command == "south" ):
            print( "You go south." )
            print( "" )
            playerScene = "church"
            runScene()
        elif( command == "north" ):
            print( "You go north.")
            print("")
            playerScene = "warehouse"
            runScene()
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
    elif( scene == "mill" ):
        if( command == "south" ):
            print( "You go south." )
            print( "" )
            playerScene = "Great_Hall"
            runScene()
        elif( command == "east" ):
            print( "You go east.")
            print("")
            playerScene = "wall_e"
            runScene()
        elif( command == "look" ):
            print( "You take your time to look around. You notice keys on one of the tables. Miller the miller has a strange tatoo of a staff on his wrist. There also seems to be a large amount of food in here, much more than the village needs." )
            print( "" )
            scenes["mill"]["commands"].append("take keys");
            millExplored = True
            runScene()
        elif( command == "take keys"):
            if millExplored:
                print("You take the keys quickly.")
                print( "" )
                inventory.append("keys")
                runScene()
        elif( command == "talk to miller"):
            print("Why hello there lad! Quite a nice day, eh? Take your time to look around, and when your done I'll be seeing you!")
            print( "" )
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
