import sys


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


class Dagoba():

    def __init__(self):
        self.autoID = 1
        self.edges = []
        self.vertices = []
        self.vertexIndex = {}

    def findVertexByID(self, ID):
        if ID in self.vertexIndex:
            return self.vertexIndex[ID]
        else:
            return None

    def addVertex(self, vertex: Vertex):
        if not vertex._id:
            vertex._id = self.autoID
            self.autoID += 1
        elif self.findVertexByID(vertex._id):
            # TODO: Create our own custom errors
            raise ValueError('Vertex with that ID already Exists')
        else:
            pass

        # Adding the vertex to our graph
        self.vertices.append(vertex)
        self.vertexIndex[vertex._id] = vertex

        # Setting the in and out of the vertexes to be empty lists
        vertex._out = []
        vertex._in = []

        return vertex._id

    def addEdge(self, edge: Edge):
        edge._in = self.findVertexByID(edge._in)
        edge._out = self.findVertexByID(edge._out)
        if not(edge._in and edge._out):
            # TODO: Create our own custom errors
            raise ValueError('Edge was not found')
        edge._out._out.append(edge)
        edge._in._in.append(edge)
        self.edges.append(edge)


class Person(Vertex):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


class Relationship(Edge):

    def __init__(self, name: str, src: Vertex, target: Vertex):
        super().__init__(src=src, target=target)
        self.name = name
        self._in = src._id
        self._out = target._id


def main(args):
    graph = Dagoba()
    p1 = Person('Rahul', 21)
    p2 = Person('Tom', 25)
    p3 = Person('Kate', 20)
    graph.addVertex(p1)
    graph.addVertex(p2)
    graph.addVertex(p3)

    graph.addEdge(Relationship('Friends', p1, p2))
    graph.addEdge(Relationship('Friends', p2, p3))


if __name__ == '__main__':
    args = sys.argv
    main(args)
