from typing import Dict, List, Tuple


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

    def __repr__(self):
        return '<Vertex: %s>' % self._id


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

    def __repr__(self):
        return '<state:{vertices:%s, edges: %s, gremlin: %s}>' % (self.vertices, self.edges, self.gremlin)


class Args:

    def __init__(self, args: List = None):
        if args:
            self.args = args
        else:
            self.args = []

    @classmethod
    def from_tuple(cls, args: Tuple):
        list_args = []
        for a in args:
            list_args.append(a)
        return Args(args=list_args)

    def is_empty(self):
        return self.args is None or len(self.args) == 0

    def get(self, index):
        if self.is_empty():
            return None
        else:
            if index >= len(self.args):
                return None
            else:
                return self.args[index]

    def __repr__(self):
        return '<Args: %s>' % self.args


class Gremlin:

    def __init__(self, vertex: Vertex, state: Dict=None):
        self.vertex = vertex
        if(state is None):
            self.state = State()
        else:
            self.state = state

        self.result = None

    def __repr__(self):
        s = '<Gremlin: vertex:%s, state:%s' % (self.vertex, self.state)
        if self.result:
            s += ', result:%s' % self.result
        s += '>'
        return s
