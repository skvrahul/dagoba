class Query():

    def __init__(self, graph):
        self.graph = graph
        self.state = []
        self.program = []
        self.gremlins = []

    def add(self, pipetype, *args):
        step = [pipetype, args]
        self.program.append(step)
