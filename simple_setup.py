N_STATES = 4

NAMES = ["a", "b", "c", "step_count"]

INIT_STATE = {
    "a": 1.5,
    "b": 0.5,
    "c": 2.5,
    "step_count": 0
}

def rule_0(history):
    state = history[-1]
    return state["a"] + 0.5 * state["b"] - 0.25 * state["c"]

def rule_1(history):
    state = history[-1]
    return 0.5* state["a"] + state["b"] - 0.5 * state["c"]

def rule_2(history):
    state = history[-1]
    return min(state["a"], state["b"])

def rule_3(history):
    state = history[-1]
    return state["step_count"] + 1

RULES = {
    "a": rule_0,
    "b": rule_1,
    "c": rule_2,
    "step_count": rule_3
}

STEPS = 10
OUTPUT_PATH = "history.csv"


def check_model():
    for d in [NAMES, INIT_STATE, RULES]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES]:
        for n in NAMES:
            assert n in d