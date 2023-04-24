from math import log

N_GRAPHS = 2

GRAPH_NAMES = [
    "used%",
    "money"
]

GRAPH_PATHS = {
    "used%" : "graph0.png",
    "money" : "graph1.png"
}

GRAPH_ENTRY_NAMES = {
    "used%" : ["a'", "c'"],
    "money" : ["b'", "step_count'"]
}

COLOURS = {
    "used%" : {
        "a'": 'r', "c'": 'g'
    },
    "money" : {
        "b'" : 'r',
        "step_count'" : 'm'
    }
}

def transform0(s):
    return {
        "a'" : s["a"],
        "c'" : 3 * s["c"]
    }

def transform1(s):
    return {
        "b'" :  s["b"],
        "step_count'" : s["step_count"]
    }

TRANSFORM = {
    "used%" : transform0,
    "money" : transform1
}

def check_postprocess_setup():
    for d in [GRAPH_NAMES, GRAPH_PATHS, GRAPH_ENTRY_NAMES, COLOURS, TRANSFORM]:
        assert N_GRAPHS == len(d)
    for d in [GRAPH_PATHS, GRAPH_ENTRY_NAMES, COLOURS, TRANSFORM]:
        for n in GRAPH_NAMES:
            assert n in d
    for gn in GRAPH_NAMES:
        for n in GRAPH_ENTRY_NAMES[gn]:
            assert n in COLOURS[gn]

