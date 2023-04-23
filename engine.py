
class Engine:
    def __init__(self, names, init_state, rules):
        self.history = []
        self.state_names = names
        self.curr_state = init_state
        self.rules = rules

    def step(self):
        self.history.append(self.curr_state)
        self.curr_state = dict()
        for name in self.state_names:
            rule = self.rules[name]
            self.curr_state[name] = rule(self.history[-1])

    def simulate(self, steps):
        for _ in range(steps):
            self.step()

    def names_to_string(self):
        output = ""
        delim = ""
        for n in sorted(self.state_names):
            output += delim
            output += n
            delim = ";"
        return output

    def state_to_string(self, state):
        output = ""
        delim = ""
        for _,s in state.items():
            output += delim
            output += str(s)
            delim = ";"
        return output

    def dump_history(self, path):
        with open(path, "w") as file:
            file.write(self.names_to_string() + "\n")
            for entry in self.history:
                file.write(self.state_to_string(entry) + "\n")
