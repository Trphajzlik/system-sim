from copy import deepcopy
from rules import incl, ticket_sales, expenses, spend_ad, spend_invest, SPEND_AD, SPEND_INVEST

N_STATES = 16

NAMES = [
    "used0", "used1", "used2", "used3", "used4",
    "max_capacity", "budget",
    "ad0", "ad1", "ad2",
    "invest0", "invest1", "invest2", "invest3", "invest4", "invest5"
]

PERC_DISTR = [0.275, 0.25, 0.225, 0.15, 0.10]
NAT_INCL = [0.9, 0.7, 0.4, 0.15, 0.05]

TOTAL_POP = 500000.0

# We divide population into 5 separate classes
# according to their opinion of public transport
# Population does not change
POP_DISTR = [
    PERC_DISTR[0] * TOTAL_POP, PERC_DISTR[1] * TOTAL_POP, PERC_DISTR[2] * TOTAL_POP,
    PERC_DISTR[3] * TOTAL_POP, PERC_DISTR[4] * TOTAL_POP
]
INIT_USED = [
    NAT_INCL[0] * POP_DISTR[0], NAT_INCL[1] * POP_DISTR[1], NAT_INCL[2] * POP_DISTR[2],
    NAT_INCL[3] * POP_DISTR[3], NAT_INCL[4] * POP_DISTR[4]
]
INIT_MAX_CAP = 0.6 * TOTAL_POP
INIT_BUDGET = 50 * 10**6 # 50 mil

INIT_STATE = {
    # For each class, we have how many have used
    # public transport in tha last month
    "used0": INIT_USED[0], "used1": INIT_USED[1], "used2": INIT_USED[2],
    "used3": INIT_USED[3], "used4": INIT_USED[4],

    # Max capacity of public transport
    "max_capacity" : INIT_MAX_CAP,

    # Budget of the city
    # We allow them to go into debt without any penalty
    "budget" : INIT_BUDGET,

    # States handling ads
    "ad0" : 0, "ad1" : 0, "ad2" : 0,

    # States handling investments into increasing
    # capacity of public transport
    "invest0" : 0, "invest1" : 0, "invest2" : 0,
    "invest3" : 0, "invest4" : 0, "invest5" : 0
}

def GET_INIT_STATE():
    return deepcopy(INIT_STATE)

# Wrapper and helper functions for rules

def total_used(state):
    sum_used = 0
    for c in range(5):
        sum_used += state[f"used{c}"]
    return sum_used

def w_ticket_sales(state):
    return ticket_sales(total_used(state))

def w_expenses(state):
    return expenses(state["max_capacity"])

def w_incl(c, state):
    ads = sum([state[f"ad{i}"] for i in range(3)])
    next_used = incl(NAT_INCL[c], POP_DISTR[c], state[f"used{c}"], total_used(state), state["max_capacity"], ads)
    # Only up to 100% of a class can travel
    assert next_used <= POP_DISTR[c]
    return next_used

def w_spend_ad(ad_strategy, history):
    state = history[-1]
    return spend_ad(ad_strategy, total_used(state), state["max_capacity"], state["budget"])

def w_spend_invest(invest_strategy, history):
    state = history[-1]
    return spend_invest(invest_strategy, total_used(state), state["max_capacity"], state["budget"])

RULES = {
    # Logic if population chooses to use public transport
    "used0": (lambda h: w_incl(0, h[-1])), "used1": (lambda h: w_incl(1, h[-1])),
    "used2": (lambda h: w_incl(2, h[-1])), "used3": (lambda h: w_incl(3, h[-1])),
    "used4": (lambda h: w_incl(4, h[-1])),

    # Capacity increases after 6 months after deciding to invest
    "max_capacity" : (lambda h: h[-1]["max_capacity"] + h[-1]["invest5"]),

    # Budget changes based on ticket sales, buying fuel,
    # spending on ads, and spending on buying new buses
    "budget" : (lambda h: 0/0),

    # Ads are in circulation for 3 months
    "ad0" : (lambda h: 0/0),
    "ad1" : (lambda h: h[-1]["ad0"]), "ad2" : (lambda h: h[-1]["ad1"]),

    # It takes 6 months to buy a bus
    # Spending 5 milion will increase max capacity by 5000
    "invest0" : (lambda h: 0/0),
    "invest1" : (lambda h: h[-1]["invest0"]), "invest2" : (lambda h: h[-1]["invest1"]),
    "invest3" : (lambda h: h[-1]["invest2"]), "invest4" : (lambda h: h[-1]["invest3"]),
    "invest5" : (lambda h: h[-1]["invest4"])
}

def GET_RULES(ad_strategy, invest_strategy):
    rules = deepcopy(RULES)
    rules["budget"] = (lambda h: h[-1]["budget"] + w_ticket_sales(h[-1]) - w_expenses(h[-1]) - w_spend_ad(ad_strategy, h) - w_spend_invest(invest_strategy, h))
    rules["ad0"] = (lambda h: w_spend_ad(ad_strategy, h))
    rules["invest0"] = (lambda h: 0.01 * w_spend_invest(invest_strategy, h))
    return rules

TESTED_STRATEGIES = [("basic","basic"), ("constant", "constant")]

STEPS = 120
OUTPUT_PATH = "history.csv"

def check_model(ad_strategy, invest_strategy):
    for d in [NAMES, INIT_STATE, RULES]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES]:
        for n in NAMES:
            assert n in d
    assert TOTAL_POP == sum(POP_DISTR)
    assert ad_strategy in SPEND_AD
    assert invest_strategy in SPEND_INVEST
