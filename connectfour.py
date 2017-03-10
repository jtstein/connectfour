# Jordan Stein
# connectfour.py
# Python 2.7

# This program simulates a game of connect four using the provided driver program in racket.
# Information from the grid is read in from the driver, and outputted back to the driver.
# naive AI (one that makes random moves) and a smart AI (one that makes optimal moves)
# Each smart move is calculated using a heuristic function to calculate optimal moves.

# Note, the execution paths for the files / compilers / interpreters must be edited in the racket
# driver program in order to use the driver program to compete AIs against eachother.

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

# parses through the json data passed in by driver program.
def readJson(data):
	global grid, height, player, width
	grid = data["grid"]
	height = data["height"]
	player = data["player"]
	width = data["width"]


moveJson = {
	"move": 0
}
data = json.loads(raw_input())
grid = data["grid"]
height = data["height"]
player = data["player"]
width = data["width"]

playerME = 0
playerOpponent = 0

# we are the opposite of whichever player is initially passed.
if player == 1:
	playerMe = 1
	playerOpponent = 2
else:
	playerMe = 2
	playerOpponent = 1

while(True):

	hMax = 0 # heuristic max
 	for x in range(0, width):
 		if grid[x][0] == 0: # if the move is valid
 			hVal = heuristic(grid, x, playerMe)
 			if hMax < hVal: # once we found the maximum heuristic value
 				hMax = hVal # save it as the best move

 				moveJson["move"] = x

 	# if we do not have a win condition, lets check if the opponent is close to one			
 	blocking = False
 	if hMax != 4:
 		for x in range(0, width):
 			if grid[x][0] == 0: # if the move is valid
 				opponentHeuristicVal = heuristic(grid,x,playerOpponent)
 				if opponentHeuristicVal >= 3:
 					moveJson["move"] = x
 					blocking = True
 				if opponentHeuristicVal == 4: # if opponent has a win condition, crush their dreams
 					break

 	if playerMe: # if we are first and it is the first move
 		if not blocking:
	 		firstMove = True
	 		for x in range(0, width):
	 			if grid[x][0] != 0:
	 				firstMove = False

	 		if firstMove:
	 			moveJson["move"] = 3  # play in the middle


	sys.stderr.write(str(grid))
	sys.stderr.write("\n")

	jsonMove = json.dumps(moveJson)

	print (jsonMove)
	sys.stdout.flush()
	sys.stderr.flush()

	readJson(json.loads(raw_input()))