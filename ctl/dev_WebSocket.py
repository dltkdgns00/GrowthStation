from dev_prototype import DevPrototype

class WSOCKET(DevPrototype):

  def __init__(self, name="WebSocket", interval=1):
    self.name = name
    self.interval = interval
    print(f"{self.name} has been initialized with interval {self.interval} seconds.")

  def loop(self):
    self.share()

  def cleanup(self):
    print(f"{self.name} has been cleaned up.")
