'''
	File 		: 	Hangman.py
	Desc 		: 	A Commmand Line based Hangman kind of game which takes choice of word size, max character help required 
					which will be displayed at random positions in the word.
	Arguments	: 	File containing words to be picked from [Command Line Argument]
	File Format	: 	One word on each line
	Created 	: 	25-08-2016
	Author 	: 	Siddhesh Nachane
	Run Command	:	python Hangman.py <filename>
'''

import sys
from random import randint

# Argument Check
if len(sys.argv) < 2:
    print('Error: Argument (File Name) not Found!')
    sys.exit(0)

dataFile = sys.argv[1]

try:
    wordFile = open(dataFile)
except EnvironmentError:
    print('File Error: Specified File Not Found')  # Check if the Specified File is Present or Not
    sys.exit(0)

else:
	# Input an Integer and check if the value is an Integer or not
	puzzleLength = input('Enter the length of Puzzle Word : ')
	while not puzzleLength.isdigit(): puzzleLength = input('Error: Please Enter a valid Integer : ')
	
    # Create a list of all words present in the file and also find each words length
	puzzleLength = int(puzzleLength)
	words = [line.replace('\n', '').upper() for line in wordFile if (len(line.replace('\n', '')) == puzzleLength)]
	wordFile.close()

# Check if the Word of Given Length is present the The File or Not
if len(words) == 0:
    print('Error: Sorry no word of length {0} found in file {1}'.format(puzzleLength, sys.argv[1]))
    sys.exit(0)

# Generate a Random Word from the File
puzzleWord = list(words[randint(0, len(words) - 1)])

# Check if the Input is Valid
# Maximum Help should be less than 40% of the length of Word
maxHelp = input('Enter Maximum Character Help required : ')
while not maxHelp.isdigit(): maxHelp = input('Error: Please Enter a valid Integer : ')
maxHelp = int(maxHelp)

while maxHelp > int(2 * len(puzzleWord) / 5):
    maxHelp = input('Please enter a lesser number : ')
    while not maxHelp.isdigit(): maxHelp = input('Error: Please Enter a valid Integer : ')
    maxHelp = int(maxHelp)

guessed = []    # List of all Guessed Characters
helped = []     # List of all Helped Characters
wrongAttempts = 6  # Max Wrong Attempts in Hangman is 6
currWord = ['-' for i in range(0, len(puzzleWord))]  # Blank Word at Start
locNotGuessed = [i for i in range(0, len(puzzleWord))]  # Remaining Location to be Guessed

while wrongAttempts > 0:
    # Input a Character and Check for Errors
    char = input('\n\n\nGuess a character : ').upper()
    while not (char.isalpha() and len(char) == 1): char = input(
        'Error : Please enter a valid single character : ').upper()

    if char in guessed or char in helped:  # Check if the Character is already Guessed
        print('You have already guessed or have been helped with the character.\n')
        continue

    guessed.append(char)

    # Check if the Character is Present in the Puzzle Word
    if char in puzzleWord:
        for i in range(0, len(puzzleWord)):
            if char == puzzleWord[i]:
                currWord[i] = char
                locNotGuessed.remove(i)

    else:
        # If Character is Not present in the Puzzle Word Decrease the MAX Wrog Attempts and Give Help Character
        wrongAttempts = wrongAttempts - 1
        if (maxHelp > 0):
            maxHelp = maxHelp - 1
            randomLoc = locNotGuessed[randint(0, len(locNotGuessed) - 1)]  # Select a Random Location in the Current Word and Give Help
            temp = puzzleWord[randomLoc]
            for i in range(0, len(puzzleWord)):
                if temp == puzzleWord[i]:
                    currWord[i] = temp
                    locNotGuessed.remove(i)  # After Help Remove the Location from the NotGuessed Field
            helped.append(temp)
	
	#Both guessed and helped lists sorted to make it user readable
    guessed.sort()		
    helped.sort()
	
	#Print the User Status after every input
    print('Your current Status : ')
    print('\tCurrent Guessed String : {0} \n\tCharacters Guessed by you : {1} \n\tCharacters Helped with : {2}'.format(
        ''.join(currWord), guessed, helped))
    print('\tNumber of Help Characters Left : {0} \n\tWrong Attempts Left : {1}'.format(maxHelp, wrongAttempts))

    if '-' not in currWord:
        print('\n\nCongrats..! You Guessed the word right')
        break

else:
    print('\n\nSorry You Lost..!! The Answer was :', ''.join(puzzleWord))
