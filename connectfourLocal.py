# Jordan Stein
# connectfour.py
# Python 2.7

# This program simulates a game of connect four using a 
# naive AI (one that makes random moves) and a smart AI (one that makes optimal moves)
# Each smart move is determined using a heuristic function to calculate optimal moves.

import sys
import json
import copy
import random

# Adds desired move to the grid
def addMove(grid, move, player):
	if grid[move][len(grid[move])-1] == 0: # if its the first move, store it
		grid[move][len(grid[move])-1] = player
		return
	else:
		for x in range(0,len(grid[move])-1): # else look for next available spot
			if (grid[move][x+1] != 0):
				grid[move][x] = player
				return


# removes desired move to the grid (for smart AI heuristic calculation)
def removeMove(grid, move, player):
	for x in range(0, len(grid[move])):
		if (grid[move][x] == player): # find most recent move, make it empty
			grid[move][x] = 0 
			return


# generates a random number from 0 to height
def randomMove(height):
	return random.randint(0,height)


# prints the grid to the output prettily
def drawGrid(grid, height, width, moveCount):
	print "--- Move",moveCount,"---"
	for x in range(0, height):
		row = ""
		for y in range(0, width):
			row += str(grid[y][x]) + " "

		print row.replace("0"," ")


# traverses through the grid to determin if any win conditions are met
def checkWin(grid, height, width):
	#check vertical win
	for x in range(0, width):
		for y in range(0, height-3):
			if grid[x][y] == 1 and grid[x][y+1] == 1 and grid[x][y+2] == 1 and grid[x][y+3] == 1:
				return True, 1
			if grid[x][y] == 2 and grid[x][y+1] == 2 and grid[x][y+2] == 2 and grid[x][y+3] == 2:
				return True, 2

	#check horizontal win
	for x in range(0,width-3):
		for y in range(0, height):
			if grid[x][y] == 1 and grid[x+1][y] == 1 and grid[x+2][y] == 1 and grid[x+3][y] == 1:
				return True, 1
			if grid[x][y] == 2 and grid[x+1][y] == 2 and grid[x+2][y] == 2 and grid[x+3][y] == 2:
				return True, 2

	#check diagonal win
	for x in range(0, width-3):
		for y in range(0, height-3):
			# diagonal right
			if grid[x][y] == 1 and grid[x+1][y+1] == 1 and grid[x+2][y+2] == 1 and grid[x+3][y+3] == 1:
				return True, 1
			if grid[x][y] == 2 and grid[x+1][y+1] == 2 and grid[x+2][y+2] == 2 and grid[x+3][y+3] == 2:
				return True, 2
			# diagonal left
			if grid[x][y] == 1 and grid[x-1][y-1] == 1 and grid[x-2][y-2] == 1 and grid[x-3][y-3] == 1:
				return True, 1
			if grid[x][y] == 2 and grid[x-1][y-1] == 2 and grid[x-2][y-2] == 2 and grid[x-3][y-3] == 2:
				return True, 2
	return False, 0



# heuristic function.
# calculates/returns the "worth" of placing a potential move on the grid (smart AI)
def heuristic(grid, move, player):
	addMove(grid, move, player) # temporarily add move

	maximum = 0
	counter = 0

	#check vertical max
	for x in range(0, width):
		counter = 0
		for y in range(0, height-3):
			counter = 0
			if grid[x][y] == player:
				counter += 1 
				if grid[x][y+1] == player:
					counter += 1
					if grid[x][y+2] == player:
						counter += 1
						if grid[x][y+3] == player:
							counter += 1
			if counter > maximum:
				maximum = counter

	counter = 0
	# check horizontal max right scan
	for x in range(0, width-3):
		counter = 0
		for y in range(0, height):
			counter = 0
			if grid[x][y] == player:
				counter += 1
				if grid[x+1][y] == player:
					counter += 1
					if grid[x+2][y] == player:
						counter += 1 
						if grid[x+3][y] == player:
							counter += 1
			if counter > maximum:
				maximum = counter

	counter = 0
	# check horizontal max left scan
	for x in xrange(width-4, 0, -1):
		counter = 0
		for y in range(0, height):
			counter = 0	
			if grid[x][y] == player:
				counter += 1
				if grid[x+1][y] == player:
					counter += 1
					if grid[x+2][y] == player:
						counter += 1 
						if grid[x+3][y] == player:
							counter += 1
			if counter > maximum:
				maximum = counter

	counter = 0
	# check diagonal max
	for x in range(0, width-3):
		counter = 0
		for y in range(0, height-3):
			counter = 0
			# diagonal right max
			if grid[x][y] == player:
				counter += 1
				if grid[x+1][y+1] == player:
					counter += 1 
					if grid[x+2][y+2] == player:
						counter += 1
						if grid[x+3][y+3] == player:
							counter += 1
			if counter > maximum:
				maximum = counter

			counter = 0

			# diagonal left max
			if grid[x][y] == player:
				counter += 1
				if grid[x-1][y-1] == player:
					counter += 1
					if grid[x-2][y-2] == player:
						counter += 1
						if grid[x-3][y-3] == player:
							counter += 1
			if counter > maximum:
				maximum = counter

	removeMove(grid, move, player) # remove the added move after heuristic calculations
	return maximum


