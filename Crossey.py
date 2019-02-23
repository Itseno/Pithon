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
        "commands" : [ "north", "south", "west", "look", "climb warehouse"],
    },
    "Great_Hall" : {
        "description" : "You are in the town's Great Hall. Inside is a long table with chairs all around it. At the head sits a depressed man, who seems to be important. There are rooms all around the hall.",
        "commands" : [ "north", "south", "east", "look", "talk to baron", "explore" ],
    },
    "mill" : {
        "description" : "You enter a mill, it reeks of wheat and barley. There is a circular staircase in fron of you that is locked by a gate. There are tables spread out in the room, and a man working the grindstone.",
        "commands" : [ "south", "east", "west", "look", "talk to miller" ],
    },
    "inn" : {
        "description" : "You enter an inn. Almost every table is full. You friend Criaf sits at the bar.",
        "commands" : [ "north", "south", "west", "look", "talk to criaf", "buy a drink" ],
    },
    "church" : {
        "description" : "You enter a church. Inside is a priest and a few people praying. There are pews, and from the center of the room hangs a rope. There is also a fountain.",
        "commands" : [ "north", "look", "talk to priest", "pull rope", "swim in fountain" ],
    },
    "camp" : {
        "description" : "You approach the camp of the Red Knights. Guards stop you, and escort you to the new leader of the camp. You talk to him in his tent. There are tables, charts, chairs, and many weapons.",
        "commands" : [ "go back to city wall", "talk to leader", "look", "attack guard", "attack leader" ],
    },
    "jail" : {
        "description" : "You enter a jail. A guard sits at his desk, sleeping. Further down the hallway is a prisoner.",
        "commands" : [ "go back to city wall", "talk to jailer", "hide", "look", "talk to prisoner" ],
    },
    "docks" : {
        "description" : "You stand on the docks of the city. There are a couple men talking in a huddled group. A heavyset dockmaster is working the dock. There are several boats in the dock.",
        "commands" : [ "go back to city wall", "talk to dockmaster", "approach men", "look", "steal boat"],
    },
    "wall_e" : {
        "description" : "You approach the city wall, and East gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "south", "dance", "attack guard", "climb wall", "talk to guard"],
    },
    "wall_s" : {
        "description" : "You approach the city wall, and South gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "dance", "attack guard", "climb wall", "talk to guard"],
    },
    "wall_w" : {
        "description" : "You approach the city wall, and West gate. Guards guard the gate.",
        "commands" : [ "enter city", "exit city", "dance", "attack guard", "climb wall", "talk to guard"],
    },
    "final_battle" : {
        "description" : "You are in the warehouse. The Mage is here.",
        "commands" : [ "attack mage", "leave"],
    }

}
inventory = ["sword", "gold", "clothes"]

playerScene = "Town_Square"
playerHealth = (4*(randint(1, 8))) + 8
playerPoints = 0
MageHealth = 50
playerHasKilledGoblin = False
takePaperAllowed = False
hallExplored = False
millExplored = False
tookPaper = False
tookChalk = False
tookKnife = False
hasNote = False
tookKeys = False


# The brains of the operation
def runScene():
    global playerScene, playerHealth, playerPoints, tookKeys, climbChance, hasNote, playerHasKilledGoblin, tookChalk, lose_health, takePaperAllowed, hallExplored, millExplored, tookPaper
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
        #EASTER EGG
        elif(command == "draw circle"):
            if(tookChalk):
                print("You draw a circle on the ground with your chalk. You stand in it, and are teleported away!!!!")
                print("")
                playerScene = "final_battle"
                runScene()
            else:
                print("Sorry, this scene does not support that command.")
                print( "" )
                runScene()
        #In case you ever want to redo the final battle, without going through the game again.
        elif(command == "test final battle"):
            scenes["final_battle"]["commands"].append("draw lines with chalk");
            scenes["final_battle"]["commands"].append("throw knife");
            inventory.append("magical knife")
            scenes["final_battle"]["commands"].append("pray");
            scenes["final_battle"]["commands"].append("flip a silver piece");
            scenes["final_battle"]["commands"].append("drink potion");
            inventory.append("potion")
            playerScene = "final_battle"
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
        print( "You've lost the game, you are dead. But, you were so close! " )
        print( "" )

