'''
	File 		: 	Hangman_GUI.py
	Desc 		: 	A Commmand Line/ GUI based Hangman kind of game which takes choice of word size, max character 
					help required which will be displayed at random positions in the word.
	Arguments	: 	File containing words to be picked from [Command Line Argument]
	File Format	: 	One word on each line
	Created 	: 	25-08-2016
	Author 	: 	Siddhesh Nachane
	Run Command	:	python Hangman_GUI.py <filename>
'''

from tkinter import *
import sys
from random import randint

class Hangman:
    # Initialise the Game
    def __init__(self, master, helpC, word):
        self.maxHelp = helpC
        self.puzzleWord = word
        self.wrongAttempts = 0
        self.currWord = ['-' for i in range(0, len(self.puzzleWord))]
        self.locNotGuessed = [i for i in range(0, len(self.puzzleWord))]
        self.characters = [chr(x) for x in range(ord('A'), ord('Z') + 1)]		#possible input characters
        self.gameOver = False

        # Creating a Blank Canvas for Displaying HangMan (Geometric Objects)
        self.canvas = Canvas(master, width=350, height=300)
        self.canvas.pack(side='left')

        # Creating a Frame for Displaying the Interactive Options
        self.frame = Frame(master, width=455, height=300)
        self.frame.pack(side='left')

        self.winStat = StringVar()
        self.wordStat = StringVar()
        self.wordStat.set(self.currWord)

		# Label to display Win/Loss Status and Current Word Staus
        self.winStatus = Label(self.frame, textvariable=self.winStat)
        self.winStatus.grid(row=0, columnspan=2)
        self.wordStatus = Label(self.frame, textvariable=self.wordStat)
        self.wordStatus.grid(row=1, columnspan=2)

        self.choiceLabel = Label(self.frame, text='Select a Letter').grid(row=2)
		# Listbox displaying available letter choices
        self.letterChoice = Listbox(self.frame)
        self.letterChoice.grid(row=3)
        for c in self.characters: self.letterChoice.insert(END, c)

        self.helpLabel = Label(self.frame, text='Help / Choice').grid(row=2, column=1)
		# Listbox dispalying chosen and helped letters
        self.helpedChar = Listbox(self.frame)
        self.helpedChar.grid(row=3, column=1, padx=25)

        self.submit = Button(self.frame, text='Submit')
        self.submit.bind("<Button-1>", self.clicked)
        self.submit.grid(row=4, pady=10)

        self.canvas.create_line(65, 285, 260, 285)
        self.canvas.create_line(260, 285, 260, 7)
        self.canvas.create_line(260, 7, 130, 7)
        self.canvas.create_line(130, 7, 130, 33)

    def clicked(self, event):
        if not self.gameOver: self.gameLogic()

    # Main Game Logic
    def gameLogic(self):
        # Selection and Removal of Selected Letter in the GUI
        char = self.letterChoice.get('active')
        self.letterChoice.delete('active')
        self.characters.remove(char)

        # Check if the Selected Character is present in the Puzzle Word
        if char in self.puzzleWord:
            for i in range(0, len(self.puzzleWord)):
                if char == self.puzzleWord[i]:
                    self.currWord[i] = char  # Update the Current Word with the Selected Character
                    self.locNotGuessed.remove(i)
            self.helpedChar.insert(END, 'Choice : ' + char)

        else:
            # If Wrong Character is selected update Wrong Attempts
            self.wrongAttempts = self.wrongAttempts + 1
            self.updateHangman()
            # Give Help when Wrong Character is Selected
            if (self.maxHelp > 0):
                self.maxHelp = self.maxHelp - 1
                # Selecting a Random Character from the Puzzle Word to give as a HINT
                randomLoc = self.locNotGuessed[randint(0, len(self.locNotGuessed) - 1)]
                temp = self.puzzleWord[randomLoc]
                ind = self.characters.index(temp)
                self.characters.remove(temp)
                self.letterChoice.delete(ind)
                # Update the Current Word with the Helped Character
                for i in range(0, len(self.puzzleWord)):
                    if temp == self.puzzleWord[i]:
                        self.currWord[i] = temp
                        self.locNotGuessed.remove(i)
                self.helpedChar.insert(END, 'Choice : ' + char + ' -- Help : ' + temp)  # Update the GUI
            else:
                self.helpedChar.insert(END, 'Choice : ' + char)  # Update the GUI
        self.updateStatus()

    def updateStatus(self):
        self.wordStat.set(''.join(self.currWord))
        if ('-' not in self.currWord):  # Check if the Puzzle Word is Guessed Correctly
            self.winStat.set('Hurray!.. You Guessed it Correct')
            self.gameOver = True

    def updateHangman(self):  # Update the Canvas with the Hangman on every wrong Attempt
        if (self.wrongAttempts == 1): head = self.canvas.create_oval(98, 33, 162, 98)
        if (self.wrongAttempts == 2): body = self.canvas.create_line(130, 98, 130, 195)
        if (self.wrongAttempts == 3): arm1 = self.canvas.create_line(130, 145, 98, 195)
        if (self.wrongAttempts == 4): arm2 = self.canvas.create_line(130, 145, 162, 195)
        if (self.wrongAttempts == 5): leg1 = self.canvas.create_line(130, 195, 98, 260)
        if (self.wrongAttempts == 6):
            leg2 = self.canvas.create_line(130, 195, 162, 260)
            self.winStatus.foreground = 'red'
            self.winStat.set(
                'Oops... You Lost!! The Word was {0}.'.format(''.join(self.puzzleWord)))  # Display Loosing Status
            self.gameOver = True


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
puzzleword = list(words[randint(0, len(words) - 1)])

# Check if the Input is Valid
maxhelp = input('Enter Maximum Character Help required : ')
while not maxhelp.isdigit(): maxhelp = input('Error: Please Enter a valid Integer : ')
maxhelp = int(maxhelp)

# Maximum Help should be less than 40% of the length of Word
while (maxhelp > int(2 * len(puzzleword) / 5)):
    maxhelp = input('Please enter a lesser number : ')
    while not maxhelp.isdigit(): maxhelp = input('Error: Please Enter a valid Integer : ')
    maxhelp = int(maxhelp)

print ('****Game Started****')

root = Tk()
root.title('Hangman')
hangman = Hangman(root, maxhelp, puzzleword)
root.mainloop()
