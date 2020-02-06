from typing import Dict


class Vertex():

    def getProperty(self, name):
        return getattr(self, name, lambda: None)

    def matches(self, query: Dict):
        for k, v in query.items():
            if not(self.getProperty(k) == v):
                return False
        return True

    def __init__(self):
        self._id = None
        self._in = []
        self._out = []


class Edge():

    def getProperty(self, name):
        return getattr(self, name, lambda: None)

    def __init__(self, src: Vertex, target: Vertex):
        if not(src._id and target._id):
            # TODO: Create our own custom errors
            raise ValueError("src or target vertices do not have an ID")
        self._in = src._id
        self._out = target._id


class State:

    def __init__(self):
        self.vertices = None
        self.edges = None
        self.gremlin = None
        self.num_taken = 0


class Gremlin:

    def __init__(self, vertex: Vertex, state: Dict=None):
        self.vertex = vertex
        if(state is None):
            self.state = State()
        else:
            self.state = state

        self.result = None
