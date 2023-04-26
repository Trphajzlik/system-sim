from math import floor
from constants import FUEL_COST_PER_CAP, TOTAL_POP, BUS_EFFICIENCY, TICKET_COST, PRICE_ONE_BUS, PRICE_ONE_AD, ONE_BUS_CAPACITY

def ticket_sales(used):
    return used * TICKET_COST

def expenses(max_cap):
    return max_cap * FUEL_COST_PER_CAP

# TODO: Think about more spendinding practices!
# Model can be adjusted that it takes the whole history,
# so you can get creative. Also what param it takes

def spend_ad_basic(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if used / max_cap < BUS_EFFICIENCY:
        return PRICE_ONE_AD
    return 0

def spend_invest_basic(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if used / max_cap > BUS_EFFICIENCY:
        return PRICE_ONE_BUS
    return 0

def spend_ad_constant(history, data):
    return 0

def spend_invest_constant(history, data):
    return 0

def spend_ad_try(history, data):
    l = len(history)
    if l < 40:
        return 0
    if l < 60:
        return PRICE_ONE_AD
    return 0

def spend_ad_try2(history, data):
    l = len(history)
    if l < 40:
        return 0
    if l < 60:
        return 2*PRICE_ONE_AD
    return 0

def spend_ad_once(history, data):
    l = len(history)
    if l == 41:
        return PRICE_ONE_AD
    return 0

def spend_invest_basic_memory(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    n_bus_build = sum([history[-1][f"invest{i}"] for i in range(6)])
    if used / (max_cap + n_bus_build * ONE_BUS_CAPACITY) > BUS_EFFICIENCY:
        return PRICE_ONE_BUS
    return 0


def did_invest(history, data):
    for i, s in enumerate(history):
        if s["invest0"] > 0:
            return i
    return False

def spend_ad_pop_aware(history, data):
    if did_invest(history, data):
        return 2 * PRICE_ONE_AD
    return 0

def stabilised(history, data):
    if len(history) < 4:
        return False
    u_0 = history[-1]["used"]
    u_1 = history[-2]["used"]
    u_2 = history[-3]["used"]
    u_3 = history[-4]["used"]
    if abs(u_0 - u_1) > 0.05 * TOTAL_POP:
        return False
    if abs(u_0 - u_1) > 0.05 * TOTAL_POP:
        return False
    if abs(u_0 - u_1) > 0.05 * TOTAL_POP:
        return False
    return True

def spend_invest_pop_aware(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    n_bus_build = sum([history[-1][f"invest{i}"] for i in range(6)])
    if used / (max_cap + n_bus_build * ONE_BUS_CAPACITY) > BUS_EFFICIENCY:
        if used / (max_cap + n_bus_build * ONE_BUS_CAPACITY) < 0.75 * TOTAL_POP:
            return PRICE_ONE_BUS
    return 0

def spend_invest_buy_opt70(history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / 0.7 - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_invest_buy_opt75(history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / 0.75 - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_invest_buy_opt80(history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / 0.8 - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_invest_buy_opt85(history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / 0.85 - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_invest_buy_opt90(history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / 0.9 - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_ad_at_5(history, data):
    if len(history) != 5:
        return 0
    return 2 * PRICE_ONE_AD

def spend_ad_cont(history, data):
    return PRICE_ONE_AD

SPEND_STRATEGIES = {
    "basic" : (spend_ad_basic, spend_invest_basic),
    "constant": (spend_ad_constant, spend_invest_constant),
    "try_ad" : (spend_ad_try, spend_invest_constant),
    "try_ad2" : (spend_ad_try2, spend_invest_constant),
    "try_ad_once" : (spend_ad_once, spend_invest_constant),

    "basic_with_memory" : (spend_ad_basic, spend_invest_basic_memory),
    "pop_aware" : (spend_ad_pop_aware, spend_invest_pop_aware),

    "buy_opt70" : (spend_ad_basic, spend_invest_buy_opt70),
    "buy_opt75" : (spend_ad_basic, spend_invest_buy_opt75),
    "buy_opt80" : (spend_ad_basic, spend_invest_buy_opt80),
    "buy_opt85" : (spend_ad_basic, spend_invest_buy_opt85),
    "buy_opt90" : (spend_ad_basic, spend_invest_buy_opt90),


    "ab_opt70" : (spend_ad_at_5, spend_invest_buy_opt70),
    "ab_opt75" : (spend_ad_at_5, spend_invest_buy_opt75),
    "ab_opt80" : (spend_ad_at_5, spend_invest_buy_opt80),
    "ab_opt85" : (spend_ad_at_5, spend_invest_buy_opt85),
    "ab_opt90" : (spend_ad_at_5, spend_invest_buy_opt90),

    "abc_opt70" : (spend_ad_cont, spend_invest_buy_opt70),
    "abc_opt75" : (spend_ad_cont, spend_invest_buy_opt75),
    "abc_opt80" : (spend_ad_cont, spend_invest_buy_opt80),
    "abc_opt85" : (spend_ad_cont, spend_invest_buy_opt85),
    "abc_opt90" : (spend_ad_cont, spend_invest_buy_opt90),
# Fituje mezi modrou zelenou
#    "" : 0,

# Fituje mezi modrou červenou
#    "" : 0,

# Nastaví max_cap na ideál a snaží se nacpat lidi do busů
#    "" : 0,
}


def spend_ad(strategy, history, data):
    return SPEND_STRATEGIES[strategy][0](history, data)

def spend_invest(strategy, history, data):
    return SPEND_STRATEGIES[strategy][1](history, data)
