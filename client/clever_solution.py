from solution import Solution

class CleverSolution(Solution):
  def solve(self):
    if self.enemy_balance > 0:
      return self.my_balance
    else:
      return 0