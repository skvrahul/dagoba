import sys
from dagoba.graph import Graph
from dagoba.query import Query
from dagoba.entities import Edge, Vertex


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


class Dagoba:
    # Map of available pipetypes
    Pipetypes = {}

    def getFauxPipetype():
        def _pipe(_, __, maybe_gremlin):
            return maybe_gremlin or 'pull'
        return _pipe

    def error(msg):
        print('Dagoba Error: ', msg)

    def addPipetype(name, func):
        def _func(self, name, *args):
            return self.add(pipetype=name, *args)

        # Adding the pipe function dynamically to the Query class
        # to allow this function to be invoked on Query objects
        setattr(Query, name, _func)

    def getPipetype(name):
        if name in Dagoba.Pipetypes:
            return Dagoba.Pipetypes
        else:
            Dagoba.error("Unrecognized pipe name")
            return Dagoba.getFauxPipetype

    '''
        Static code to create pipes
    '''


def main(args):
    graph = Graph()
    p1 = Person('Rahul', 21)
    p2 = Person('Tom', 25)
    p3 = Person('Kate', 20)
    graph.addVertex(p1)
    graph.addVertex(p2)
    graph.addVertex(p3)

    graph.addEdge(Relationship('Friends', p1, p2))
    graph.addEdge(Relationship('Friends', p2, p3))

    q = Query(graph)
    q.add('find', 'bob')


if __name__ == '__main__':
    args = sys.argv
    main(args)
