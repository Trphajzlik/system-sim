from math import floor

# TODO: Review function `incl`, it is the most important
# part of our model, so it has to do what we want it
# to do!

def cap_opinion(sum_used, max_cap):
    # Returns pair of opinions (o_1, o_2):
    #  - o_1 influences ppl who used public
    #    transport, meaning personal experience
    #  - o_2 influences ppl who didn't,
    #    meaning "common" rumors
    ratio = sum_used / max_cap
    if ratio < 0.5:
        return (2, 1.5)
    elif ratio < 0.7:
        return (1.5, 1.25)
    elif ratio < 0.9:
        return (1, 1)
    elif ratio < 1.0:
        return (0.7, 0.85)
    else: # Some didn't even get into bus
        return (0.4, 0.7)

def ad_opinion(ads):
    # Spending 500.000 will increase mult opinion by 5%
    # Spending 1.000.000 will increase mult opinion by 7.5%
    # Spending 1.500.000 will increase mult opinion by 8.75%
    # ...> 
    # a_0 = 0
    # a_n = a_{n-1} + 5 / 2^{n-1}
    # Wolfram says that it is equal to
    # 10 - 5/2^n
    # Maybe play with the constant `2` -> 1.8?
    return 1 + 0.01 * (10 - 5 / (2**floor(0.00001 * ads)))

def clamp(i):
    if i < 0:
        return 0
    if i > 1:
        return 1
    return i

def incl(nat_incl, pop_c, used_c, sum_used, max_cap, ads):
    # Each person from a class has a probability that they will use
    # public transport. This is influenced by:
    #  - "class inclination"
    #  - rumors about comfort (i.e. capacity)
    #  - ads

    op_u, op_n = cap_opinion(sum_used, max_cap)
    op_a = ad_opinion(ads)

    # Probability that someone who did use will use
    p_u = clamp(nat_incl * op_u * op_a)
    # Probability that someone who didnt use will use
    p_n = clamp(nat_incl * op_n * op_a)

    return used_c * p_u + (pop_c - used_c) * p_n


def ticket_sales(sum_used):
    return sum_used * 2000

def expenses(max_cap):
    return max_cap * 1000

# TODO: Think about more spendinding practices!
# Model can be adjusted that it takes the whole history,
# so you can get creative. Also what param it takes

def spend_ad_basic(sum_used, max_cap, budget):
    if sum_used / max_cap <= 0.6:
        # 0.5 mil
        return 500000
    return 0

def spend_invest_basic(sum_used, max_cap, budget):
    if sum_used / max_cap >= 0.8:
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
