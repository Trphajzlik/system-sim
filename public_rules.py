from math import floor
from constants import TOTAL_POP, OP_CAP_VALS, OP_AD_VALS, RUMOR_IMPACT, FORGET, MEM_RELEVANCE, MEM_WEIGHT, AD_REL_USED

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

def capacity_opinion(used, max_cap):
    # Returns number in [0,1]
    # Used multiplicatively
    ratio = used / max_cap
    cap_opinion =  lin_interpolate_set(ratio, OP_CAP_VALS)
    assert cap_opinion <= 1
    assert cap_opinion >= 0
    return cap_opinion

def ad_opinion(n_ads):
    # Returns "any" number
    # Used additively
    return lin_interpolate_set(n_ads, OP_AD_VALS)

def clamp(i):
    if i < 0:
        return 0
    if i > 1:
        return 1
    return i

def memory(relevant_history):
    # Returns number in [0,1]
    # Used multiplicatively
    cap_mem = 0
    forgetfulness = 1
    mem_offset = 0
    for i in range(len(relevant_history)-2, -1, -1):
        used, max_c = relevant_history[i]
        step_op = forgetfulness * capacity_opinion(used, max_c)
        cap_mem += step_op
        mem_offset += forgetfulness
        forgetfulness *= FORGET
        if forgetfulness < MEM_RELEVANCE:
            break
    if mem_offset == 0:
        return None
    cap_mem = cap_mem / mem_offset
    assert cap_mem <= 1
    assert cap_mem >= 0
    return cap_mem

def incl(relevant_history, n_ads):
    # Returns number of persons that will use public transport
    # Each person has a probability that they will use
    # public transport. This is influenced by:
    #  - rumors about comfort (i.e. capacity)
    #  - ads
    op_mem = memory(relevant_history)
    used, max_c = relevant_history[-1]
    op_cap = capacity_opinion(used, max_c)
    op_a = ad_opinion(n_ads)
    if op_mem is None:
        op_weig = op_cap
    else:
        op_weig = (op_cap + op_mem * MEM_WEIGHT) / (MEM_WEIGHT + 1)

    used_and_will_use = used * clamp(op_weig + AD_REL_USED * op_a)
    not_used_will_use = (TOTAL_POP - used) * clamp(RUMOR_IMPACT * op_weig + op_a)
    return used_and_will_use + not_used_will_use
