#!/usr/bin/env python3

# proposal for a trump rating function for Doppelkopf
# The core function calculate_trump_power applies the formula  p = (c_q*q + n + c_t*t)/c to calculate the trump rating (p) 
# as weighted sum of trump quality (q), quantity (n) and the number of unbeatable trumps (t). 
# Unbeatable card hands get a trump power of 100 (normalization factor (c) is set accordingly).
# Trump quality is numerically expressed using an arctan-function (details see below).
# main() sets a test frame with randomly assigned cards to four players. The sorted card hands and their respective trump ratings appear in the output.

import sys
import random
import math

def get_trump(cards_list, special_solo):
    # translates lists of numeric values into list of strings (for readability of code and output) and
    # discard non-trump cards from cards_list for the respective special_solo type
    
    if isinstance(cards_list, list):
    
        s_list = [] # output list
        bock = cards_list.count(2) == 2 # checks for Bock (double HK) on player's hand
    
        for i in cards_list:
            # for each card of cards_list translate numeric value into string abbreviation for card type
            # assign "" to non-trump cards 
        
            if special_solo == "F":
                card = "" # no trump in Fleischlos
            
            elif special_solo == "U":
                # Bubensolo: only Unter matter
                if i == 16:
                    card = "SU"
                elif i == 17:
                    card = "HU"
                elif i == 18:
                    card = "BU"
                elif i == 19:
                    card = "EU"
                else:
                    card = ""  # else no trump
                
            elif special_solo == "O":
                # Obersolo: Ober count 
                if i == 20:
                    card = "SO"
                elif i == 21:
                    card = "HO"
                elif i == 22:
                    card = "BO"
                elif i == 23:
                    card = "EO"
                else:
                    card = ""  # else no trump
                
            else:  # no special solo or Herz-, Blatt- or Eichelsolo
                # Bock, Unter, Ober, Dulle are equal in all cases
                if i == 2 and bock:
                    card = "HK"
                elif i == 16:
                    card = "SU"
                elif i == 17:
                    card = "HU"
                elif i == 18:
                    card = "BU"
                elif i == 19:
                    card = "EU"
                elif i == 20:
                    card = "SO"
                elif i == 21:
                    card = "HO"
                elif i == 22:
                    card = "BO"
                elif i == 23:
                    card = "EO"
                elif i == 24:
                    card = "H10"
                else:
                    # further cards depend on trump color
                    if special_solo == "H":
                        # Herzsolo               
                       if i == 1:
                           card = "H9"
                       elif i == 2:
                           card = "HK"
                       elif i == 3:
                           card = "HA"
                       else:
                           card = ""  # else no trump
            
                    elif special_solo == "B":
                        # Blattsolo
                       if i == 4:
                           card = "B9"
                       elif i == 5:
                           card = "BK"
                       elif i == 6:
                           card = "S10"
                       elif i == 7:
                           card = "BA"
                       else:
                           card = ""  # else no trump
            
                    elif special_solo == "E":
                        # Eichel solo               
                       if i == 8:
                           card = "E9"
                       elif i == 9:
                           card = "EK"
                       elif i == 10:
                           card = "E10"
                       elif i == 11:
                           card = "EA"
                       else:
                           card = ""  # else no trump
         
                    else:
                       # no special solo               
                       if i == 12:
                           card = "S9"
                       elif i == 13:
                           card = "SK"
                       elif i == 14:
                           card = "S10"
                       elif i == 15:
                           card = "SA"
                       else:
                           card = ""  # i < 12 -> no trump
        
            if card != "":
                s_list.append(card) # if card is trump, add it to s_list
        return s_list # return string list
   
    else: # invalid input variables
        print("Type error: bock has to be bool. schweinchen has to be bool. card_list has to be list.")
        return None
    

