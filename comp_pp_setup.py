from setup import TOTAL_POP
from rules import SPEND_STRATEGIES

C_N_GRAPHS = 10

C_GRAPH_NAMES = [
    "used%",
    "try_ads",
    "try_ads_b",
    "buy_opt",
    "buy_opt_b",
    "ab_opt",
    "ab_opt_b",
    "abc_opt",
    "abc_opt_b",
    "money",
]

C_GRAPH_PATHS = {
    "used%" : "c_graph0.png",
    "try_ads" : "try_ads.png",
    "try_ads_b" : "try_ads_b.png",
    "buy_opt" : "buy_opt.png",
    "buy_opt_b" : "buy_opt_b.png",
    "ab_opt" : "ab_opt.png",
    "ab_opt_b" : "ab_opt_b.png",
    "abc_opt" : "abc_opt.png",
    "abc_opt_b" : "abc_opt_b.png",
    "money" : "c_graph1.png",
}

TRY_AD_COLOURS = {
    "constant" : 'r',
    "try_ad1" : 'g',
    "try_ad2" : 'b',
    "try_ad3" : 'c',
    "try_ad4" : 'm',
    "try_ad5" : 'y',
}

BUY_OPT_COLOURS = {
    "buy_opt65" : 'r',
    "buy_opt70" : 'g',
    "buy_opt75" : 'b',
    "buy_opt80" : 'c',
    "buy_opt85" : 'm',
    "buy_opt90" : 'y',
}

AB_OPT_COLOURS = {
    "ab_opt65" : 'r',
    "ab_opt70" : 'g',
    "ab_opt75" : 'b',
    "ab_opt80" : 'c',
    "ab_opt85" : 'm',
    "ab_opt90" : 'y',
}

ABC_OPT_COLOURS = {
    "ab_opt65" : 'r',
    "ab_opt70" : 'g',
    "ab_opt75" : 'b',
    "ab_opt80" : 'c',
    "ab_opt85" : 'm',
    "ab_opt90" : 'y',
}

C_COLOURS = {
    "used%" : {
        "basic" : 'r',
        "constant" : 'r',
        "try_ad1" :'r',
        "basic_with_memory" : 'r',
        "pop_aware" : 'r',
        "try_ad_once" : 'r',
    },
    "try_ads" : TRY_AD_COLOURS,
    "try_ads_b" : TRY_AD_COLOURS,
    "buy_opt" : BUY_OPT_COLOURS,
    "buy_opt_b" : BUY_OPT_COLOURS,
    "ab_opt" : AB_OPT_COLOURS,
    "ab_opt_b" : AB_OPT_COLOURS,
    "abc_opt" : ABC_OPT_COLOURS,
    "abc_opt_b" : ABC_OPT_COLOURS,
    "money" : {
        "basic" : 'r',
        "constant" : 'r',
        "try_ad1" : 'r',
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

def get_used_p(s):
    return s["used"] / TOTAL_POP

def get_budget(s):
    return s["budget"]

C_TRANSFORM = {
    "used%" : get_used_p,
    "try_ads" : get_used_p,
    "buy_opt" : get_used_p,
    "ab_opt" : get_used_p,
    "abc_opt" : get_used_p,
    "try_ads_b" : get_budget,
    "buy_opt_b" : get_budget,
    "ab_opt_b" : get_budget,
    "abc_opt_b" : get_budget,
    "money" : get_budget,
}


def check_c_pp_setup(tested_strats):
    for d in [C_GRAPH_NAMES, C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        assert C_N_GRAPHS == len(d)
    for d in [C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        for n in C_GRAPH_NAMES:
            assert n in d
