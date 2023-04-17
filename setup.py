N_STATES = 4

INIT_STATE = [1.5, 0.5, 2.5, 0]

def rule_0(state):
    return state[0] + 0.5 * state[1] - 0.25 * state[2]

def rule_1(state):
    return 0.5* state[0] + state[1] - 0.5 * state[2]

def rule_2(state):
    return min(state[0], state[1])

def rule_3(state):
    return state[3] + 1

RULES = [rule_0, rule_1, rule_2, rule_3]

STEPS = 10
OUTPUT_PATH = "history.csv"

COLOURS = ['r', 'g', 'b', 'y']
GRAPH_PATH = "graph.png"
DRAW_STATE = [True, True, True, False]