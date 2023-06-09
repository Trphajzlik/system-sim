from setup import TOTAL_POP
from math import log
from constants import BUS_EFFICIENCY

N_GRAPHS = 2

GRAPH_NAMES = [
    "used",
    "money"
]

GRAPH_PATHS = {
    "used" : "used.png",
    "money" : "budget.png"
}

GRAPH_ENTRY_NAMES = {
    "used" : ["used", "max_c", "c75", "eff_c", "invested", "ad_bought"],
    "money" : ["budget"]
}

COLOURS = {
    "used" : {
        "used" : 'k',
        "max_c" : 'g',
        "c75" : 'r',
        "eff_c" : 'b',
        "invested": 'om:',
        "ad_bought": 'oc:'
    },
    "money" : {
        "budget" : 'y'
    }
}

def transform0(s):
    return {
        "used" : s["used"] / TOTAL_POP,
        "max_c" : s["max_capacity"] / TOTAL_POP,
        "c75" : s["max_capacity"] * 0.75 / TOTAL_POP,
        "eff_c" : s["max_capacity"] * BUS_EFFICIENCY / TOTAL_POP,
        "invested" : 0,#s["invest0"] * 0.1,
        "ad_bought" : 0,#s["ad0"] * 0.1
    }

def transform1(s):
    return {
        "budget" :  s["budget"]
    }

TRANSFORM = {
    "used" : transform0,
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

