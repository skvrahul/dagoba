import sys
from graph import Graph
from query import Query
from entities import Edge, Vertex


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
