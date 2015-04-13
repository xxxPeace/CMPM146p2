##Name       : Rihui Tan
##Student ID : 1436650

import time
from math import *
import random

class Node:
    def  __init__(self, move = None, parent = None, state = None, who = None):
        self.move = move
        self.parentNode = parent     
        self.who = who
        self.childNodes = []
        self.untriedMoves = state.get_moves()
        self.visits = 0
        self.score = 0.0

    def UCTSelectChild(self):
        #s = sorted(self.childNodes, key = lambda c: c.score + sqrt(2*log(self.visits)/c.visits))[-1]
        s = sorted(self.childNodes, key = lambda c: c.score/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s, j):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s, who = j)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, score):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.score += score
        self.visits += 1


def UCT(rootstate, verbose = False):
    if (rootstate.get_whos_turn() == 'red'):
        who = 'blue'
    else:
        who = 'red'
    rootnode = Node(state = rootstate, who = who)
    start = time.time()
    end = 0
    iterations = 0
    while end < 1:
        node = rootnode
        state = rootstate.copy()
        iterations+=1

		# Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            playerJustMoved = state.get_whos_turn()
            m = random.choice(node.untriedMoves) 
            state.apply_move(m)
            node = node.AddChild(m,state,playerJustMoved) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []: # while state is non-terminal
            state.apply_move(random.choice(state.get_moves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            if (node.who == 'blue' ):
                otherScore = state.get_score()['red']
            else:
                otherScore = state.get_score()['blue']
            node.Update(state.get_score()[node.who] - otherScore) # state is terminal. Update node with result from POV of node.playerJustMoved
            #node.Update(state.get_score()[node.who])
            node = node.parentNode
        end = time.time() - start

    print ("Number of iterations for UCT: ")
    print (iterations)
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move


def think(state, quip):

    return UCT(state) 
 


