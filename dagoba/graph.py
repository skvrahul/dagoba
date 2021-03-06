from .entities import Vertex, Edge, Args
from .query import Query
from typing import Dict, List


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

    def _searchVertices(self, query: Dict):
        return list(filter(lambda v: v.matches(query), self.vertices))

    def _findVerticesByIDs(self, ids: List[int]):
        if len(ids) == 1:
            v = self.findVertexByID(ID=ids[0])
            if v:
                return [v]
            else:
                return []
        else:
            verts = map(lambda i: self.findVertexByID(ID=i))
            return list(filter(lambda v: v is not None, verts))

    def findVertices(self, args: Args):
        if args.is_empty():
            return self.vertices[:]
        elif isinstance(args.args[0], dict):
            return self._searchVertices(args.args[0])
        else:
            return self._findVerticesByIDs(args)

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
        edge._in._out.append(edge)
        edge._out._in.append(edge)
        self.edges.append(edge)

    def findOutEdges(self, vertex):
        return vertex._out

    def findInEdges(self, vertex):
        return vertex._in

    def v(self, *args):
        args = Args.from_tuple(args)
        q = Query(self)
        q.add('vertex', args)
        return q
