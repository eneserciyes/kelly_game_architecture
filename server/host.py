import asyncio
import random
from enum import Enum
import sys

players = []

def warn(message):
  print("\033[103;1m[WARNING] " + str(message) + "\033[0m")

class Player:
  def __init__(self, name, writer):
    self.writer = writer
    self.balance = 0
    self.game = None
    self.side = None
    self.name = name

  def onMessage(self, message):
    try:
      self.game.setBet(self.side, int(message))
    except Exception as e:
      warn("Illegal bet amount {}".format(message))

  async def sendMessage(self, message):
    self.writer.write(message.encode("utf8"))
    await self.writer.drain()

class GameStage(Enum):
  NOT_STARTED = 0
  FIRST_SET = 1
  SECOND_SET = 2
  ENDED = 3

class Game:
  def __init__(self, players, gameend_cb, balance, prob_seq):
    self.A = players[0]
    self.B = players[1]
    self.A.game = self
    self.A.side = "A"
    self.B.game = self
    self.B.side = "B"
    self.balance = balance
    self.A.balance = balance[0]
    self.B.balance = balance[1]
    self.round = 0
    self.prob_seq = prob_seq
    self.stage = GameStage.NOT_STARTED
    self.bet = {
      "A": None,
      "B": None
    }
    self.first_set_result = None
    self.gameend_cb = gameend_cb
    print("\n\033[36m== Game Info ==\033[0m\n")
    print("Player A Balance: {}".format(self.A.balance))
    print("Player B Balance: {}".format(self.B.balance))
    print("Player: \033[36;4;1m{}\033[0m \033[33;4;1m{}\033[0m".format(self.A.name, self.B.name))
    print("Rounds per set: {}".format(len(prob_seq)))

  def getPlayer(self, side) -> Player:
    if side == "A": return self.A
    elif side == "B": return self.B
  
  async def start(self):
    await self.A.sendMessage("A {} {} {}".format(
      self.A.balance,
      self.B.balance,
      " ".join(map(str, self.prob_seq))
    ))
    await self.B.sendMessage("B {} {} {}".format(
      self.A.balance,
      self.B.balance,
      " ".join(map(str, self.prob_seq))
    ))
    print("\n\033[36m== 1st Set Started ==\033[0m\n")
    self.stage = GameStage.FIRST_SET
  
  def setBet(self, side, amount):
    if self.stage == GameStage.NOT_STARTED or self.stage == GameStage.ENDED:
      warn("Not in game while placing bet")
      return
    if self.bet[side] != None:
      warn("Bet amount already set for player " + str(side))
      return
    player = self.getPlayer(side)
    print("Player {} ({}) put ${}".format(side, player.name, amount))
    if amount > player.balance:
      warn("Betting more than balance, maximum balance placed as bet")
      amount = player.balance
    if amount < 0:
      amount = 0
    self.bet[side] = amount
    if self.bet["A"] != None and self.bet["B"] != None:
      loop = asyncio.get_event_loop()
      loop.create_task(self.settleRound())
  
  async def settleRound(self):
    total_bet = self.bet["A"] + self.bet["B"]
    this_round_prob = self.prob_seq[self.round]
    this_round_result = random.random()
    if this_round_result < this_round_prob:
      total_bet = min(total_bet, self.B.balance)
      self.A.balance += total_bet
      self.B.balance -= total_bet
    else:
      total_bet = min(total_bet, self.A.balance)
      self.B.balance += total_bet
      self.A.balance -= total_bet
    message = "{} {}".format(self.A.balance, self.B.balance)
    print("Set {} Round {}: Player {} ({}) wins ${}. Balance: {} {}".format(
      "1" if self.stage == GameStage.FIRST_SET else "2",
      self.round + 1,
      "A" if this_round_result < this_round_prob else "B",
      self.A.name if this_round_result < this_round_prob else self.B.name,
      total_bet,
      self.A.balance,
      self.B.balance
    ))
    await self.A.sendMessage(message)
    await self.B.sendMessage(message)
    self.bet["A"] = None
    self.bet["B"] = None
    self.round += 1
    if self.round == len(self.prob_seq):
      if self.stage == GameStage.FIRST_SET:
        print("\n\033[36m== 1st Set Ended ==\033[0m\n")
        balance_diff = self.A.balance - self.B.balance
        print("[First Set Results]\n{} (Player A): {} {}\n{} (Player B): {} {}".format(
          self.A.name, self.A.balance, (" [Lead by " + str(balance_diff) + "]") if balance_diff > 0 else "",
          self.B.name, self.B.balance, (" [Lead by " + str(-balance_diff) + "]") if balance_diff < 0 else ""
        ))
        print("Switching Sides...")
        self.stage = GameStage.SECOND_SET
        self.round = 0
        self.first_set_result = (self.A.balance, self.B.balance)
        self.A, self.B = self.B, self.A
        self.A.side = "A"
        self.B.side = "B"
        self.A.balance = self.balance[0]
        self.B.balance = self.balance[1]
        print("\n\033[36m== 2nd Set Started ==\033[0m\n")
      else:
        print("\n\033[36m== Game Over ==\033[0m\n")
        total_score = (self.B.balance + self.first_set_result[0], self.A.balance + self.first_set_result[1])
        score_diff = total_score[0] - total_score[1]
        print("[Final Results]\n{} (Player B in second set): {} + {} = {} {}\n{} (Player A in second set): {} + {} = {} {}".format(
          self.B.name,
          self.first_set_result[0], self.B.balance, total_score[0],
          (" [Lead by " + str(score_diff) + "]") if score_diff > 0 else "",
          self.A.name,
          self.first_set_result[1], self.A.balance, total_score[1],
          (" [Lead by " + str(-score_diff) + "]") if score_diff < 0 else ""
        ))
        if score_diff > 0:
          print("\033[31;1;4m{}\033[0m\033[31;1m WINS!\033[0m".format(self.B.name))
        elif score_diff < 0:
          print("\033[31;1;4m{}\033[0m\033[31;1m WINS!\033[0m".format(self.A.name))
        else:
          print("\033[31;1mDRAW!\033[0m")
        self.stage = GameStage.ENDED
        self.gameend_cb()

