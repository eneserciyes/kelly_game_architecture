# The Kelly Game Architecture

## Game Format

A game consists of two **sets**, players will switch sides in between the sets. Each set contains a number of **rounds** determined by the probability sequence. The two sets will be played one after the other.

## Running the Server

Please execute

```shell
python3 server/host.py
```

to run the server. The server will run on `0.0.0.0:4000` by default, and it might instantly quit due to a port collision. The probability sequence is randomly generated with a length `20` for now, and the initial balance is `6000 6800`. You can modify these parameters at the end of `host.py`.


## Sample *python* Clients

There are many python files in the directory, and you only need to modify the name in `player.py`, and fill in the strategy in `solution.py:48`. The comments will help you understand the variables. Functions other than `solve()` in `solution.py` do not need to be changed.

You can run the client by
```python
python3 player.py
```

You can also create multiple strategies and make them compete with each other. Simply create a new `xxx_player.py` and `xxx_solution.py` which extends `Solution`. Examples are provided in `clever_player.py`, `clever_solution.py` and `random_player.py`, `random_solution.py`.



## Interacting with Server

If you are not using the sample clients, please follow the instructions below. 

The client should establish the socket connection with the server first. After connected to the server, the client should send its **player name** as the first piece of data.

Request example:
```
GOAT-Alice
```

After both clients send their names, the server will send the game information, and the game begins. The game information has three sections separated by space:
- Initial side (`A` or `B`)
- Initial balance (two integers separated by space, balance of A and balance of B)
- The probability sequence (`n` numbers separated by space)

Response example:
```
A 2000 2600 0.52 0.68 0.42 0.66 0.59 0.47
```

Then, at each round, the two clients should send their bets first; and after receiving bets from both sides, the server will respond with the updated balances. The request should only contain a non-negative integer, and the response will be two integers separated by space.

Request example:
```
30
```

Response example:
```
2080 2520
```

This interaction will repeat `2n` rounds. After the first `n` rounds, players should switch sides and reset their balance, but **no additional interaction is expected**.

## Web Spectator

To run the simple web spectator, please keep the `exchange.py` running in background first, and open the webpage at `web/index.html`. Specify the websocket address around `host.py:258` by providing the URI to the `remote` parameter of the `Server` class. Then, run the server and both players and view results on the webpage. You may need to refresh the web page before each game begins.