def calculate_trump_power(card_list, bock, schweinchen, special_solo):
    # calculates the trump rating of card_list, taking into account schweinchen, bock and special_solo rules
    # card_list - list
    # bock - Boolean
    # schweinchen - Boolean
    # special_solo - String
    
    # idea: p = (q + n + t)/c
    # trump power (p) is weighted sum of trump quality (q), quantity of trump cards (n) and the number of unbeatable trump cards (t)
    # divided by normalization factor (c)
    
    if isinstance(card_list, list) and isinstance(bock, bool) and isinstance(schweinchen, bool):
    
        if special_solo == "F":
            power = 0 # no one has trump in Fleischlos
    
        elif special_solo == "U" or special_solo == "O":
            c = 0.25 # normalization constant: trump power should be 100 if player has all Unter/Ober (depends on choices for other parameters)
            c_t = 4 # weight of unbeatable trump
        
            # calculating quality:
            # assumption: exponential increase in quality, relatively low weight, as quantity matters more in Ober-/Untersolo
            q = 0
            for card in card_list:
               if card == "S" + special_solo:
                   q = q + 0.25
               elif card == "H" + special_solo:
                   q = q + 0.5
               elif card == "B" + special_solo:
                   q = q + 1
               elif card == "E" + special_solo:
                   q = q + 2
        
            # determining unbeatable trumps:
            t = card_list.count("E" + special_solo) # Eichelunter/-ober is unbeatable
        
            # blank cards do not count
            if t == len(card_list) and t == 1:
                t = 0
        
            if t == 2: # continue only if player has both EU/EO
                t = t + card_list.count("B" + special_solo)
                if t == 4:
                    t = t + card_list.count("H" + special_solo)
                    if t == 6:
                        t = t + card_list.count("S" + special_solo)
                    
            power = (q + len(card_list) + c_t*t) / c
            
        else:
            # 1) set parameters and normalization constants
            if schweinchen:
                if bock:
                    c = 3.15 # normalization constant: trump power should be 100 if player has all unbeatable trump (depends on choices for other parameters)
                else:
                    c = 2.47
            else:
                if bock:
                    c = 3.13
                else:
                    c = 2.02
            c_t = 4 # weight of unbeatable trump
            c_q = 1 # weight of quality (card of highest quality gets a quality value of 3*c_q,
                    # for comparison: the quantity score is 1 for every card
        
            # 2) calculate trump quality
            # idea: quality is non-linear -> arctan function
            q = 0
            if special_solo == "n":
                pre = "S"
            else:
                pre = special_solo
                
            for card in card_list:
                # determine the argument of the arctangent for card
                if card == pre + "9":
                    arg = -6
                elif card == pre + "K" and not(bock and pre == "H"):
                    arg = -5
                elif card == pre + "10" and pre != "H":
                    arg = -4
                elif card == pre + "A" and not(schweinchen): # should Fuchs get a penalty?
                    arg = -3
                elif card == "SU":
                    arg = -2
                elif card == "HU":
                    arg = -1
                elif card == "BU":
                    arg = 0
                elif card == "EU":
                    arg = 1
                elif card == "SO":
                    arg = 2
                elif card == "HO":
                    arg = 3
                elif card == "BO":
                    arg = 4
                elif card == "EO":
                    arg = 5
                elif card == "HK" and bock:
                    arg = 5.5
                elif card == "H10":
                    arg = 6
                elif card == pre + "A" and schweinchen:
                    arg = 7
                else:
                    arg = 0
                
                q = q + c_q*(math.atan(arg) + 1.5) # arctan ranges from -pi/2 to pi/2 
                # in order to avoid negative values, add 1.5
                # multiply with quality weight c_q
    
            # 3) determine the number of unbeatable trump cards in card_list
        
            # set ordered trump list
            if schweinchen:
                if bock:
                    unbeatable_list = ["SA", "H10", "HK", "EO", "BO", "HO", "SO", "EU", "BU", "HU", "SU", "S10", "SK", "S9"]
                else:
                    unbeatable_list = ["SA", "H10", "EO", "BO", "HO", "SO", "EU", "BU", "HU", "SU", "S10", "SK", "S9"]
            else:
                # no Schweinchen
                if bock:
                    unbeatable_list = ["H10", "HK", "EO", "BO", "HO", "SO", "EU", "BU", "HU", "SU", "SA", "S10", "SK", "S9"]
                else: 
                    unbeatable_list = ["H10", "EO", "BO", "HO", "SO", "EU", "BU", "HU", "SU", "SA", "S10", "SK", "S9"]
                
            # count unbeatable trumps in card_list
            t = 0    
            for u_card in unbeatable_list:
                if card_list.count(u_card) == 2:
                    t = t + 2
                elif u_card == "EO" and card_list.count(u_card) == 1: # special case "EO": other player with EO is team member
                    t = t + 1                                         # therefore, single EO does not count as break in unbeatable row
                else:
                    if card_list.count(u_card) == 1:
                        t = t + 1
                    break # break from for-loop if row of unbeatable cards is disrupted
                   
            
            power = (q * len(card_list) + c_t*t)/c

            if power > 100: # perfect cards = weakest unbeatable card hand, since there are also stronger unbeatable card hands cap power at 100
                power = 100
        return power
    
    else: # invalid input variable types
        print("Type error: bock has to be bool. schweinchen has to be bool. card_list has to be list.")
        return None


