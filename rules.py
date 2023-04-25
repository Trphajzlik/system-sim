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


SPEND_STRATEGIES = {
    "basic" : (spend_ad_basic, spend_invest_basic),
    "constant": (spend_ad_constant, spend_invest_constant),
    "try_ad" : (spend_ad_try, spend_invest_constant),
    "basic_with_memory" : (spend_ad_basic, spend_invest_basic_memory),
    "pop_aware" : (spend_ad_pop_aware, spend_invest_pop_aware),

# Fituje mezi modrou zelenou
    "" : 0,

# Fituje mezi modrou červenou
    "" : 0,

# Nastaví max_cap na ideál a snaží se nacpat lidi do busů
    "" : 0,
}


def spend_ad(strategy, history, data):
    return SPEND_STRATEGIES[strategy][0](history, data)

def spend_invest(strategy, history, data):
    return SPEND_STRATEGIES[strategy][1](history, data)
