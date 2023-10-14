from solution import Solution
import random

class RandomSolution(Solution):
  def solve(self):
    return random.randint(10, 100)