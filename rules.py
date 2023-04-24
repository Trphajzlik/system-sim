from math import floor
from constants import CAP50, CAP75, CAP90, CAP100, RUMOR_IMPACT, AD_IMPACT, AD_DROPOFF, BUS_EFFICIENCY, TICKET_COST, FORGET, MEM_RELEVANCE

# TODO: Review function `incl`, it is the most important
# part of our model, so it has to do what we want it
# to do!

def lin_interpolate(x, x_0, y_0, x_1, y_1):
    return y_0 * (x_1 - x) / (x_1 - x_0) + y_1 * (x - x_0) / (x_1 - x_0)

def capacity_opinion(sum_used, max_cap):
    ratio = sum_used / max_cap
    cap = 0
    if ratio < 0.5:
        cap = CAP50
    elif ratio < 0.75:
        cap = lin_interpolate(ratio, 0.5, CAP50, 0.75, CAP75)
    elif ratio < 0.9:
        cap = lin_interpolate(ratio, 0.75, CAP75, 0.9, CAP90)
    elif ratio < 1.0:
        cap = lin_interpolate(ratio, 0.9, CAP90, 1.0, CAP100)
    else: # Some didn't even get into bus
        cap = CAP100
    # We wont differentiate between personal experience
    # and rummors so we can more easily do "memory"
    return cap

def ad_opinion(ads):
    # Spending 500.000 will increase mult opinion by AD_IMPACT%
    return 1 + 0.01 * ((2 * AD_IMPACT) - AD_IMPACT / (AD_DROPOFF**floor(0.00001 * ads)))

def clamp(i):
    if i < 0:
        return 0
    if i > 1:
        return 1
    return i

def incl(pop_c, relevant_history, ads):
    # Each person has a probability that they will use
    # public transport. This is influenced by:
    #  - rumors about comfort (i.e. capacity)
    #  - ads
    # We def should add some affinity towards history
    # so that the constant spending converges at least a bit,
    # Or at least is less erradic
    """
    op_cap = 0
    forgetfulness = 1
    mem_offset = 0
    for total_u, max_c in reversed(relevant_history):
        step_op = forgetfulness * capacity_opinion(total_u, max_c)
        #weighted_op = total_u * step_op + (pop_c - total_u) * step_op * RUMOR_IMPACT
        # Adding using vs not using ppl, should create desired ad behaviour
        #op_cap += weighted_op / pop_c
        op_cap += step_op
        mem_offset += forgetfulness
        forgetfulness *= FORGET
        if forgetfulness < MEM_RELEVANCE:
            break

    op_cap = op_cap / mem_offset
    """
    used, max_c = relevant_history[-1]
    op_cap = capacity_opinion(used, max_c)
    op_a = ad_opinion(ads)

    return used * clamp(op_cap * op_a) + (pop_c - used) * clamp(RUMOR_IMPACT * op_cap * op_a)


def ticket_sales(sum_used):
    return sum_used * TICKET_COST

def expenses(max_cap):
    return max_cap * TICKET_COST * BUS_EFFICIENCY

# TODO: Think about more spendinding practices!
# Model can be adjusted that it takes the whole history,
# so you can get creative. Also what param it takes

def spend_ad_basic(sum_used, max_cap, budget):
    if sum_used / max_cap < BUS_EFFICIENCY:
        # 0.5 mil
        return 500000
    return 0

def spend_invest_basic(sum_used, max_cap, budget):
    if sum_used / max_cap > BUS_EFFICIENCY:
        # 5 mil
        return 5000000
    return 0

def spend_ad_constant(sum_used, max_cap, budget):
    return 0

def spend_invest_constant(sum_used, max_cap, budget):
    return 0


SPEND_AD = {
    "basic" : spend_ad_basic,
    "constant": spend_ad_constant
}
SPEND_INVEST = {
    "basic" : spend_invest_basic,
    "constant": spend_invest_constant
}

def spend_ad(strategy, sum_used, max_cap, budget):
    return SPEND_AD[strategy](sum_used, max_cap, budget)

def spend_invest(strategy, sum_used, max_cap, budget):
    return SPEND_INVEST[strategy](sum_used, max_cap, budget)
