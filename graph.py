from entities import Vertex, Edge
from query import Query


class Graph():

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

    def v(self, *args):
        q = Query(self)
        q.add('vertex', args)
        return q
