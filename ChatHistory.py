class chathistory:
    def __init__(self, size=4):
        self.size = size
        self.history = []

    def add_message(self, message):
        self.history.append(message)
        if len(self.history) > self.size:
            self.history.pop(0)