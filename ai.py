
from __future__ import absolute_import, division, print_function
import copy, random
from game import Game
import math


MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        return len(self.children) == 0

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)


    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None: ###the node is the current node
            node = self.root
        if depth == self.search_depth: #base case
            self.simulator.reset(node.state[0], node.state[1])
            return

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)
            self.simulator.reset(node.state[0], node.state[1])
            for d in MOVES:
                if self.simulator.move(d) == True:
                    state = self.simulator.get_state()
                    new_node = Node(state, CHANCE_PLAYER)
                    node.children.append((d, new_node))
                    self.simulator.undo()

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():

            self.simulator.reset(node.state[0], node.state[1])
            for spot in self.simulator.get_open_tiles():
                self.simulator.tile_matrix[spot[0]][spot[1]] = 2
                state = self.simulator.get_state()
                new_node = Node(state, MAX_PLAYER)
                node.children.append((None, new_node))
                self.simulator.tile_matrix[spot[0]][spot[1]] = 0

        # TODO: build a tree for each child of this node
        for n in node.children:
            self.build_tree(n[1], depth+1, ec=False)


    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            payoff = node.state[1]
            return None, payoff

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            score_best = -math.inf
            init_score = score_best
            d_best = 0
            for d, child_node in node.children:
                current_score = self.expectimax(child_node)[1]
                score_best = max(score_best, current_score)
                if score_best > init_score:
                    init_score = score_best
                    d_best = d
            return d_best, score_best
        

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0
            for d, child_node in node.children:
                value = value + self.expectimax(child_node)[1] / (len(node.children))
            return None, value


    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction







































        # recursive function to build a game tree
    def build_tree2(self, node=None, depth=0, ec=True):
        if node == None: ###the node is the current node
            node = self.root
            matrix2 = [[10000,10000,10000,10000],[5000,5000,10000,10000],[500,500,10000,10000],[0,0,10000000,10000]]
            #matrix = [[0,1,2,3],[1,2,3,4],[2,3,4,5],[3,4,5,6]]
            #matrix = [[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
            matrix = [[-1,0,0,100],[-1,0,50,1000],[-1,0,100,10000],[0,0,1000,1000000]]
            matrix3 = [[-1,0,0,0],[-1,0,0,0],[-1,0,0,10000000],[0,0,0,10000000]]
            lst = []
            temp_state =[]
            for i in range(self.simulator.board_size):
                for j in range(self.simulator.board_size):
                    lst.append(0)
                temp_state.append(lst)
                lst = []
            
            

        if depth == self.search_depth: #base case
            self.simulator.reset(node.state[0], node.state[1])
            return


        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)
            self.simulator.reset(node.state[0], node.state[1])
        
            for d in MOVES:
                if self.simulator.move(d) == True:
                    new_score = 0
                    state = self.simulator.get_state()
                    if state[0][3][3] == 512:
                        for i in range(self.simulator.board_size):
                            for j in range(self.simulator.board_size):
                                temp_state[i][j] = state[0][i][j] + matrix2[i][j]
                    elif state[0][2][2] == 128 and state[0][3][3] == 512:
                         for i in range(self.simulator.board_size):
                            for j in range(self.simulator.board_size):
                                temp_state[i][j] = state[0][i][j] + matrix3[i][j]
                    else:
                        for i in range(self.simulator.board_size):
                            for j in range(self.simulator.board_size):
                                temp_state[i][j] = state[0][i][j] + matrix[i][j]

                    print(state)

                    
                    for i in range(self.simulator.board_size):
                        for j in range(self.simulator.board_size):
                            if matrix[i][j] == temp_state[i][j]:
                                continue
                            else:
                                new_score = new_score + temp_state[i][j]
                    print(new_score)

                    new_state = (state[0], new_score)
                    new_node = Node(new_state, CHANCE_PLAYER)
                    node.children.append((d, new_node))
                    self.simulator.undo()


            

            
                    

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():

            self.simulator.reset(node.state[0], node.state[1])
            for spot in self.simulator.get_open_tiles():
                self.simulator.tile_matrix[spot[0]][spot[1]] = 2
                state = self.simulator.get_state()
                new_node = Node(state, MAX_PLAYER)
                node.children.append((None, new_node))
                self.simulator.tile_matrix[spot[0]][spot[1]] = 0

        # TODO: build a tree for each child of this node
        for n in node.children:
            self.build_tree(n[1], depth+1, ec=True)
    


    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax2(self, node = None):

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            payoff = node.state[1]
            return None, payoff

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            score_best = -math.inf
            init_score = float(score_best)
            d_best = 0
            for d, child_node in node.children:
                current_score = self.expectimax(child_node)[1]
                score_best = max(score_best, current_score)
                if score_best > init_score:
                    init_score = score_best
                    d_best = d
            return d_best, score_best
        
        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            value = 0.0
            for d, child_node in node.children:
                value = value + self.expectimax(child_node)[1] / (len(node.children))
            return None, value

    

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        self.build_tree2()
        direction, _ = self.expectimax2(self.root)
        return direction



