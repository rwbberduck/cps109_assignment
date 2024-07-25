"""
Mastermind Game in Python:

As a university student who definitely has a lot of spare time on their hands, I have a problem with killing time
instead of studying or doing other assignments. To solve this issue, I have decided to create a game using python, based
on the game "Mastermind." It is a puzzle board game where you must decipher a 4 colour sequence in the right order.
If a colour is in the exact correct spot, it will be marked with an "O", if a colour is correct but in the wrong spot,
it will be marked with a "V", and if the colour is completely wrong, it will be marked with an "X". There is an easy
mode, where the correct/incorrect output list is in the exact same order, and there is a hard mode, where the user
doesn't know which specific colours are particularly correct. The game can be played with one or two players; if there
is only one player, it will randomly generate a sequence (with or without duplicates based on user input), but if the
two player option is chosen, one player will get to choose the sequence (with or without duplicates based on user
input).

The expected inputs are based on the prompts given: the 4 options for settings and then to enter a guess for the
sequence. The output should return a list of the user inputted guess beside a list of consisting of "O", "V", and "X"
based on if the guessed colours are correct or not. If the user does not solve the sequence within the amount of turns
they set, the game is over. If they successfully guess the sequence within the given amount of turns, it prints a
congratulation message, and writes the score of the user in a txt file.
"""
# importing random library
import random

def get_random_sequence(filename):
    """
    Function that reads a line of the file (sequence) then returns it
    """
    with open(filename, "r") as file:
        sequence = file.readlines()
        return random.choice(sequence).strip()

def new_score(name, score, turns, filename, difficulty):
    """
    Function to save how many turns it took the user to solve the sequence (if they did)
    """
    with open(filename, "a") as file:
        file.write(f"{name}'s number of tries: {score} out of {turns} turns on difficulty {difficulty}\n")

def mastermind():
    """
    Mastermind game main function
    """
    # welcome statement
    print("------------------------")
    print('Welcome to Mastermind!'.center(24))
    print("------------------------")

    # next 30 lines are settings related
    print("\nSettings:")

    # determine amount of players participating
    players = str(input("How many players: 1 or 2... "))
    while players.isdigit() is False:
        players = str(input("Invalid input, how many players: 1 or 2... "))
    players = int(players)
    while players > 2 or players <= 0:
        try:
            players = int(str(input("Error! How many players: 1 or 2... ")))
        except ValueError:
            print("Please enter an integer!")

    # easy or hard mode (easy wiil reveal which are in right position, hard will not)
    difficulty = str(input("Choose your difficulty: Easy or Hard... ")).lower()
    # checking if input is valid
    while not (difficulty == "easy" or difficulty == "hard"):
        difficulty = str(input("Invalid input, choose your difficulty: Easy or Hard... ")).lower()

    # turn on/off duplicates in the sequence
    filename = None
    duplicates = str(input("Duplicates on or off... ")).lower()
    while not (duplicates == "on" or duplicates == "off"):
        duplicates = str(input("Invalid input, duplicates on or off... ")).lower()
    if duplicates == "on":
        filename = "sequences.txt"  # txt file with all 1296 sequences
    elif duplicates == "off":
        filename = "sequences_no_dupes.txt"  # txt with no duplicate colours in the sequence

    # setting the number of turns
    # ensuring input is an integer and is within the limit
    turns = (input("Please enter the amount of turns you'd like (max: 15)... "))
    while turns.isdigit() is False:
        turns = (input("Invalid input, please enter the amount of turns you'd like (max: 15)... "))
    turns = int(turns)
    while turns > 15 or turns <= 0:
        try:
            turns = int(input("Error, please enter the amount of turns you'd like (max: 15)... "))
        except ValueError:
            print("Please enter an integer!")
    total_turns = turns

    # list of available colours
    colours = ['red', 'blue', 'yellow', 'green', 'black', 'white']

    guess_sequence = []

    # retrieve sequence and turn it into a list if one player
    if players == 1:
        guess_sequence = (get_random_sequence(f"{filename}")).split(",")
    # if two players, let one player enter a sequence
    if players == 2:
        print("\nPlayer 2 please enter 4 colours for the sequence")
        guess_sequence = []
        for i in range(1, 5):
            user_guess_sequence = (input(f"Enter colour number {i} of 4... ").lower())
            while user_guess_sequence not in colours:
                user_guess_sequence = (input(f"Invalid colour, please enter colour number {i} of 4... ").lower())
            # ensure duplicate inputs are allowed or not
            if duplicates == "off":
                while user_guess_sequence in guess_sequence:
                    user_guess_sequence = (input(f"No duplicate colours, enter colour number {i} of 4... ").lower())
            guess_sequence.append(user_guess_sequence)

    score = 0

    print("\nGame will now start!")
    print("The available colours are: red, blue, yellow, green, white, black\n")
    if players == 2:
        print("\n"*15)

    # while loop to help track how many turns has been taken
    while turns > 0:

        # to avoid loop going over the same colours again
        dupe_guess_sequence = guess_sequence[:]
        check_guess_list = []

        # input for the 4 colours for their guess
        print("Please enter 4 colours for your sequence")
        guess = []
        for i in range(1, 5):
            guess_colour = (input(f"Enter colour number {i} of 4... ").lower())
            # if the input is not a valid colour, it makes them try again
            while guess_colour not in colours:
                guess_colour = (input(f"Invalid colour, please enter colour number {i} of 4... ").lower())
            guess.append(guess_colour)

        # if easy
        # for each placeholder, if it is right print "O", if it is the right colour print "V", else print "X"
        for i in range(len(guess)):
            # checks if the guess is in the right place
            if guess[i] == guess_sequence[i]:
                check_guess_list.append("O")
                dupe_guess_sequence.remove(guess[i])
            else:
                # temporarily puts the guess as wrong
                check_guess_list.append("X")
        for j in range(len(dupe_guess_sequence)):
            for k in range(len(guess)):
                # if the colour is right but not in the correct place
                if guess[k] == dupe_guess_sequence[j]:
                    if check_guess_list[k] != "O":
                        check_guess_list[k] = "V"

        # if easy, the sorter is skipped
        # for each placeholder, if it is right print "O", if it is the right colour print "V", else print "X"
        # if hard
        # print "O", if it is the right colour print "V", else print "X", not in the right order
        # sorts list alphabetically so user doesn't know which colours are exactly correct or not
        if difficulty == "hard":
            check_guess_list.sort()

        # counts how many turns it takes the user to solve
        score += 1

        # check if user's guess is entirely correct
        if guess_sequence == guess:
            print(guess, "=>", check_guess_list)
            print(f'\nHooray! You correctly guessed the sequence in {score} turns')
            new_score(str(input("Enter your name... ")), score, total_turns, "cps109_a1_output.txt", difficulty)
            break

        # if user's guess is still wrong
        # tracks user's guess and how many turns are left
        turns -= 1
        print(guess, "=>", check_guess_list)
        print(f"Turns left: {turns}\n")

    # if user runs out of turns, game is lost
    if turns == 0:
        print("Game over! Better luck next time!")
        print(f"The sequence was: {guess_sequence}")


# calling main function to run code
if __name__ == "__main__":
    mastermind()
