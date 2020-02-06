from dagoba.entities import State
Pipetypes = {}


class Query():

    def __init__(self, graph):
        self.graph = graph
        self.state = State()
        self.program = []
        self.gremlins = []

    def add(self, pipetype, *args):
        step = (pipetype, args)
        self.program.append(step)

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
            ts = self.state
            step = self.program[pc]
            state = ts or State()
            pipetype = core.Core.getPipetype(step[0])
            maybe_gremlin = pipetype(self.graph, step[1], maybe_gremlin, state)
            if (maybe_gremlin == 'pull'):
                maybe_gremlin = False
                if pc - 1 > done:
                    pc -= 1                 # Try pulling from the previous pipe
                else:
                    done = pc               # This pipe is done as well
            if maybe_gremlin == 'done':
                maybe_gremlin = False
                done = pc

            if pc > last_step:
                if maybe_gremlin:
                    results.append(maybe_gremlin)
                maybe_gremlin = False
                pc -= 1
