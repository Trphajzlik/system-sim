from setup import TOTAL_POP
from rules import SPEND_STRATEGIES

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
        "constant" : 'r',
        "try_ad" :'r',
        "basic_with_memory" : 'r',
        "pop_aware" : 'r',
        "try_ad2" : 'r',
        "try_ad_once" : 'r',
        "buy_opt70" : 'g',
        "buy_opt75" : 'b',
        "buy_opt80" : 'c',
        "buy_opt85" : 'm',
        "buy_opt90" : 'y',
        "ab_opt70" : 'g',
        "ab_opt75" : 'b',
        "ab_opt80" : 'c',
        "ab_opt85" : 'm',
        "ab_opt90" : 'y',
        "abc_opt70" : 'g',
        "abc_opt75" : 'b',
        "abc_opt80" : 'c',
        "abc_opt85" : 'm',
        "abc_opt90" : 'y',
    },
    "money" : {
        "basic" : 'r',
        "constant" : 'r',
        "try_ad" : 'r',
        "basic_with_memory" : 'r',
        "pop_aware" : 'r',
        "try_ad2" : 'r',
        "try_ad_once" : 'r',
        "buy_opt70" : 'g',
        "buy_opt75" : 'b',
        "buy_opt80" : 'c',
        "buy_opt85" : 'm',
        "buy_opt90" : 'y',
        "ab_opt70" : 'g',
        "ab_opt75" : 'b',
        "ab_opt80" : 'c',
        "ab_opt85" : 'm',
        "ab_opt90" : 'y',
        "abc_opt70" : 'g',
        "abc_opt75" : 'b',
        "abc_opt80" : 'c',
        "abc_opt85" : 'm',
        "abc_opt90" : 'y',
    },
}

C_TESTED_NAMES = [
#    "basic", "constant", "try_ad", "basic_with_memory",
#    "pop_aware",
    n for n in SPEND_STRATEGIES
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
