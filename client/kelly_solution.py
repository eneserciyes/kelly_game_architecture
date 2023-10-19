from solution import Solution

class KellySolution(Solution):
  def solve(self):
    print(f"Balance at round {self.current_round}: {self.my_balance}")
    win_prob = self.prob_seq[self.current_round] if self.my_side == 0 else (1 - self.prob_seq[self.current_round])
    bet_amount = int(round(self.my_balance * (2*win_prob - 1)))

    # Don't forget to return the amount to bet!
    return bet_amount
