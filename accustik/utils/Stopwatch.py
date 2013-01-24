import time
class stopwatch:
    def __init__(self):
        self.start = time.clock()
        self.running = True

    def stop(self):
        self.end = time.clock()
        self.running = False
        return self.__str__()

    def __str__(self):
        if self.running:
            t = time.clock()
            return str(t-self.start)
        else:
            return (self.end-self.start)