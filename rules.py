# TODO: Review function `incl`, it is the most important
# part of our model, so it has to do what we want it
# to do!

def cap_opinion(sum_used, max_cap):
    # TODO
    # Returns pair of opinions (o_1, o_2):
    #  - o_1 influences ppl who used public
    #    transport, meaning personal experience
    #    + "personal" rumors that affect others
    #  - o_2 influences ppl who didn't,
    #    meaning "common" rumors
    ratio = sum_used / max_cap
    if ratio < 0.5:
        return (1,1)
    elif ratio < 0.7:
        return (1,1)
    elif ratio < 0.9:
        return (1,1)
    elif ratio < 1.0:
        return (1,1)
    else: # Some didn't even get into bus
        return (1,1)

def incl(nat_incl, pop_c, used_c, sum_used, max_cap, ads):
    # TODO -- multiplicative vs additive
    # Each person from a class has a probability that they will use
    # public transport. This is influenced by:
    #  - "class inclination"
    #  - rumors about comfort (i.e. capacity)
    #  - ads
    op_u, op_n = cap_opinion(sum_used, max_cap)

    # Probability that someone who did use will use
    p_u = 0
    # Probability that someone who didnt use will use
    p_n = 0

    return nat_incl * pop_c


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


SPEND_AD = {
    "basic" : spend_ad_basic
}
SPEND_INVEST = {
    "basic" : spend_invest_basic
}

def spend_ad(strategy, sum_used, max_cap, budget):
    return SPEND_AD[strategy](sum_used, max_cap, budget)

def spend_invest(strategy, sum_used, max_cap, budget):
    return SPEND_INVEST[strategy](sum_used, max_cap, budget)
