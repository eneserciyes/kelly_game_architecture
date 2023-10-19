from solution import Solution
import random
SIMULATION_COUNT = 5000

def simulate_game(my_balance, opp_balance, win_probs, risk_factor_pos, risk_factor_neg):
    moving_avg = 0
    for i in range(SIMULATION_COUNT):
        balance = my_balance
        opp = opp_balance
        for j, win_prob in enumerate(win_probs[0:10]): # only simulate first 10 rounds
            if balance <= 0 or opp <= 0:
                break
            # determine criterion with risk factors
            if j==0: # play with risk factor in first round
                criterion = 2*win_prob - 1
                if criterion > 0:
                    bet_amount = int(balance * (risk_factor_pos * criterion))
                if criterion <= 0:
                    if my_balance > opp_balance:
                        kelly_leftover = (balance - opp) * (risk_factor_neg * (1 + criterion))
                        bet_amount = kelly_leftover
                    else:
                        bet_amount = balance * (risk_factor_neg * (1 + criterion))
            else: # then play with Kelly criterion
                if win_prob>0.5:
                    bet_amount = int(balance * (2*win_prob - 1))
                else:
                    bet_amount = 0

            # determine opponent bet amount, assume always playing Kelly criterion
            if win_prob>0.5:
                opp_bet_amount = 0
            else:
                opp_bet_amount = int(opp * (2*(1-win_prob) - 1))
            
            total_bet = bet_amount + opp_bet_amount

            # determine win or lose and settle
            random_number = random.random()
            if random_number < win_prob:
                balance += min(total_bet, opp)
                opp -= min(total_bet, opp)
            else:
                balance -= min(total_bet, balance)
                opp += min(total_bet, balance)
        moving_avg = ((moving_avg * i) + balance) / (i+1)
    return moving_avg

class MonteCarloSolution(Solution):
  def solve(self):
    if self.current_round == 0: self.balance_init = self.my_balance

    print(f"Balance at round {self.current_round}: {self.my_balance}")
    win_probs = self.prob_seq[self.current_round:] if self.my_side == 0 else ([1 - x for x in self.prob_seq[self.current_round:]])
    print(f"Current win prob: {win_probs[0]}")

    # if about to go bankrupt strategy
    if self.my_balance < self.balance_init / 6:
        print("I'm about to go bankrupt!")
        if self.first_set_score_diff is not None:
            if (self.first_set_score_diff > 0 and self.my_side==0) or (self.first_set_score_diff < 0 and self.my_side==1): 
                return int(self.my_balance * (2*win_probs[0] - 1) * 2) # play very risky, not more to lose
            else:
                return int(self.my_balance * (2*win_probs[0] - 1) * 0.1) # you were winning, try to play safer
        return int(self.my_balance * (2*win_probs[0] - 1) * 0.1) # you are in the first round, play safe, try to keep as much as you can
    
        
    # use a Monte carlo estimation with various risk factors and choose the best one.
    ranges = 10
    pos_start, pos_step = 0.5, 0.1
    neg_start, neg_step = 0, 0.02
    
    risk_factor_poss = [pos_start + i*pos_step for i in range(ranges)]
    risk_factor_negs = [neg_start + i*neg_step for i in range(ranges)]
    outputs = [0] * ranges
    if win_probs[0] > 0.5:
        # run the simulations with positive risk factor and place them in an array
        for i, risk_factor_pos in enumerate(risk_factor_poss):
            exp_balance = simulate_game(self.my_balance, self.enemy_balance, win_probs, risk_factor_pos, risk_factor_neg=0.)
            outputs[i] = exp_balance
    else:
        # run the simulations with negative risk factor and place them in an array
        for i, risk_factor_neg in enumerate(risk_factor_negs):
            exp_balance = simulate_game(self.my_balance, self.enemy_balance, win_probs, risk_factor_pos=1., risk_factor_neg=risk_factor_neg)
            outputs[i] = exp_balance


    # find the best risk factors
    max_output = max(outputs)
    max_index = outputs.index(max_output)

    if win_probs[0] > 0.5:
        best_risk_factor_pos = risk_factor_poss[max_index]
        best_risk_factor_neg = 0
    else:
        best_risk_factor_neg = risk_factor_negs[max_index]
        best_risk_factor_pos = 0

    print("Best pos risk factor: ", best_risk_factor_pos)
    print("Best neg risk factor: ", best_risk_factor_neg)
    
    # play the risk factors
    criterion = 2*win_probs[0] - 1
    if criterion > 0:
        bet_amount = int(self.my_balance * (best_risk_factor_pos * criterion))
    if criterion <= 0:
        bet_amount =  int(self.my_balance * (best_risk_factor_neg * (1 + criterion)))

    # Don't forget to return the amount to bet!
    return bet_amount if bet_amount > 0 else 0
