# Import our required libraries and functions
from random import randint
from graphics import *


#####################################################
# main()
#
# Carries out the main functionality of the program 
#####################################################
def main(win, infile_name):
	# If a word list file hasn't yet been sepcified, then we need to get one
	if not(infile_name):
		infile_name = getInfile()

	# Choose a word at random from the acquired word list
	word, word_len = chooseWord(infile_name)

	# Build the grid of empty spaces, one space for each letter of the chosen word
	grid = '__'
	for i in range(word_len - 1):
		grid = grid + ' __'

	# Generate the graphics window for the game's GUI
	win_width = 500
	win_width2 = 400
	win_height = 480
	if not(win):
		# This will only be called on the first play-through of the game, so that
		#	a new window isn't generated each time a player chooses to "play again"
		win = GraphWin("Hangman Simple-Game", win_width, win_height)
		win.setCoords(0, 0, win_width, win_height)

	# Draw the game message area, the ground of the Hangman graphic, and the empty grid
	win_message = Text(Point(win_width / 2, 70), "Let's play! Guess a letter below to see if it's in the word.")
	win_message.setStyle('bold')
	win_message.draw(win)
	win_message2 = Text(Point(win_width2 / 1.60, 457), "Guess the correct word by entering letters.\nThe words are related to useful things at school/university.")
	win_message2.setStyle('bold')
	win_message2.draw(win)
	win_message3 = Text(Point(win_width2 / 1.60, 375), "You have a total of 7 strikes.")
	win_message3.setStyle('bold')
	win_message3.draw(win) 
	win_ground = Line(Point(win_width / 10, 433), Point(win_width - win_width / 10, 433))
	win_ground.draw(win)
	win_ground = Line(Point(win_width / 10, 90), Point(win_width - win_width / 10, 90))
	win_ground.draw(win)
	win_grid = Text(Point(win_width / 2, win_height - 70), grid)
	win_grid.draw(win)

	# Draw the input box and accompanying text label
	win_guesstxt = Text(Point(win_width / 4 - 35, 30), "Type a letter:")
	win_guesstxt.draw(win)
	win_guessinput = Entry(Point(win_width / 4 + 30, 28), 3)
	win_guessinput.draw(win)
	win_guessinput.setText('')

	# Draw the "Guess it!" button and its label
	win_butguess = Rectangle(Point(win_width / 2 + 80, 43), Point(win_width / 2 + 200, 13))
	win_butguess.setFill(color_rgb(126, 236, 53))
	win_butguess.setOutline(color_rgb(0, 110, 0))
	win_butguess.draw(win)
	win_butguess_label = Text(Point(win_width / 2 + 140, 28), 'Guess it!')
	win_butguess_label.setTextColor(color_rgb(0, 110, 0))
	win_butguess_label.draw(win)

	# Now, we keep taking guesses of letters until either the player amounts 7 total strikes (wrong
	#	guesses), or until the player correctly guesses the entire word and the game is won
	strikes = 0
	guessed_letters = []
	win_hangmanpic = []
	game_won = False
	while strikes < 7 and game_won == False:
		# Log the player's mouse click location
		p = win.getMouse()
		# If the player clicked outside of the area of the "Guess it!" button, then we go back to the start
		#	of the loop and wait for another click
		if p.getX() < win_width / 2 + 80 or p.getX() > win_width / 2 + 200 or p.getY() < 13 or p.getY() > 43:
			continue

		# Grab the guessed letter, and if it's invalid, go back to the top of the loop and wait for another guess
		guess = win_guessinput.getText().lower()
		win_guessinput.setText('')
		if guess == ' ' or guess == '' or len(guess) != 1:
			if len(guess) != 1:
				win_message.setText("Please only guess a single letter at a time. Try again!")
			continue

		# If the guessed letter is in the word, and it hasn't been guessed yet by the player, then we update our
		#	grid by placing this letter in the appropriate empty spaces on the grid
		if guess in word.lower() and not(guess in guessed_letters):
			guessed_letters.append(guess)
			grid = word
			for letter in word:
				if (not (letter.lower() in word) or not(letter.lower() in guessed_letters)) and letter != ' ':
					grid = grid.replace(letter, ' __ ')
				
				win_grid.setText(grid)

			if grid == word:
				game_won = True
			else:
				win_message.setText("Nice! {0} is in the word. Try another letter.".format(guess.upper()))
		elif guess in guessed_letters:
			# This letter has already been guessed, so alert the player about this and wait for another guess
			win_message.setText("You've already guessed {0}. Try another letter.".format(guess.upper()))
		else:
			# Wrong guess! Add a strike and draw a new piece of the Hangman picture
			guessed_letters.append(guess)
			strikes = strikes + 1
			win_message.setText('{0} is a wrong guess! Try another letter.'.format(guess.upper()))
			win_message3.setText('This is your strike {0}'.format(strikes)) # This prints to the user or customer the number of strikes have made, when entering a incorrect letter. 
			drawPiece(strikes, win, win_width, win_height, win_hangmanpic)

	# The game is over, so let's remove some of the objects at the bottom of the window
	#	to make room for the "Quit" and "Play Again?" buttons and the final message
	win_guesstxt.undraw()
	win_guessinput.undraw()
	win_butguess.undraw()
	win_butguess_label.undraw()
	win_message.move(0, -10)  # Move the message area down a bit to fill up some space

	# Update the grid to display the full, actual word that the program chose
	win_grid.setText(word.upper())
	win_grid.setStyle('bold')
	win_grid.setSize(16)

	# Change the message at the bottom of the window to reflect a win or loss
	if game_won == True:
		win_message.setText("Congrats! You've guessed the word correctly.")
		win_message.setTextColor(color_rgb(0, 120, 0))
		win_message2.setText("VICTORY!")
		win_message2.setTextColor(color_rgb(0, 120, 0))
		win_message2.setSize(24)
		win_message3.setText("")
		win_grid.setTextColor(color_rgb(0, 120, 0))
		# Remove the incomplete Hangman picture
		for hm_obj in win_hangmanpic:
			hm_obj.undraw()
		win_hangmanpic = []
		# And replace it with a picture that's representative of winning the game
		circle1 = Circle(Point(win_width / 2, 240), 110)
		circle1.setOutline(color_rgb(0, 120, 0))
		circle1.setFill(color_rgb(126, 236, 53))
		circle1.draw(win)
		win_hangmanpic.append(circle1)
		eye1 = Circle(Point(win_width / 2 - 40, 285), 20)
		eye1.setOutline(color_rgb(0, 120, 0))
		eye1.draw(win)
		win_hangmanpic.append(eye1)
		eye2 = eye1.clone()
		eye2.move(80, 0)
		eye2.draw(win)
		win_hangmanpic.append(eye2)
		eye1_inner = Circle(Point(win_width / 2 - 40, 285), 5)
		eye1_inner.setFill(color_rgb(0, 120, 0))
		eye1_inner.setOutline(color_rgb(0, 120, 0))
		eye1_inner.draw(win)
		win_hangmanpic.append(eye1_inner)
		eye2_inner = eye1_inner.clone()
		eye2_inner.move(80, 0)
		eye2_inner.draw(win)
		win_hangmanpic.append(eye2_inner)
		mouth = Circle(Point(win_width / 2, 200), 50)
		mouth.setFill(color_rgb(0, 120, 0))
		mouth.setOutline(color_rgb(0, 120, 0))
		mouth.draw(win)
		win_hangmanpic.append(mouth)
		# Replace the rectangle for a circle and moved up where the original circle is located (mouth).
		mouth_cover = Circle(Point(win_width / 2, 205), 50)
		mouth_cover.setFill(color_rgb(126, 236, 53))
		mouth_cover.setOutline(color_rgb(126, 236, 53))
		mouth_cover.draw(win)
		win_hangmanpic.append(mouth_cover)
	else:
		win_message.setText("Sorry! You didn't completely guess the word.")
		win_message.setTextColor(color_rgb(170, 0, 0))
		win_grid.setTextColor(color_rgb(170, 0, 0))
		win_message2.setText("GAME OVER")
		win_message2.setTextColor(color_rgb(170, 0, 0))
		win_message2.setSize(24)
		win_message3.setText("You've used all your attempts")
		# Added the sad face when player lose the game.
		# Remove the incomplete Hangman picture.
		for hm_obj in win_hangmanpic:
			hm_obj.undraw()
		win_hangmanpic = []
		# And replace it with a picture that's representative of losing the game.
		circle1 = Circle(Point(win_width / 2, 240), 110)
		circle1.setOutline(color_rgb(170, 0, 0))
		circle1.setFill(color_rgb(255, 177, 177))
		circle1.draw(win)
		win_hangmanpic.append(circle1)
		eye1 = Circle(Point(win_width / 2 - 40, 285), 20)
		eye1.setOutline(color_rgb(170, 0, 0))
		eye1.draw(win)
		win_hangmanpic.append(eye1)
		eye2 = eye1.clone()
		eye2.move(80, 0)
		eye2.draw(win)
		win_hangmanpic.append(eye2)
		eye1_inner = Circle(Point(win_width / 2 - 40, 285), 5)
		eye1_inner.setFill(color_rgb(170, 0, 0))
		eye1_inner.setOutline(color_rgb(170, 0, 0))
		eye1_inner.draw(win)
		win_hangmanpic.append(eye1_inner)
		eye2_inner = eye1_inner.clone()
		eye2_inner.move(80, 0)
		eye2_inner.draw(win)
		win_hangmanpic.append(eye2_inner)
		mouth = Circle(Point(win_width / 2, 190), 50)
		mouth.setFill(color_rgb(170, 0, 0))
		mouth.setOutline(color_rgb(170, 0, 0))
		mouth.draw(win)
		win_hangmanpic.append(mouth)
		# Replace the rectangle for a circle and moved down where the original circle is located (mouth).
		mouth_cover = Circle(Point(win_width / 2, 185), 50)
		mouth_cover.setFill(color_rgb(255, 177, 177))
		mouth_cover.setOutline(color_rgb(255, 177, 177))
		mouth_cover.draw(win)
		win_hangmanpic.append(mouth_cover)

	# Draw a button to ask if the player wants to play again
	win_butagain = Rectangle(Point(win_width - 495, 30), Point(win_width, 0))
	win_butagain.setFill(color_rgb(220,220,220))
	win_butagain.setOutline(color_rgb(128,128,128))
	win_butagain.draw(win)
	win_butagain_label = Text(Point(win_width - 250, 15), 'Play again?')
	win_butagain_label.setTextColor(color_rgb(0,0,0))
	win_butagain_label.draw(win)

	# Wait for an option to be selected by the player, then either quit the game or
	#	play another round, based on what button the player clicks
	opt_selected = False
	while not(opt_selected):
		p = win.getMouse()
		if p.getX() >= (win_width - 495) and p.getY() <= 30:
			# Play again
			opt_selected = 1

	# Do something based on the option that was selected
	if opt_selected == 1:
		# Undraw all graphics objects from this game and call another instance of the game
		graphic_objs = [win_message, win_message2, win_message3, win_ground, win_grid, win_butagain, win_butagain_label, win_hangmanpic]
		for obj in graphic_objs:
			if obj == win_hangmanpic:
				for hm_obj in win_hangmanpic:
					hm_obj.undraw()
			else:
				obj.undraw()

		main(win, infile_name)
	else:
		# Close the game window
		win.close()


