import asyncio
import websockets
from websockets.sync.client import connect

# async def echo(websocket):
#   async for message in websocket:
#     await websocket.send(message)

class SyncRemote:
  def __init__(self, uri):
    self.uri = uri
    self.ws = connect(self.uri)
    self.ws.send("reg server")
  
  def send(self, message):
    self.ws.send(message)
  
  def close(self):
    self.ws.close()
  
  def receive(self):
    return self.ws.recv()