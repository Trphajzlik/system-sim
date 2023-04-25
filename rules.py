from math import floor
from constants import TOTAL_POP, CAP_VALS, AD_VALS, RUMOR_IMPACT, BUS_EFFICIENCY, TICKET_COST, FORGET, MEM_RELEVANCE, MEM_WEIGHT, ONE_BUS, ONE_AD, AD_REL_USED
# TODO: Review function `incl`, it is the most important
# part of our model, so it has to do what we want it
# to do!

def lin_interpolate(x, x_0, y_0, x_1, y_1):
    return y_0 * (x_1 - x) / (x_1 - x_0) + y_1 * (x - x_0) / (x_1 - x_0)

def lin_interpolate_set(x, vals):
    # We assume that xs are ordered
    if x < vals[0][0]:
        return vals[0][1]
    if x >= vals[-1][0]:
        return vals[-1][1]
    x_l, y_l = vals[0]
    for x_u, y_u in vals[1:]:
        if x < x_u:
            return lin_interpolate(x, x_l, y_l, x_u, y_u)
        x_l, y_l = x_u, y_u
    raise RuntimeError("Bug in linear interpolation!")

def capacity_opinion(sum_used, max_cap):
    ratio = sum_used / max_cap
    return lin_interpolate_set(ratio, CAP_VALS)

def ad_opinion(ads):
    return lin_interpolate_set(ads, AD_VALS)

def clamp(i):
    if i < 0:
        return 0
    if i > 1:
        return 1
    return i

def memory(pop_c, relevant_history):
    mem_cap = 0
    forgetfulness = 1
    mem_offset = 0
    for i in range(len(relevant_history)-2, -1, -1):
        total_u, max_c = relevant_history[i]
        step_op = forgetfulness * capacity_opinion(total_u, max_c)
        mem_cap += step_op
        mem_offset += forgetfulness
        forgetfulness *= FORGET
        if forgetfulness < MEM_RELEVANCE:
            break
    if mem_offset == 0:
        return None
    mem_cap = mem_cap / mem_offset
    return mem_cap

def incl(pop_c, relevant_history, ads):
    # Each person has a probability that they will use
    # public transport. This is influenced by:
    #  - rumors about comfort (i.e. capacity)
    #  - ads
    # We def should add some affinity towards history
    # so that the constant spending converges at least a bit,
    # Or at least is less erradic
    op_mem = memory(pop_c, relevant_history)
    used, max_c = relevant_history[-1]
    op_cap = capacity_opinion(used, max_c)
    op_a = ad_opinion(ads)
    if op_mem is None:
        op_weig = op_cap
    else:
        op_weig = (op_cap + op_mem * MEM_WEIGHT) / (MEM_WEIGHT + 1)

    return used * clamp(op_weig + AD_REL_USED * op_a) + (pop_c - used) * clamp(RUMOR_IMPACT * op_weig + op_a)


def ticket_sales(sum_used):
    return sum_used * TICKET_COST

def expenses(max_cap):
    return max_cap * TICKET_COST * BUS_EFFICIENCY

# TODO: Think about more spendinding practices!
# Model can be adjusted that it takes the whole history,
# so you can get creative. Also what param it takes

def spend_ad_basic(history):
    sum_used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if sum_used / max_cap < BUS_EFFICIENCY:
        # 0.5 mil
        return ONE_AD
    return 0

def spend_invest_basic(history):
    sum_used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    if sum_used / max_cap > BUS_EFFICIENCY:
        # 5 mil
        return ONE_BUS
    return 0

def spend_ad_constant(history):
    return 0

def spend_invest_constant(history):
    return 0

def spend_ad_try(history):
    l = len(history)
    if l < 40:
        return 0
    if l < 60:
        return ONE_AD
    return 0

def spend_invest_basic_memory(history):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    bonus_max_cap = sum([history[-1][f"invest{i}"] for i in range(6)])
    if used / (max_cap + bonus_max_cap) > BUS_EFFICIENCY:
        return ONE_BUS
    return 0


def did_invest(history):
    for i, s in enumerate(history):
        if s["invest0"] > 0:
            return i
    return False

def spend_ad_pop_aware(history):
    if did_invest(history):
        return 2* ONE_AD
    return 0

def stabilised(history):
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

def spend_invest_pop_aware(history):
    used = history[-1]["used"]
    max_cap = history[-1]["max_capacity"]
    bonus_max_cap = sum([history[-1][f"invest{i}"] for i in range(6)])
    if used / (max_cap + bonus_max_cap) > BUS_EFFICIENCY:
        if used / (max_cap + bonus_max_cap) < 0.75 * TOTAL_POP:
            return ONE_BUS
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


def spend_ad(strategy, history):
    return SPEND_STRATEGIES[strategy][0](history)

def spend_invest(strategy, history):
    return SPEND_STRATEGIES[strategy][1](history)
