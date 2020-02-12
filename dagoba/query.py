from dagoba.entities import State, Gremlin


class Query():

    def __init__(self, graph):
        self.graph = graph
        self.state = State()
        self.program = []
        self.gremlins = []

    def add(self, pipetype, args):
        step = (pipetype, args)
        self.program.append(step)
        return self

    def run(self):
        last_step = len(self.program) - 1   # Index of last step in the pipeline
        maybe_gremlin = False               # Gremlin / Signal / False
        results = []                        # Results of this invokation of `run`
        done = -1                           # Step behind which things have finished
        pc = last_step                      # pc = Program Counter. Start by pointing to the last step

        step = None
        state = None
        pipetype = None
        print('Running pipetypes')
        print(self.program)

        cnt = 0
        while(done < last_step):
            if cnt > 15:
                exit()
            cnt += 1
            ts = self.state
            step = self.program[pc]
            print(step)
            state = ts or State()
            pipetype = Core.getPipetype(step[0])
            maybe_gremlin = pipetype(self.graph, step[1], maybe_gremlin, state)
            if (maybe_gremlin == 'pull'):
                print('Pulling from ', step)
                maybe_gremlin = False
                if pc - 1 > done:
                    print('Go to prev pipe')
                    pc -= 1                 # Try pulling from the previous pipe
                    continue
                else:
                    print('This pipe is done')
                    done = pc               # This pipe is done as well

            if maybe_gremlin == 'done':
                print('Done')
                maybe_gremlin = False
                done = pc
            pc += 1
            if pc > last_step:
                print('Gremlin came out')
                if maybe_gremlin:
                    results.append(maybe_gremlin)
                maybe_gremlin = False
                pc -= 1

        return results


class Core:
    # Map of available pipetypes
    Pipetypes = {}

    @classmethod
    def getFauxPipetype():
        def _pipe(_, __, maybe_gremlin):
            return maybe_gremlin or 'pull'
        return _pipe

    def error(msg):
        print('Dagoba Error: ', msg)

    @classmethod
    def addPipetype(cls, name, func):
        Core.Pipetypes[name] = func

        def _func(self, args=None):
            return self.add(pipetype=name, args=args)

        # Adding the pipe function dynamically to the Query class
        # to allow this function to be invoked on Query objects
        setattr(Query, name, _func)

    def getPipetype(name):
        if name in Core.Pipetypes:
            return Core.Pipetypes[name]
        else:
            Core.error("Unrecognized pipe name")
            return Core.getFauxPipetype

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
        print(state.vertices, 'state.vertices')

        if len(state.vertices) == 0:
            return 'done'

        vertex = state.vertices.pop()
        if gremlin:
            return Gremlin(vertex, gremlin.state)
        else:
            return Gremlin(vertex, State())

    def _out(graph, args, gremlin, state):
        print(args)
        state_has_no_edges = state.edges is None or len(state.edges) == 0
        if not gremlin and state_has_no_edges:
            return 'pull'

        if state_has_no_edges:
            state.gremlin = gremlin
            state.edges = list(filter(Core.filterEdges(args[0]), graph.findOutEdges(gremlin.vertex)))

        if len(state.edges) == 0:
            return 'pull'

        # TODO: Check if below line is correct
        vertex = state.edges.pop()._in
        return Gremlin(vertex, gremlin.state)       # Return a Gremlin sitting on the vertex

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
        return Gremlin(vertex, gremlin.state)       # Return a Gremlin sitting on the vertex

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


Core.addPipetype('vertex', Core._vertex)
Core.addPipetype('in', Core._in)
Core.addPipetype('out', Core._out)
