##Name       : Rihui Tan
##Student ID : 1436650

from random import choice 
def think(state, quip):
	highScore = 0
	moveArray = state.get_moves()
	#bestMove = state.get_moves()[0]
	bestMove = choice(state.get_moves())
	for move in moveArray:
		stateCopy = state.copy()
		stateCopy.apply_move(move)
		score = stateCopy.get_score()[state.get_whos_turn()]
		if score > highScore:
			highScore = score
			bestMove = move
  	return bestMove