from solution import Solution
import numpy as np
from enum import Enum

class NodeType(Enum):
        MAX = 0
        MIN = 1

class Node:
    def __init__(self, balance: int, win_prob: float, current_round:int):
        self.balance = balance
        self.win_prob = win_prob
        self.children = []
        self.prev_move = None
        self.current_round = current_round 
     
# Getting expectimax
def expectimax(node): 
    # Condition for Terminal node
    if node.win_prob == None:
        return node.balance
     
    kelly_amount = int(round(node.balance * (2*node.win_probs[node.current_round] - 1)))
    for i in range(-2, 3):
        bet_amount = int(round(kelly_amount + i*0.05*node.balance))
        node.children.append(Node(node.balance + bet_amount *, NodeType.CHANCE, node.win_prob[node.current_round], node.current_round)) 
    return max(*[expectimax()])
  
    # Chance node. Returns the average of
    # the left and right sub-trees
    else:
        return (expectimax(node.left, True)+ expectimax(node.right, True))/2;

class KellySolution(Solution):
  def solve(self):
    # Variables that might be helpful:
    #   self.prob_seq : List of the probability sequence
    #   self.current_round : Current round number, round starts at 0
    #   self.my_side : Side in current set, 0 for A and 1 for B
    #   self.my_balance
    #   self.enemy_balance
    #   self.first_set_score_diff : The score difference in first set
    #                               will be None during first set

    win_prob = np.array(self.prob_seq) if self.my_side == 0 else (1 - np.array(self.prob_seq))
    print("My win rate this round is", win_prob)
    kelly_amount = int(round(self.my_balance * (2*win_prob - 1)))


    # Don't forget to return the amount to bet!
    return bet_amount