def playGame():
	global player1wincount, player2wincount

	height = 6
	width = 7
	grid = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
	player = 1
	move = 0

	moveCount = 0


	win = False
	while (not win):
		# Player 1 (naive AI)
		validMove = False
		moveList = [] # will store all moves we have attempted
		while not validMove:
			randMove = randomMove(height); # generates a random move
			if randMove not in moveList: # add the random move to the list if it is unique
				moveList.append(randMove)
			
			if len(moveList) == 6: # all moves possible = valid move
				break

			if grid[randMove][0] == 0: # top move unused = valid move
				break
			else:
				validMove = False

		moveList[:] = []

		addMove(grid, randMove, 1)
		moveCount+=1
		if not manygames:
			drawGrid(grid, height, width, moveCount)

		win, winner = checkWin(grid, height, width)
		if win:
			break

		# Player 2 (smart AI)
		hMax = 0 # heuristic max
		for x in range(0, width):
			if grid[x][0] == 0: # if the move is valid
				hVal = heuristic(grid, x, 2)
				if hMax < hVal: # once we found the maximum heuristic value
					hMax = hVal # save it as the best move
					bestMove = x

		# if we do not have a win condition, lets check if the opponent is close to one			
		if hMax != 4:
			for x in range(0, width):
				if grid[x][0] == 0: # if the move is valid
					opponentHeuristicVal = heuristic(grid,x,1)
					if opponentHeuristicVal >= 3:
						bestMove = x  # if opponent is close to a win condition, block their path
					if opponentHeuristicVal == 4: # if opponent has a win condition, crush their dreams
						break

		addMove(grid, bestMove, 2)
		moveCount+=1
		if not manygames:
			drawGrid(grid, height, width, moveCount)

		win, winner = checkWin(grid, height, width)
		if win:
			break

	if win:
		if not manygames:
			print "Player",winner,"wins."
		else:
			if winner == 2:
				player2wincount+=1
			else:
				player1wincount+=1
	else:
		print "Stalemate" # final build does not stalemate.


print "This program simulates a game of Connect-Four using a naive AI (one that makes random moves) \nand a smart AI (one that makes optimal moves). Each smart move is determined using a heuristic \nfunction to calculate optimal moves.    Player 1 = naive AI     Player 2 = smart AI"
print "\nPlease input your option (1/2): "
print "1 Simulate one game of connect four."
print "2 Simulate many games, view results."

manygames = input()
gameCount = 0
height = 6
width = 7
grid = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
player = 1
move = 0

if manygames == 2:
	manygames = True
else:
	manygames = False

if manygames:
	gameCount = int(raw_input("How many games would you like to simulate: "))

player1wincount = 0
player2wincount = 0

if not manygames:
	playAgain = "y"
	while (playAgain.lower() == "y"):
		playGame()
		playAgain = raw_input("\nWould you like to simulate another game (y/n): ")

else:
	for z in range(0, gameCount): # simulate number of games requested
		playGame()

	print "Player 1 (naive AI) win count:",player1wincount
	print "Player 2 (smart AI) win count:",player2wincount
	print "smart AI winrate = ", (float(player2wincount)/float(gameCount))*100,"%"