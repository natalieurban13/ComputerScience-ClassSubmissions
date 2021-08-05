"""CSCI 1106 Assignment 4: Iterated Prisoner's Dilemma

Author: Natalie Urban
A program using one of the fundamental game theories of prisoner's dilemma that impliments a tournament using different strategies."""

import random
random.seed(31337)

##########################################################################
#
# Increase these symbolic constants when you implement
# the associated Prisoner subclasses.
#
##########################################################################

NUM_COOPERATOR = 0
NUM_DEFECTOR = 0
NUM_TITFORTAT = 0
NUM_GRIMTRIGGER = 0
NUM_COINFLIPPER = 0
NUM_DIEROLLER = 0

POINTS_BOTH_COOPERATE = 1
POINTS_BOTH_DEFECT = 0
POINTS_BETRAYER = 2
POINTS_BETRAYED = -1

GAMES_PER_MATCH = 200

##########################################################################
#
# The main code takes in the number of each prisoner strategies, adds them
# to a list of prisoners, and calls them to their separate sub-classes. Each
# prisoner is played against every other prisoner in the list and their points
# are added until the number of games has ended. The results of the scores are
# sorted and printed.
#
##########################################################################

def main():
    the_dilemma = Dilemma(POINTS_BOTH_COOPERATE,POINTS_BOTH_DEFECT,POINTS_BETRAYER,POINTS_BETRAYED)

    prisoners = []
    for i in range(NUM_COOPERATOR):
        prisoners.append(Cooperator())
    for i in range(NUM_DEFECTOR):
        prisoners.append(Defector())
    for i in range(NUM_TITFORTAT):
        prisoners.append(TitForTat())
    for i in range(NUM_GRIMTRIGGER):
        prisoners.append(GrimTrigger())
    for i in range(NUM_COINFLIPPER):
        prisoners.append(CoinFlipper())
    for i in range(NUM_DIEROLLER):
        prisoners.append(DieRoller())
        
        
    for i in range(len(prisoners)):
        for j in range(i+1,len(prisoners)):
            the_dilemma.play(prisoners[i],prisoners[j],GAMES_PER_MATCH)

    print("\n****RESULTS****")
    for prisoner in sorted(prisoners,reverse=True):
        print(prisoner)

##########################################################################
#
# This is the main parent class, which holds all of the basic methods for
# the prisoner strategy sub-classes. It initializes prisoner's points and names,
# updates prisoner points after each round, contains a reset function to be
# overridden in the future, returns name and point variables, compares
# points as lesser than or greater to and equal, and gives a string of individual
# prisoner names and points to the user.
#
##########################################################################

class Prisoner:

    def __init__(self):
        self.prisoner_points = 0
        self.prisoner_name = ""
    
    def update(self, last_betrayal, last_points_earned):
        self.prisoner_points = self.prisoner_points + last_points_earned
        
    def match_reset(self):
        pass
    
    def get_name(self):
        return self.prisoner_name
        
    def get_points(self):
        return self.prisoner_points
    
    def __lt__(self, other):
        if self.prisoner_points < other.prisoner_points:
            return True
        else:
            return False
        
    def __ge__(self, other):
        if self.prisoner_points >= other.prisoner_points:
            return True
        else:
            return False
    
    def __str__(self):
        return f"{self.prisoner_name}: {self.prisoner_points} points"

##########################################################################
#
# Class cooperator returns false and therefore, cooperates during every match
# regardless of what its opponent does. __init__ function returns the iterated players'
# names and adds them to a list to be retrieved by get_name in the parent class.
# The play function utilizes the class strategy by always cooperating.
#
##########################################################################

class Cooperator(Prisoner):
    cooperators = []
    
    def __init__(self):
        super().__init__()
        count = len(self.cooperators) + 1
        self.prisoner_name = "Cooperator " + str(count)
        self.cooperators.append(self.prisoner_name)
        
    def play(self):
        return False

##########################################################################
#
# Class defector returns true and therefore, defects during every match
# regardless of what its opponent does. __init__ function returns the iterated players'
# names and adds them to a list to be retrieved by get_name in the parent class.
# The play function utilizes the class strategy by always defecting.
#
##########################################################################

class Defector(Prisoner):
    defectors = []
    
    def __init__(self):
        super().__init__()
        count = len(self.defectors) + 1
        self.prisoner_name = "Defector " + str(count)
        self.defectors.append(self.prisoner_name)
        
    def play(self):
        return True

##########################################################################
#
# Class Tit for Tat cooperates during the first game of every match, then
# plays whatever its oppenent played in the last match for its subsequent game.
# It overrides match_reset in the parent class to always start each
# game by cooperating, then the update function changes the betrayal instance
# variable to what its opponent's last move was. Play utilizes the instance variable
# and update's affect or lack of affect on it.
#
##########################################################################

