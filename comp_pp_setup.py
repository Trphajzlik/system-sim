from setup import TOTAL_POP
from rules import SPEND_STRATEGIES

C_N_GRAPHS = 13

C_GRAPH_NAMES = [
    "used%",
    "try_ads",
    "max_capacity",
    "try_ads_b",
    "buy_opt",
    "buy_opt_b",
    "db_opt",
    "db_opt_b",
    "ab_opt",
    "ab_opt_b",
    "abc_opt",
    "abc_opt_b",
    "money",
]

C_GRAPH_PATHS = {
    "used%" : "int_used.png",
    "max_capacity" : "int_max_cap.png",
    "try_ads" : "try_ads.png",
    "try_ads_b" : "try_ads_b.png",
    "buy_opt" : "buy_opt.png",
    "buy_opt_b" : "buy_opt_b.png",
    "db_opt" : "db_opt.png",
    "db_opt_b" : "db_opt_b.png",
    "ab_opt" : "ab_opt.png",
    "ab_opt_b" : "ab_opt_b.png",
    "abc_opt" : "abc_opt.png",
    "abc_opt_b" : "abc_opt_b.png",
    "money" : "int_money.png",
}

INTERESTING_COLOURS = {
    "basic" : 'r',
    "no_investment" : 'tab:orange',
    "constant_ad" : 'g',
    "basic_with_memory" : 'b',
    "pop_aware" : 'c',
    "buy_opt85" : 'k',
    "ab_opt90" : 'm',
    "db_opt90" : 'tab:purple',
    "abc_opt90" : 'y',
}

TRY_AD_COLOURS = {
    "no_investment" : 'r',
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

DB_OPT_COLOURS = {
    "ab_opt65" : 'r',
    "ab_opt70" : 'g',
    "ab_opt75" : 'b',
    "ab_opt80" : 'c',
    "ab_opt85" : 'm',
    "ab_opt90" : 'y',
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
    "used%" : INTERESTING_COLOURS,
    "money" : INTERESTING_COLOURS,
    "max_capacity" : INTERESTING_COLOURS,
    "try_ads" : TRY_AD_COLOURS,
    "try_ads_b" : TRY_AD_COLOURS,
    "buy_opt" : BUY_OPT_COLOURS,
    "buy_opt_b" : BUY_OPT_COLOURS,
    "db_opt" : DB_OPT_COLOURS,
    "db_opt_b" : DB_OPT_COLOURS,
    "ab_opt" : AB_OPT_COLOURS,
    "ab_opt_b" : AB_OPT_COLOURS,
    "abc_opt" : ABC_OPT_COLOURS,
    "abc_opt_b" : ABC_OPT_COLOURS,
}

def get_used_p(s):
    return s["used"] / TOTAL_POP

def get_budget(s):
    return s["budget"]

def get_max_cap(s):
    return s["max_capacity"]

C_TRANSFORM = {
    "used%" : get_used_p,
    "try_ads" : get_used_p,
    "max_capacity" : get_max_cap,
    "buy_opt" : get_used_p,
    "db_opt" : get_used_p,
    "ab_opt" : get_used_p,
    "abc_opt" : get_used_p,
    "money" : get_budget,
    "try_ads_b" : get_budget,
    "buy_opt_b" : get_budget,
    "db_opt_b" : get_budget,
    "ab_opt_b" : get_budget,
    "abc_opt_b" : get_budget,
}

def check_c_pp_setup(tested_strats):
    for d in [C_GRAPH_NAMES, C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        assert C_N_GRAPHS == len(d)
    for d in [C_GRAPH_PATHS, C_COLOURS, C_TRANSFORM]:
        for n in C_GRAPH_NAMES:
            assert n in d
