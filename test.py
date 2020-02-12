from dagoba.graph import Graph
from dagoba.query import Query
from dagoba.entities import Vertex, Edge
import sys


class Person(Vertex):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


class Relationship(Edge):

    def __init__(self, name, src: Vertex, target: Vertex):
        super().__init__(src, target)
        self.name = name


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

    print(graph.v({'name': 'Rahul'}).out().run())


if __name__ == '__main__':
    args = sys.argv
    main(args)
