from query import Query
from entities import Edge, Vertex, Gremlin, State


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


class Core:
    # Map of available pipetypes
    Pipetypes = {}

    def getFauxPipetype():
        def _pipe(_, __, maybe_gremlin):
            return maybe_gremlin or 'pull'
        return _pipe

    def error(msg):
        print('Dagoba Error: ', msg)

    def addPipetype(name, func):
        Core.Pipetypes[name] = func

        def _func(self, name, *args):
            return self.add(pipetype=name, *args)

        # Adding the pipe function dynamically to the Query class
        # to allow this function to be invoked on Query objects
        setattr(Query, name, _func)

    def getPipetype(name):
        if name in Core.Pipetypes:
            return Core.Pipetypes[name]
        else:
            Core.error("Unrecognized pipe name")
            return Core.getFauxPipetype

    def goToVertex(gremlin: Gremlin, vertex: Vertex):
        return Gremlin(vertex, gremlin.state)

    def filterEdges(query):
        if not query:
            # Empty or null query
            return lambda x: True
        elif isinstance(query, str):
            # Edge label has to be the same as query
            return lambda edge: edge._label == query
        elif isinstance(query, list):
            # Edge label has to be one of the query string
            return lambda edge: edge._label in query
        elif isinstance(query, dict):
            # Edge has to match a set of parameters. Using edge's 'matches' method to match the dict
            return lambda edge: edge.matches(query)
        else:
            # Unknown query. Match all edges
            return lambda x: True

    '''
        Defining various standard pipetypes
    '''
    def _vertex(graph, args, gremlin: Gremlin, state: State):
        if not state.vertices:
            state.vertices = graph.findVertices(args)

        if len(state.vertices) == 0:
            return 'done'

        vertex = state.vertices.pop()
        return Gremlin(vertex, gremlin.state)

    def _out(graph, args, gremlin, state):
        state_has_no_edges = state.edges is None or len(state.edges) == 0
        if gremlin is None and state_has_no_edges:
            return 'pull'

        if state_has_no_edges:
            state.gremlin = gremlin
            state.edges = list(filter(Core.filterEdges(args[0]), graph.findOutEdges(gremlin.vertex)))

        if len(state.edges) == 0:
            return 'pull'

        # TODO: Check if below line is correct
        vertex = state.edges.pop()._in
        return Core.goToVertex(state.gremlin, vertex)

    def _in(graph, args, gremlin, state):
        state_has_no_edges = state.edges is None or len(state.edges) == 0
        if gremlin is None and state_has_no_edges:
            return 'pull'

        if state_has_no_edges:
            state.gremlin = gremlin
            state.edges = graph.findInEdges(gremlin.vertex).filter(Core.filterEdges(args[0]))

        if len(state.edges) == 0:
            return 'pull'
        # TODO: Check if below line is correct
        vertex = state.edges.pop()._out
        return Core.goToVertex(state.gremlin, vertex)

    def _property(graph, args, gremlin: Gremlin, state):
        if not gremlin:
            return 'pull'
        gremlin.result = gremlin.vertex.getProperty(args[0])
        if gremlin.result:
            return gremlin
        else:
            return False

    def _take(graph, args, gremlin, state):
        state.num_taken = state.num_taken or 0
        if state.num_taken == args[0]:
            state.num_taken = 0
            return 'done'

        if not gremlin:
            return 'pull'

        state.num_taken += 1
        return gremlin

    addPipetype('vertex', _vertex)
    addPipetype('in', _vertex)
    addPipetype('out', _vertex)