# Defining all the logic and command responses
def runCommand(scene,command):

    # These are global variables which we want to modify globally
    global playerScene, playerHealth, playerPoints, tookKeys, MageHealth, climbChance, playerHasKilledGoblin, tookChalk, lose_health, hasNote, takePaperAllowed, hallExplored, millExplored, tookPaper, tookKnife, fall_damage

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
    #Warehouse
    elif( scene == "warehouse" ):
        if( command == "south" ):
            print( "You approach an inn." )
            print( "" )
            playerScene = "inn"
            runScene()
        elif( command == "north" ):
            print( "You go north.")
            print("")
            playerScene = "wall_e"
            runScene()
        elif( command == "west" ):
            print( "You go west.")
            print("")
            playerScene = "Great_Hall"
            runScene()
        elif( command == "unlock warehouse" ):
            if tookKeys:
                print( "You unlock the door with the miller's keys and enter.")
                print("")
                playerScene = "final_battle"
            runScene()
        elif( command == "climb warehouse" ):
            print( "You attempt to climb the warehouse.")
            climbChance = randint(1,4)
            if climbChance == 1:
                print("You climb the warehouse successfully, and enter through the roof.")
                playerScene = "final_battle"
                print("")
                runScene()
            else:
                print("You stink at climbing, and so you fall. You lose some health.")
                playerHealth = playerHealth - 1
                print("")
                runScene()
        elif( command == "look" ):
            print( "You look around the whole building, yet there are no entryways. You do find a engravement of a staff on the main door." )
            print( "" )
            if(tookKnife):
                print("Your magical knife glows a very bright blue.")
                print("")
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
                scenes["final_battle"]["commands"].append("draw lines with chalk");
                tookChalk = True
                print( "" )
                runScene()
        elif( command == "take knife" ):
            if(hallExplored):
                inventory.append("magical knife")
                print("You take the knife.")
                scenes["final_battle"]["commands"].append("throw knife");
                tookKnife = True
                print( "" )
                runScene()
        elif( command == "take letter" ):
            if(takePaperAllowed):
                inventory.append("letter from baron")
                print("You take the letter.")
                tookPaper = True
                print( "" )
                runScene()
    #Inn
    elif( scene == "inn" ):
        if( command == "west" ):
            print( "You go west." )
            print( "" )
            playerScene = "Town_Square"
            runScene()
        elif( command == "south" ):
            print( "You go south." )
            print( "" )
            playerScene = "church"
            runScene()
        elif( command == "north" ):
            print( "You go north.")
            print("")
            playerScene = "warehouse"
            runScene()
        elif( command == "look" ):
            if (hasNote == False):
                print( "A mysterious looking man leans against the wall in the corner. He seems to call you over. Everyone else in the inn seems to ignore him." )
                scenes["inn"]["commands"].append("approach man");
            else:
                print("Everyone seems normal within the bar.")
            print( "" )
            runScene()
        elif( command == "approach man"):
            print("You approach the man, he walks towards you, and passes you a piece of paper. He says nothing, and leaves the bar.")
            inventory.append("strange note")
            scenes["inn"]["commands"].append("read note");
            scenes["inn"]["commands"].remove("approach man");
            hasNote = True
            print( "" )
            runScene()
        elif( command == "read note"):
            if hasNote:
                print("The note reads: The wizard is treacherous. A siege is starting, you must stop the wizard. Talk to the Red Knights. Watch for the ware-")
            print( "" )
            runScene()
        elif( command == "buy a drink"):
            print("You buy a drink from the bar.")
            inventory.remove("gold")
            print( "" )
            runScene()
        elif( command == "talk to criaf"):
            print("Criaf is too inebriated to understand.")
            print( "" )
            runScene()
    #Mill
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
        elif( command == "west" ):
            print( "You go west.")
            print("")
            playerScene = "wall_w"
            runScene()
        elif( command == "look" ):
            print( "You take your time to look around. Miller the miller has a strange tatoo of a staff on his wrist. There also seems to be a large amount of food in here, much more than the village needs." )
            print( "" )
            if tookKeys == False:
                print("There are some keys on the table")
                print( "" )
            scenes["mill"]["commands"].append("take keys");
            millExplored = True
            runScene()
        elif( command == "take keys"):
            if millExplored:
                print("You take the keys quickly.")
                print( "" )
                scenes["warehouse"]["commands"].append("unlock warehouse");
                inventory.append("keys")
                tookKeys = True
                runScene()
        elif( command == "talk to miller"):
            print("Why hello there lad! Quite a nice day, eh? Take your time to look around. I'll be watching you!")
            print( "" )
            runScene()
    #Church
    elif( scene == "church" ):
        if( command == "north" ):
            print( "You go south." )
            print( "" )
            playerScene = "inn"
            runScene()
        elif( command == "look" ):
            print( "You notice the rope is attached to a church bell.")
            print("")
            runScene()
        elif( command == "talk to priest" ):
            print( "The priest tells you he is worried of the spirit of the town. It no longer seems safe. He gives you a holy symbol.")
            inventory.append("holy symbol")
            scenes["final_battle"]["commands"].append("pray");
            print("")
            runScene()
        elif( command == "pull rope" ):
            print( "You pull down on the rope and the church bell rings loudly throughout the village. The priest becomes angry and sends you away.")
            playerScene = "inn"
            print("")
            runScene()
        elif( command == "swim in fountain"):
            print( "You swim in the fountain and gain healing properties! Your health increases. The priest becomes angry and sends you away.")
            playerHealth = playerHealth*2
            print("")
            runScene()
    #Camp
    elif( scene == "camp" ):
        if( command == "go back to city wall" ):
            print( "You go back to the town." )
            print( "" )
            playerScene = "wall_w"
            runScene()
        elif( command == "talk to leader" ):
            print( "The leader tells you that he is preparing to squash a rising rebellion in the town.")
            print("")
            if tookPaper:
                print("You hand the leader the message from the baron. He smiles with glea, and tells his guards that the plan is ready. They sail for an island tomorrow from the docks.")
                print("")
            runScene()
        elif( command == "look"):
            print("Maps on the leader's table show a warehouse.")
            print("")
            runScene()
        elif( command == "attack guard"):
            print("You attack the nearest guard!")
            if playerHealth > 10:
                print("You kill him swiftly, but are taken into custody.")
            else:
                print("He disarms you, and you stabs you through the stomach.")
            print("")
        elif( command == "attack leader"):
            print("You attack the leader, but he is too strong. He stabs you through the ribs.")
            print("")
    #Wall West
    elif(scene == "wall_w"):
        if( command == "enter city" ):
            print( "You go back to the town." )
            print( "" )
            playerScene = "mill"
            runScene()
        elif( command == "exit city" ):
            print( "You exit the city" )
            print( "" )
            playerScene = "camp"
            runScene()
        elif( command == "dance" ):
            print( "You dance horribly at the gate, and the guards, mistaking you for a pauper because of your horrible dance moves, throw you a few coins." )
            inventory.append("silver")
            scenes["final_battle"]["commands"].append("flip a silver piece");
            print( "" )
            runScene()
        elif( command == "attack guard"):
            print("You attack the guards.")
            print("")
            if playerHealth > 15:
                print("You kill them swiftly, but you are taken into custody.")
            else:
                print("You are disarmed, and sent to prison for life.")
            print("")
        elif( command == "climb wall"):
            print("You attempt to climb the wall.")
            climbChance = randint(1,2)
            if climbChance == 1:
                print("You climb the wall successfully, but the guards stop you on the other side, and send you out of the city.")
                playerScene = "camp"
                print("")
                runScene()
            else:
                print("You stink at climbing, and so you fall. You lose some health, and the guards send you out of the city.")
                playerHealth = playerHealth - 2
                playerScene = "camp"
                print("")
                runScene()
    #Wall East
    elif(scene == "wall_e"):
            if( command == "enter city" ):
                print( "You go back to the town." )
                print( "" )
                playerScene = "mill"
                runScene()
            elif( command == "exit city" ):
                print( "You exit the city" )
                print( "" )
                playerScene = "docks"
                runScene()
            elif( command == "south" ):
                print( "You go south." )
                print( "" )
                playerScene = "warehouse"
                runScene()
            elif( command == "dance" ):
                print( "You dance horribly at the gate, and the guards, mistaking you for a pauper because of your horrible dance moves, throw you a few coins." )
                inventory.append("silver")
                scenes["final_battle"]["commands"].append("flip a silver piece");
                print( "" )
                runScene()
            elif( command == "attack guard"):
                print("You attack the guards.")
                print("")
                if playerHealth > 15:
                    print("You kill them swiftly, but you are taken into custody.")
                else:
                    print("You are disarmed, and sent to prison for life.")
                print("")
            elif( command == "climb wall"):
                print("You attempt to climb the wall.")
                climbChance = randint(1,2)
                if climbChance == 1:
                    print("You climb the wall successfully, but the guards stop you on the other side, and send you out of the city.")
                    playerScene = "docks"
                    print("")
                    runScene()
                else:
                    print("You stink at climbing, and so you fall. You lose some health, and the guards send you out of the city.")
                    playerHealth = playerHealth - 2
                    playerScene = "docks"
                    print("")
                    runScene()
    #Wall South
    elif(scene == "wall_s"):
            if( command == "enter city" ):
                print( "You go back to the town." )
                print( "" )
                playerScene = "Town_Square"
                runScene()
            elif( command == "exit city" ):
                print( "You exit the city" )
                print( "" )
                playerScene = "jail"
                runScene()
            elif( command == "dance" ):
                print( "You dance horribly at the gate, and the guards, mistaking you for a pauper because of your horrible dance moves, throw you a few coins." )
                inventory.append("silver")
                scenes["final_battle"]["commands"].append("flip a silver piece");
                print( "" )
                runScene()
            elif( command == "attack guard"):
                print("You attack the guards.")
                print("")
                if playerHealth > 15:
                    print("You kill them swiftly, but you are taken into custody.")
                else:
                    print("You are disarmed, and sent to prison for life.")
                print("")
            elif( command == "climb wall"):
                print("You attempt to climb the wall.")
                climbChance = randint(1,2)
                if climbChance == 1:
                    print("You climb the wall successfully, but the guards stop you on the other side, and send you out of the city.")
                    playerScene = "jail"
                    print("")
                    runScene()
                else:
                    print("You stink at climbing, and so you fall. You lose some health, and the guards send you out of the city.")
                    playerHealth = playerHealth - 2
                    playerScene = "jail"
                    print("")
                    runScene()

    #Jail
    elif(scene == "jail"):
            if( command == "go back to city wall" ):
                print( "You go back to the town." )
                print( "" )
                playerScene = "wall_s"
                runScene()
            elif( command == "look" ):
                print( "Nothing seems out of the ordinary. The prisoner makes noises with a cup against the rungs of his cell." )
                print( "" )
                runScene()
            elif( command == "talk to prisoner" ):
                print( "The prisoner seems to be in a fit of lunacy. He talks of tunnels, and a plan to take down the city with a machine of power." )
                print( "" )
                runScene()
            elif( command == "talk to jailer" ):
                print( "The jailer is angry you woke him up, and tells you to go away." )
                print( "" )
                runScene()
            elif( command == "hide" ):
                print( "You hide behind some crates. A man walks in who looks familiar. He is the Mage! He talks about a warehouse with the jailer. He leaves and after a while doesn't return." )
                print( "" )
                runScene()

    #Docks
    elif(scene == "docks"):
            if( command == "go back to city wall" ):
                print( "You go back to the town." )
                print( "" )
                playerScene = "wall_e"
                runScene()
            elif( command == "talk to dockmaster" ):
                print( "The Dockmaster tells you that no boats are for sale or rent right now." )
                print( "" )
                runScene()
            elif( command == "look"):
                print( "The men seem to be drawing staffs in the sand." )
                print( "" )
                runScene()
            elif( command == "steal boat"):
                print( "You outrun the large dockmaster easily, and board a boat. It catches the wind, and you sail off, leaving Pithon to a mysterious fate." )
            elif( command == "approach men"):
                print( "The men offer some potions for gold." )
                scenes["docks"]["commands"].append("buy potion");
                print( "" )
                runScene()
            elif( command == "buy potion"):
                if "gold" in inventory:
                    print( "You buy a potion of hiding." )
                    inventory.remove("gold")
                    inventory.append("potion")
                    scenes["final_battle"]["commands"].append("drink potion");
                else:
                    print("You have no gold to give.")
                print( "" )
                runScene()
    #Final Battle
    elif(scene == "final_battle"):
        if( command == "attack mage" ):
            print("You run towards the Mage, and swing your sword.")
            print("")
            hitMage = randint(1,4)
            print("You deal " + str(hitMage) + " damage!")
            print("")
            print("The Mage swings his staff, and bludgeons you.")
            hitPlayer = randint(3,6)
            print("")
            print("The Mage deals " + str(hitPlayer) + " damage!")
            print("")
            playerHealth = playerHealth - hitPlayer
            MageHealth = MageHealth - hitMage
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the Mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif( command == "leave" ):
            print( "You attempt to leave, but the Mage stops you." )
            print("")
            print("The Mage swings his staff, and bludgeons you.")
            hitPlayer = randint(1,5)
            print("")
            print("The Mage deals " + str(hitPlayer) + " damage!")
            print("")
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the Mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif(command == "throw knife"):
            print("You throw your knife like a boss!")
            knifeHit = randint(4,8)
            print("")
            print("You deal " + str(knifeHit) + " damage! And the Mage is on fire!")
            print("")
            print("The Mage swings his staff, and bludgeons you.")
            hitPlayer = randint(1,2)
            print("")
            print("The Mage deals " + str(hitPlayer) + " damage!")
            print("")
            playerHealth = playerHealth - hitPlayer
            MageHealth = MageHealth - knifeHit
            inventory.remove("magical knife")
            scenes["final_battle"]["commands"].remove("throw knife");
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the Mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif(command == "draw lines with chalk"):
            print("A demonic beast is summoned and shoots lightning at the Mage, before dissapearing.")
            print("")
            chalkHit = randint(5,10)
            MageHealth = MageHealth - chalkHit
            print("The beast deals " + str(chalkHit) + " damage!")
            print("")
            print("The Mage swings his staff, and bludgeons you.")
            hitPlayer = randint(1,2)
            print("")
            print("The Mage deals " + str(hitPlayer) + " damage!")
            print("")
            playerHealth = playerHealth - hitPlayer
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the Mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif(command == "flip a silver piece"):
            print("You flip your silver pieces in the air. How stupid. This gives the Mage enough time to hit you.")
            silverhit = randint(3,6)
            print("")
            print("The Mage deals " + str(silverhit) + " damage!")
            playerHealth = playerHealth - silverhit
            print("")
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif(command == "drink potion"):
            print("You drink the potion, and become invisible. You sneak around behind the mage, and attack with your sword!")
            print("")
            potionHit = randint(3,8)
            print("You deal " + str(potionHit) + " damage!")
            print("")
            MageHealth = MageHealth - potionHit
            inventory.remove("potion")
            scenes["final_battle"]["commands"].remove("drink potion");
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
        elif(command == "pray"):
            print("You pray for a second, and a beam of light shines into the warehouse. Doves come and attack the Mage!")
            doveHit = randint(8,12)
            print("")
            MageHealth = MageHealth - doveHit
            print("The doves deal " + str(doveHit) + " damage!")
            print("")
            print("The Mage swings his staff, and bludgeons you.")
            hitPlayer = randint(1,2)
            print("")
            print("The Mage deals " + str(hitPlayer) + " damage!")
            print("")
            playerHealth = playerHealth - hitPlayer
            if MageHealth > 0:
                runScene()
            else:
                print("You have defeated the mage, he disappears in a fade of light, and you leave. You have become the Protector of Pithon.")
    else:
        print( "Scene not found, error." )

# The opening description for the game, along with some simple instructions
print("Welcome to Pithon!\n\nYou attend a famous duel in the city of Pithon. During the duel of a Famouse Mage and the Leader of the Red Knights, they both dissapear! Onlookers are shocked!\n\nYou notice a group of hooded figures depart, but you don't know where...\n\nYou also see a sad looking man head to the north.")
print( "" )
print("Your friend, Criaf, heads back to the east.")
print( "" )
print( "If you need help at any time, type help.")
print( "" )
print( "If you need to view your inventory, type inventory.")
print( "" )

# Let's go right into the game, this function is recursive and will keep calling itself until we win or lose
runScene()

# We broke out of the "game loop" so let's output the final score
print( "Thanks for playing!" )
