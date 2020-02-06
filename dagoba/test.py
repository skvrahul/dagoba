from graph import Graph


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

