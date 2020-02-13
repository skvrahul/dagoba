# dagoba
A basic in memory Graph DB built using Python   

This is a Python implementation of the Graph DB by the same name as illustrated in the book [500 Lines or Less](https://github.com/aosabook/500lines) (Originally built in JS)

## Usage

To add any object as a vertex to the graph ensure your object is a subclass of `Vertex` and similarly, to add your object as an edge, ensure it is a subclass of `Edge`.

Below is a quick example

```python
from dagoba.graph import Graph
from dagoba.entities import Vertex, Edge


class Person(Vertex):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


class Relationship(Edge):

    def __init__(self, name, src: Vertex, target: Vertex):
        super().__init__(src, target)
        self.name = name
```

Below few lines highlight instantiation of the graph and adding vertices and edges to it..

```python
graph = Graph()

p1 = Person('Bob', 21)
p2 = Person('Tom', 25)
p3 = Person('Kate', 22)
p4 = Person('Alice', 27)


graph.addVertex(p1)
graph.addVertex(p2)
graph.addVertex(p3)
graph.addVertex(p4)


graph.addEdge(Relationship('friend', p1, p3))
graph.addEdge(Relationship('friend', p1, p2))
graph.addEdge(Relationship('family', p1, p4))
```

Here are some examples of how the Graph DB can be queried   
*Dagoba* uses chained querying along with lazy execution so each query operator operates on a query and returns another query object.
The results of the query are evaluated upon calling **run()**

```python
# Get all of Bob's connections
print(graph.v({'name', 'Bob'}).out().run())

# Get all of Bob's friends
print(graph.v({'name':'Bob'}).out({'name':'friend'}).run())


# Get one of Bob's friends
print(graph.v({'name':'Bob'}).out({'name':'friend'}).take(1).run())

```
