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
        return 2 * PRICE_ONE_AD
    return 0

def spend_invest_basic(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if used / max_cap > BUS_EFFICIENCY:
        return PRICE_ONE_BUS
    return 0

def spend_invest_basic_memory(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    n_bus_build = sum([history[-1][f"invest{i}"] for i in range(6)])
    future_cap = max_cap + n_bus_build * ONE_BUS_CAPACITY
    if used > BUS_EFFICIENCY * future_cap:
        return PRICE_ONE_BUS
    return 0

def dont_invest(history, data):
    return 0

def spend_ad_try(amount, history, data):
    l = len(history)
    if l < 40:
        return 0
    if l < 60:
        return amount * PRICE_ONE_AD
    return 0

def spend_ad_once(history, data):
    l = len(history)
    if l == 41:
        return 2 * PRICE_ONE_AD
    return 0

def spend_ad_pop_aware(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if used / max_cap < 0.75:
        return 2 * PRICE_ONE_AD
    return 0

def spend_invest_pop_aware(history, data):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    n_bus_build = sum([history[-1][f"invest{i}"] for i in range(6)])
    future_cap = max_cap + n_bus_build * ONE_BUS_CAPACITY
    if used > BUS_EFFICIENCY * future_cap:
        # TOTAL_POP < c * future_cap does not make sense
        if TOTAL_POP > 0.9 * future_cap:
            return PRICE_ONE_BUS
    return 0

def spend_invest_buy_opt(ratio, history, data):
    if len(history) != 1:
        return 0
    return PRICE_ONE_BUS * (TOTAL_POP / ratio - history[0]["max_capacity"]) / ONE_BUS_CAPACITY

def spend_ad_at_5(history, data):
    if len(history) != 5:
        return 0
    return 2 * PRICE_ONE_AD

def spend_ad_cont(history, data):
    return 2 * PRICE_ONE_AD

SPEND_STRATEGIES = {
    "no_investment" : (dont_invest, dont_invest),
    "constant_ad": ((lambda h, d : 2 * PRICE_ONE_AD), dont_invest),
    "basic" : (spend_ad_basic, spend_invest_basic),
    "try_ad_once" : (spend_ad_once, dont_invest),

    "basic_with_memory" : (spend_ad_basic, spend_invest_basic_memory),
    "pop_aware" : (spend_ad_pop_aware, spend_invest_pop_aware),

    "try_ad1" : ((lambda h, d: spend_ad_try(1, h, d)), dont_invest),
    "try_ad2" : ((lambda h, d: spend_ad_try(2, h, d)), dont_invest),
    "try_ad3" : ((lambda h, d: spend_ad_try(3, h, d)), dont_invest),
    "try_ad4" : ((lambda h, d: spend_ad_try(4, h, d)), dont_invest),
    "try_ad5" : ((lambda h, d: spend_ad_try(5, h, d)), dont_invest),

    "db_opt65" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.65, h, d))),
    "db_opt70" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.7, h, d))),
    "db_opt75" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.75, h, d))),
    "db_opt80" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.8, h, d))),
    "db_opt85" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.85, h, d))),
    "db_opt90" : (dont_invest, (lambda h, d : spend_invest_buy_opt(0.9, h, d))),

    "buy_opt65" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.65, h, d))),
    "buy_opt70" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.7, h, d))),
    "buy_opt75" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.75, h, d))),
    "buy_opt80" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.8, h, d))),
    "buy_opt85" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.85, h, d))),
    "buy_opt90" : (spend_ad_basic, (lambda h, d : spend_invest_buy_opt(0.9, h, d))),

    "ab_opt65" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.65, h, d))),
    "ab_opt70" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.7, h, d))),
    "ab_opt75" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.75, h, d))),
    "ab_opt80" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.8, h, d))),
    "ab_opt85" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.85, h, d))),
    "ab_opt90" : (spend_ad_at_5, (lambda h, d : spend_invest_buy_opt(0.9, h, d))),

    "abc_opt65" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.65, h, d))),
    "abc_opt70" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.7, h, d))),
    "abc_opt75" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.75, h, d))),
    "abc_opt80" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.8, h, d))),
    "abc_opt85" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.85, h, d))),
    "abc_opt90" : (spend_ad_cont, (lambda h, d : spend_invest_buy_opt(0.9, h, d))),
}


def spend_ad(strategy, history, data):
    return SPEND_STRATEGIES[strategy][0](history, data)

def spend_invest(strategy, history, data):
    return SPEND_STRATEGIES[strategy][1](history, data)
