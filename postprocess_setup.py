from setup import POP_DISTR
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
    "used%" : [f"used{i}%" for i in range(5)] + ["invested", "ad_bought"],
    "money" : ["budget", "invest", "ad"]
}

COLOURS = {
    "used%" : {
        "used0%": 'r', "used1%": 'g', "used2%": 'b',
        "used3%": 'y', "used4%": 'k', "invested": 'm',
        "ad_bought": 'c'
    },
    "money" : {
        "budget" : 'r',
        "invest" : 'm',
        "ad" : 'y'
    }
}

def transform0(s):
    return dict ({
        f"used{i}%" : s[f"used{i}"] / POP_DISTR[i] for i in range(5)
    }, **{
        "invested" : s["invest0"] * 0.1 / 5000000,
        "ad_bought" : s["ad0"] * 0.1 / 500000
    })

def transform1(s):
    def clog(r):
        if r > 0:
            return log(r)
        if r < 0:
            return -log(-r)
        return 0
    return {
        "budget" :  clog(s["budget"]),
        "invest" : clog(s["invest0"]),
        "ad" : clog(s["ad0"])
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