class TitForTat(Prisoner):
    tit_for_tats = []
    
    def __init__(self):
        super().__init__()
        count = len(self.tit_for_tats) + 1
        self.prisoner_name = "Tit For Tat " + str(count)
        self.tit_for_tats.append(self.prisoner_name)
    
    def match_reset(self):
        self.last_betrayal = False
    
    def update(self, last_betrayal, last_points_earned):
        super().update(last_betrayal, last_points_earned)
        self.last_betrayal = last_betrayal

    def play(self):
        if self.last_betrayal == False:
            return False
        else:
            return True
    
##########################################################################
#
# Class Grim Trigger cooperates during the first game of every match and every match
# until its oppenent defects. Then Grim Trigger will defect for the remainder of the match.
# It overrides match_reset in the parent class to always start and continue each
# game cooperating. Then update checks if player defected in last game and changes
# the classes strategy to defect once defected. Play utilizes the instance variable
# and update's affect or lack of affect on it.
#
##########################################################################
    
class GrimTrigger(Prisoner):
    grim_triggers = []
    
    def __init__(self):
        super().__init__()
        count = len(self.grim_triggers) + 1
        self.prisoner_name = "Grim Trigger " + str(count)
        self.grim_triggers.append(self.prisoner_name)
    
    def match_reset(self):
        self.current_betrayal = False

    def update(self, last_betrayal, last_points_earned):
        super().update(last_betrayal, last_points_earned)
        if last_betrayal == True:
            self.current_betrayal = True
        else:
            pass

    def play(self):
        if self.current_betrayal == False:
            return False
        else:
            return True

##########################################################################
#
# Class Coin Flipper uses random to pick a random number. The function returns
# true and defects if the number is less then 0.5, or returns false and cooperates
# if the number is greater than 0.5. 
#
##########################################################################

class CoinFlipper(Prisoner):
    coin_flippers = []
    
    def __init__(self):
        super().__init__()
        count = len(self.coin_flippers) + 1
        self.prisoner_name = "Coin Flipper " + str(count)
        self.coin_flippers.append(self.prisoner_name)
        
    def play(self):
        if random.random() < 0.5:
            return True
        else:
            return False

##########################################################################
#
# Class Die Roller uses random to pick a random number. The function returns
# true and defects if the number is less then 1/6 and returns false and cooperates
# if the number is greater than 1/6.
#
##########################################################################

class DieRoller(Prisoner):
    die_rollers = []
    
    def __init__(self):
        super().__init__()
        count = len(self.die_rollers) + 1
        self.prisoner_name = "Die Roller " + str(count)
        self.die_rollers.append(self.prisoner_name)
        
    def play(self):
        if random.random() < 1/6:
            return True
        else:
            return False
    
##########################################################################
#
# Class Dilemma starts each match with a call to reset, then retrieves points.
# Dilemma takes in the player's choice and returns it to the parent class's update
# function. Points are then retrieved and printed with the prisoner names.
#
##########################################################################

class Dilemma:

    def __init__(self,both_coop_outcome,both_defect_outcome,betrayer_outcome,betrayed_outcome):
        self.both_coop_outcome = both_coop_outcome
        self.both_defect_outcome = both_defect_outcome
        self.betrayer_outcome = betrayer_outcome
        self.betrayed_outcome = betrayed_outcome

    def play(self,player1,player2,num_games):

        # some Prisoner classes track information from game to game
        # ensure this information is wiped clean at the start of each match
        player1.match_reset()
        player2.match_reset()

        # take note of each player's points at the start of each match
        # so that we can calculate how many points were won/lost by both players
        player1_starting_score = player1.get_points()
        player2_starting_score = player2.get_points()

        for i in range(num_games):
        
            player1_choice = player1.play()
            player2_choice = player2.play()

            # if A defects...
            if player1_choice:
                # ...and so does B
                if player2_choice:
                    player1.update(True,self.both_defect_outcome)
                    player2.update(True,self.both_defect_outcome)
                # ...and player B cooperates
                else:
                    player1.update(False,self.betrayer_outcome)
                    player2.update(True,self.betrayed_outcome)
            # if A cooperates...
            else:
                # ...and B defects
                if player2_choice:
                    player1.update(True,self.betrayed_outcome)
                    player2.update(False,self.betrayer_outcome)
                # ...and so does B
                else:
                    player1.update(False,self.both_coop_outcome)
                    player2.update(False,self.both_coop_outcome)

        # compare the starting scores we noted to the ending scores and print
        # a short description of the outcome
        player1_ending_score = player1.get_points()
        player2_ending_score = player2.get_points()
        change_in_player1_score = player1_ending_score-player1_starting_score
        change_in_player2_score = player2_ending_score-player2_starting_score
        print(f"{player1.get_name()} ({change_in_player1_score}) vs. {player2.get_name()} ({change_in_player2_score})")

if __name__ == "__main__":
    main()