def main():
    # define card deck of 24 different cards, ranging from 1 to 24
    card_deck = [i + 1 for i in range(24)]
    # each card type exists twice -> double deck
    card_deck.extend(card_deck)
    # shuffle card deck
    random.shuffle(card_deck)

    # assign cards to players
    player_cards = []
    player_cards.append(card_deck[0:12])  # player 1 gets first 12 cards
    player_cards.append(card_deck[12:24]) # player 2
    player_cards.append(card_deck[24:36]) # player 3
    player_cards.append(card_deck[36:48]) # player 4


    special_rules = ["n", "H", "B", "E", "U", "O", "F"] # n - none, H - Herzsolo, B - Blattsolo, E - Eichelsolo, U - Untersolo, O - Obersolo, F - Fleischlos
    special_solo = "n" # default option is none

    # check for run parameters to use special solo rules
    # sys.argv is the list of arguments given when executing the script
    # e.g. python TrumpRating.py --solo O (The script name ifself is one element of sys.argv.)
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--solo":
            # check argument after "--solo" after for solo type-
            if i < len(sys.argv):
                if sys.argv[i+1] in special_rules:
                    special_solo = sys.argv[i+1]

    # sort players' card hands
    for i in range(4):
        player_cards[i].sort()

    if not(special_solo in ["U", "O", "F"]):
        bock = any(player_cards[i].count(2) == 2 for i in range(4)) # Does anyone has Bock (double HK)?
    else:
        bock = False

    if special_solo == "n":
        schweinchen = any(player_cards[i].count(15) == 2 for i in range(4)) # Does anyone has Schweinchen (double SA)?
    elif special_solo == "H":
        schweinchen = any(player_cards[i].count(3) == 2 for i in range(4)) # Does anyone has Schweinchen (double HA)?
    elif special_solo == "B":
        schweinchen = any(player_cards[i].count(7) == 2 for i in range(4)) # Does anyone has Schweinchen (double SA)?
    elif special_solo == "E":
        schweinchen = any(player_cards[i].count(11) == 2 for i in range(4)) # Does anyone has Schweinchen (double SA)?
    else:
        schweinchen = False

    # print players' card hands and trump power
    for i in range(4):
        print('Spieler ' + str(i + 1) + ': ' + str(get_trump(player_cards[i], special_solo)) + "\n Trumpfstärke: " + str(calculate_trump_power(get_trump(player_cards[i], special_solo), bock, schweinchen, special_solo)))


def normalization(bock, schweinchen, special_solo):
    # returns the trump rating for the least unbeatable hands under the specified options for bock, schweinchen and special_solo
    # bock - Boolean
    # schweinchen - Boolean
    # special_solo - String
    
    if isinstance(bock, bool) and isinstance(schweinchen, bool):
        # normalization decks:
        if special_solo in ["O", "U"]:
            perfect_cards = ["SO", "SO", "HO", "HO" "BO", "BO", "EO", "EO"] # special_solo = "O"	
        else:
            # game modes with usual trump
            if bock and not(schweinchen):
                perfect_cards = ["S9", "S9", "SK", "SK", "BO", "BO", "EO", "EO", "HK", "HK", "H10", "H10"] # with Bock
            elif bock and schweinchen:
                perfect_cards = ["S9", "S9", "SK", "SK", "EO", "EO", "HK", "HK", "H10", "H10", "SA", "SA"] # with Bock and Schweinchen
            elif schweinchen and not(bock):
                perfect_cards = ["S9", "S9", "SK", "SK", "SU", "SU", "EO", "EO", "H10", "H10", "SA", "SA"] # with Schweinchen
            elif not(schweinchen) and not(bock):
                perfect_cards = ["S9", "S9", "SK", "SK", "SA", "SU" "BO", "BO", "EO", "EO", "H10", "H10"] # without Bock and Schweinchen

        return calculate_trump_power(perfect_cards, bock, schweinchen, special_solo)
    else:
        print("Type error: bock has to be bool. schweinchen has to be bool.")
        return None

if __name__ == '__main__':
    # start main() function when the py-file is executed
    main()