class Server:
  def closeServer(self):
    self.server.close()
  
  async def onNewConnection(self, reader, writer):
    socket_info = reader._transport.get_extra_info("peername")
    print("\033[90;1mConnection established from", socket_info, "\033[0m")
    player = None
    while True:
      try:
        request = (await reader.read(64)).decode("utf8")
        if not request:
          break
        if player:
          player.onMessage(request)
        elif len(players) < 2:
          player = Player(request[0:32], writer)
          players.append(player)
          if len(players) == 2:
            game = Game((players[0], players[1]), self.closeServer, self.initial_balance, self.prob_seq)
            await game.start()
        else:
          print("\033[90;1mIllegal request from", socket_info, "\033[0m")
          break
      except ConnectionResetError as e:
        break
      except:
        break
    if player:
      self.closeServer()
    print("\033[90;1mConnection closed at", socket_info, "\033[0m")
    writer.close()

  async def run(self):
    self.server = await asyncio.start_server(self.onNewConnection, self.host, self.port)
    print("\033[90;1mServer started at {}:{}\033[0m".format(self.host, self.port))
    async with self.server:
      await self.server.serve_forever()

  def __init__(self, host, port, initial_balance, prob_seq):
    self.host = host
    self.port = port
    self.initial_balance = initial_balance
    self.prob_seq = prob_seq

if __name__ == "__main__":
  server = Server(
    host = "0.0.0.0",
    port = 4000,
    initial_balance = (6000, 6800),
    prob_seq = list(random.randint(40, 70) / 100 for x in range(0, 20))
  )
  try:
    asyncio.run(server.run())
  except:
    pass