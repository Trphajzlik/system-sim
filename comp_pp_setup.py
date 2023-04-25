from setup import TOTAL_POP

C_N_GRAPHS = 2

C_GRAPH_NAMES = [
    "used%",
    "money",
]

C_GRAPH_PATHS = {
    "used%" : "c_graph0.png",
    "money" : "c_graph1.png",
}

C_COLOURS = {
    "used%" : {
        "basic" : 'r',
        "constant" : 'g',
        "try_ad" :'b',
        "basic_with_memory" : 'y',
        "pop_aware" : 'm',
    },
    "money" : {
        "basic" : 'r',
        "constant" : 'g',
        "try_ad" : 'b',
        "basic_with_memory" : 'y',
        "pop_aware" : 'm',
    },
}

C_TESTED_NAMES = [
    "basic", "constant", "try_ad", "basic_with_memory",
    "pop_aware",
]

def transform0(s):
    return s["used"] / TOTAL_POP

def transform1(s):
    return s["budget"]

C_TRANSFORM = {
    "used%" : transform0,
    "money" : transform1,
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
    for strat in tested_strats:
        strat in C_TESTED_NAMES