############################################################################################
# drawPiece()
#
# Draws a piece of the Hangman picture when an incorrect letter is guessed. The piece that 
#	is drawn depends on the number of strikes that the player has amounted thus far		   
############################################################################################
def drawPiece(strike, win, win_width, win_height, win_hangmanpic):
	hangman_yaxis = win_width / 2.2  # The body of the hangman will align with this axis
	if strike == 1:
		# Strike 1: Draw the post
		line1 = Line(Point(win_width - win_width / 3, 100), Point(win_width - win_width / 3, 300))
		line1.draw(win)
		win_hangmanpic.append(line1)
		line2 = Line(Point(win_width - win_width / 3, 300), Point(hangman_yaxis, 300))
		line2.draw(win)
		win_hangmanpic.append(line2)
		line3 = Line(Point(hangman_yaxis, 300), Point(hangman_yaxis, 270))
		line3.draw(win)
		win_hangmanpic.append(line3)
	elif strike == 2:
		# Strike 2: Draw the head
		circle4 = Circle(Point(hangman_yaxis, 254), 16)
		circle4.draw(win)
		win_hangmanpic.append(circle4)
	elif strike == 3:
		# Strike 3: Draw the torso
		line5 = Line(Point(hangman_yaxis, 238), Point(hangman_yaxis, 180))
		line5.draw(win)
		win_hangmanpic.append(line5)
	elif strike == 4:
		# Strike 4: Draw the left arm
		line6 = Line(Point(hangman_yaxis, 225), Point(hangman_yaxis - 20, 200))
		line6.draw(win)
		win_hangmanpic.append(line6)
	elif strike == 5:
		# Strike 5: Draw the right arm
		line7 = Line(Point(hangman_yaxis, 225), Point(hangman_yaxis + 20, 200))
		line7.draw(win)
		win_hangmanpic.append(line7)
	elif strike == 6:
		# Strike 6: Draw the left leg
		line8 = Line(Point(hangman_yaxis, 180), Point(hangman_yaxis - 15, 135))
		line8.draw(win)
		win_hangmanpic.append(line8)
	elif strike == 7:
		# Strike 7: Draw the right leg
		line9 = Line(Point(hangman_yaxis, 180), Point(hangman_yaxis + 15, 135))
		line9.draw(win)
		win_hangmanpic.append(line9)

		
