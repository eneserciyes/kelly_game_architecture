import asyncio
from websockets.server import serve

class ExchangeServer:
  server_ws = None
  client_ws = None

  # def broadcast(self, message):
  #   loop = asyncio.get_event_loop()
  #   for client in self.client_ws:
  #     loop.create_task(client.send(message))
  #     await client.send(message)

  async def handler(self, websocket):
    is_server = False
    is_client = False
    try:
      async for message in websocket:
        if message == "reg server":
          is_server = True
          self.server_ws = websocket
          print("Server Registered")
        elif message == "reg client":
          is_client = True
          self.client_ws = websocket
          print("Client Registered")
        elif is_client == True:
          pass
        elif is_server == True:
          # print(message)
          await self.client_ws.send(message)
    except:
      print("Connection Closed")
      if websocket == self.client_ws:
        self.client_ws = None

  async def run(self, address, port):
    async with serve(self.handler, address, port):
      await asyncio.Future()
  
  def __init__(self, address, port):
    asyncio.run(self.run(address, port))

ExchangeServer("localhost", "8765")