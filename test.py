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
    rah = Person('Rahul', 21)
    tom = Person('Tom', 25)
    kat = Person('Kate', 20)
    raj = Person('Raj', 25)
    graph.addVertex(rah)
    graph.addVertex(tom)
    graph.addVertex(kat)
    graph.addVertex(raj)

    graph.addEdge(Relationship('Friends', rah, raj))
    graph.addEdge(Relationship('Friends', raj, kat))
    graph.addEdge(Relationship('Friends', rah, tom))
    graph.addEdge(Relationship('Friends', tom, kat))
    graph.addEdge(Relationship('Friends', tom, raj))
    graph.addEdge(Relationship('Friends', tom, rah))

    print(graph.v({'age': 25}).out().property('name').run())


if __name__ == '__main__':
    args = sys.argv
    main(args)
