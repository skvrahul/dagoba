from dagoba.entities import State, Gremlin, Args


class Query():

    def __init__(self, graph):
        self.graph = graph
        self.state = []
        self.program = []
        self.gremlins = []

    def add(self, pipetype, args: Args):
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

        while(done < last_step):
            step = self.program[pc]

            # Initialize state if needed
            try:
                state = self.state[pc]
            except IndexError:
                for i in range(len(self.state), pc + 1):
                    self.state.append(State())
                state = self.state[pc]

            pipetype = Core.getPipetype(step[0])
            maybe_gremlin = pipetype(self.graph, step[1], maybe_gremlin, state)

            if (maybe_gremlin == 'pull'):
                maybe_gremlin = False
                if pc - 1 > done:
                    pc -= 1                 # Try pulling from the previous pipe
                    continue
                else:
                    done = pc               # This pipe is done as well

            if maybe_gremlin == 'done':
                maybe_gremlin = False
                done = pc

            pc += 1
            if pc > last_step:
                if maybe_gremlin:
                    results.append(maybe_gremlin)
                maybe_gremlin = False
                pc -= 1

        outp = [grem.result if grem.result is not None else grem.vertex for grem in results]
        return outp


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

        def _func(self, *args):
            args_ob = Args.from_tuple(args=args)
            return self.add(pipetype=name, args=args_ob)

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
    def _vertex(graph, args: Args, gremlin: Gremlin, state: State):
        if state.vertices is None:
            state.vertices = graph.findVertices(args)

        if len(state.vertices) == 0:
            return 'done'

        vertex = state.vertices.pop()
        if gremlin:
            return Gremlin(vertex, gremlin.state)
        else:
            return Gremlin(vertex, None)

    def _out(graph, args: Args, gremlin, state):
        state_has_no_edges = state.edges is None or len(state.edges) == 0
        if not gremlin and state_has_no_edges:
            return 'pull'

        if state_has_no_edges:
            state.gremlin = gremlin
            out_edges = graph.findOutEdges(gremlin.vertex)
            state.edges = list(filter(Core.filterEdges(args.get(0)), out_edges))

        if len(state.edges) == 0:
            return 'pull'

        vertex = state.edges.pop()._out

        if gremlin:
            return Gremlin(vertex, gremlin.state)       # Return a Gremlin sitting on the vertex
        else:
            return Gremlin(vertex, None)

    def _in(graph, args: Args, gremlin, state):
        state_has_no_edges = state.edges is None or len(state.edges) == 0
        if gremlin is None and state_has_no_edges:
            return 'pull'

        if state_has_no_edges:
            state.gremlin = gremlin
            state.edges = graph.findInEdges(gremlin.vertex).filter(Core.filterEdges(args.get(0)))

        if len(state.edges) == 0:
            return 'pull'

        vertex = state.edges.pop()._in
        return Gremlin(vertex, gremlin.state)       # Return a Gremlin sitting on the vertex

    def _property(graph, args: Args, gremlin: Gremlin, state):
        if not gremlin:
            return 'pull'
        gremlin.result = gremlin.vertex.getProperty(args.get(0))
        if gremlin.result is not None:
            return gremlin
        else:
            return False

    def _take(graph, args: Args, gremlin, state):
        state.num_taken = state.num_taken or 0
        if state.num_taken == args.get(0):
            state.num_taken = 0
            return 'done'

        if not gremlin:
            return 'pull'

        state.num_taken += 1
        return gremlin

    def _filter(graph, args: Args, gremlin, state):
        if not gremlin:
            return 'pull'

        # Filter query is a property dictionary
        if isinstance(args.get(0), dict):
            return gremlin if gremlin.vertex.matches(args.get(0)) else 'pull'
        # Filter query is a function or lambda
        elif callable(args.get(0)):
            filter_func = args.get(0)
            return gremlin if filter_func(gremlin.vertex) else 'pull'
        # Unsupported filter type
        else:
            Core.error("Unrecognized filter query:" + str(type(args.get(0))))
            return gremlin

    def _unique(graph, args: Args, gremlin, state):
        if not gremlin:
            # No gremlin. Try to get one
            return 'pull'
        elif gremlin.vertex._id in state.vert_ids:
            # Already returned this particular vertex
            return 'pull'
        else:
            # Mark this gremlins vertex as returned
            state.vert_ids.add(gremlin.vertex._id)
            return gremlin


Core.addPipetype('vertex', Core._vertex)
Core.addPipetype('in', Core._in)
Core.addPipetype('out', Core._out)
Core.addPipetype('property', Core._property)
Core.addPipetype('take', Core._take)
Core.addPipetype('filter', Core._filter)
Core.addPipetype('unique', Core._unique)
