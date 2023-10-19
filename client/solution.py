class Solution:
  def __init__(self, initial_side, balance, prob_seq):
    self.initial_side = initial_side # Side to take in the first set, "A" or "B"
    self.initial_balance = balance # Initial balance of two players in tuple, (Balance A, Balance B)
    self.prob_seq = prob_seq # The probability sequence list

    #
    # Information that can be derived from initial data
    #
    self.current_round = 0
    self.total_rounds = len(prob_seq)
    self.my_side = 0 if initial_side == "A" else 1 # Use number to represent side (0 for A and 1 for B)
    self.my_balance = balance[self.my_side]
    self.enemy_balance = balance[self.my_side ^ 1]
    self.first_set_score_diff = None

  # update() will be called each round before solve() to update data
  def update(self, current_round, current_balance):
    self.current_round = current_round
    self.my_balance = current_balance[self.my_side]
    self.enemy_balance = current_balance[self.my_side ^ 1]

  # switchSides() will be called when first set ends
  def switchSides(self):
    self.first_set_score_diff = self.my_balance - self.enemy_balance # Might be used in strategy
    self.my_side ^= 1
    self.my_balance = self.initial_balance[self.my_side] # Reset to initial balance
    self.enemy_balance = self.initial_balance[self.my_side ^ 1]

  # endofGame() will be called at the end of the second set, you can celebrate in this function or do nothing
  def endOfGame(self, final_balance):
    print("Did I win?")

  # solve() will be called when it's time to placing bets
  # Returns the amount to place for this round
  def solve(self):
    # Variables that might be helpful:
    #   self.prob_seq : List of the probability sequence
    #   self.current_round : Current round number, round starts at 0
    #   self.my_side : Side in current set, 0 for A and 1 for B
    #   self.my_balance
    #   self.enemy_balance
    #   self.first_set_score_diff : The score difference in first set
    #                               will be None during first set
    #   For example, your win rate this round is 
    #     self.prob_seq[self.current_round] if self.my_side == 0 else (1 - self.prob_seq[self.current_round])

    # Your solution here...
    win_prob = self.prob_seq[self.current_round] if self.my_side == 0 else (1 - self.prob_seq[self.current_round])
    print("My win rate this round is", win_prob)
    bet_amount = int(round(self.my_balance * (2*win_prob - 1)))

    # Don't forget to return the amount to bet!
    return bet_amount
