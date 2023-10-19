import time

class Timer:
  def start(self):
    if self.start_timestamp == None:
      self.start_timestamp = time.time()
  
  def stop(self):
    if self.start_timestamp != None:
      self.time = time.time() - self.start_timestamp + self.time
      self.start_timestamp = None
    return self.time
  
  def get(self):
    if self.start_timestamp != None:
      return time.time() - self.start_timestamp + self.time
    else:
      return self.time

  def __init__(self, start_time = 0):
    self.time = start_time
    self.start_timestamp = None