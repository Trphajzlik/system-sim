
class Engine:
    def __init__(self, init_state, rules):
        self.history = []
        self.curr_state = init_state
        self.rules = rules

    def step(self):
        self.history.append(self.curr_state)
        self.curr_state = []
        for rule in self.rules:
            self.curr_state.append(rule(self.history[-1]))

    def simulate(self, steps):
        for _ in range(steps):
            self.step()

    def state_to_string(self, state):
        output = ""
        delim = ""
        for s in state:
            output += delim
            output += str(s)
            delim = ";"
        return output

    def dump_history(self, path):
        with open(path, "x") as file:
            for entry in self.history:
                file.write(self.state_to_string(entry) + "\n")