#########################################################################
# getInfile()								
#
# Gets a text file containing words to be chosen by the Hangman program #
#########################################################################
def getInfile():
	try:
		# First, we check for a file called "words.txt". If it exists in the same directory
		#	as the Hangman program, then we use this file as our word list automatically
		with open('words.txt', 'r'): infile_name = 'words.txt'
	except IOError:
		# If words.txt cannot be found, then we ask the user to specify a text file
		found_file = False
		infile_name = input('Please specify a text file containing a list of words for the Hangman game to choose from (include the full file path if the file is in a different directory than the Hangman program): ')
		# If the user specifies a file name of a file that cannot be found, we keep asking for
		#	a valid input file until a valid one is specified
		while not(found_file):
			try:
				with open(infile_name, 'r'): found_file = True
			except IOError:
				infile_name = input('\n{0} was not found!\n\nPlease try again, or specify a different file (include the full file path if the file is in a different directory than the Hangman program): '.format(infile_name))
	return infile_name


############################################################################
# chooseWord()							   #
#
# Chooses a word randomly from the list of words taken from the input file 
############################################################################
def chooseWord(infile_name):
	infile = open(infile_name, 'r')
	wordlist = infile.readlines()
	total_words = len(wordlist)
	random_num = randint(0, total_words - 1)

	chosen_word = wordlist[random_num].replace('\n', '')
	word_len = len(chosen_word)
	return chosen_word, word_len

		
# Start the first instance of the Hangman game
main(False, False)
