from setup import POP_DISTR

def get_name(strat):
    ad_strat, spend_strat = strat
    return f"{ad_strat}|{spend_strat}"

C_N_GRAPHS = 2

C_GRAPH_NAMES = [
    "used%",
    "money"
]

C_GRAPH_PATHS = {
    "used%" : "c_graph0.png",
    "money" : "c_graph1.png"
}

C_COLOURS = {
    "used%" : {
        get_name(("basic", "basic")) : 'r',
        get_name(("constant", "constant")) : 'g'
    },
    "money" : {
        get_name(("basic", "basic")) : 'r',
        get_name(("constant", "constant")) : 'g'
    },
}

C_TESTED_NAMES = [
    get_name(("basic", "basic")),
    get_name(("constant", "constant"))
]

def transform0(s):
    sum_used = 0
    for i in range(5):
        sum_used += s[f"used{i}"]
    return sum_used / sum(POP_DISTR)

def transform1(s):
    return s["budget"]

C_TRANSFORM = {
    "used%" : transform0,
    "money" : transform1
}


def check_c_pp_setup(tested_strats):
    for d in [C_GRAPH_NAMES, C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        assert C_N_GRAPHS == len(d)
    for d in [C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        for n in C_GRAPH_NAMES:
            assert n in d
    for n in C_TESTED_NAMES:
        for _, d in C_COLOURS.items():
            assert n in d
    assert len(tested_strats) == len(C_TESTED_NAMES)
    for a, i in tested_strats:
        get_name((a,i)) in C_TESTED_NAMES
