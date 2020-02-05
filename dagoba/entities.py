
class Vertex():

    def __init__(self):
        self._id = None
        self._in = []
        self._out = []


class Edge():

    def __init__(self, src: Vertex, target: Vertex):
        if not(src._id and target._id):
            # TODO: Create our own custom errors
            raise ValueError("src or target vertices do not have an ID")
        self._in = src._id
        self._out = target._id
