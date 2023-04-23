from rules import incl, ticket_sales, expenses, spend_ad, spend_invest, SPEND_AD, SPEND_INVEST

N_STATES = 16

NAMES = [
    "used0", "used1", "used2", "used3", "used4",
    "max_capacity", "budget",
    "ad0", "ad1", "ad2",
    "invest0", "invest1", "invest2", "invest3", "invest4", "invest5"
]

PERC_DISTR = [0.275, 0.25, 0.225, 0.15, 0.1]
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

# Choose investments strategy
AD_STRATEGY = "basic"
INVEST_STRATEGY = "basic"


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
    ads = [state[f"ad{i}"] for i in range(3)]
    next_used = incl(NAT_INCL[c], POP_DISTR[c], state[f"used{c}"], total_used(state), state["max_capacity"], ads)
    # Only up to 100% of a class can travel
    assert next_used <= POP_DISTR[c]
    return next_used

def w_spend_ad(state):
    return spend_ad(AD_STRATEGY, total_used(state), state["max_capacity"], state["budget"])

def w_spend_invest(state):
    return spend_invest(INVEST_STRATEGY, total_used(state), state["max_capacity"], state["budget"])

RULES = {
    # Logic if population chooses to use public transport
    "used0": (lambda s: w_incl(0, s)), "used1": (lambda s: w_incl(1, s)),
    "used2": (lambda s: w_incl(2, s)), "used3": (lambda s: w_incl(3, s)),
    "used4": (lambda s: w_incl(4, s)),

    # Capacity increases after 6 months after deciding to invest
    "max_capacity" : (lambda s: s["max_capacity"] + s["invest5"]),

    # Budget changes based on ticket sales, buying fuel,
    # spending on ads, and spending on buying new buses
    "budget" : (lambda s: s["budget"] + w_ticket_sales(s) - w_expenses(s) - w_spend_ad(s) - w_spend_invest(s)),

    # Ads are in circulation for 3 months
    "ad0" : (lambda s: w_spend_ad(s)),
    "ad1" : (lambda s: s["ad1"]), "ad2" : (lambda s: s["ad1"]),

    # It takes 6 months to buy a bus
    # Spending 5 milion will increase max capacity by 5000
    "invest0" : (lambda s: 0.01 * w_spend_invest(s)),
    "invest1" : (lambda s: s["invest0"]), "invest2" : (lambda s: s["invest1"]),
    "invest3" : (lambda s: s["invest2"]), "invest4" : (lambda s: s["invest3"]),
    "invest5" : (lambda s: s["invest4"])
}

STEPS = 120
OUTPUT_PATH = "history.csv"

COLOURS = {
    "used0": 'r', "used1": 'r', "used2": 'r',
    "used3": 'r', "used4": 'r',
    "max_capacity" : 'r', "budget" : 'r',
    "ad0" : 'r', "ad1" : 'r', "ad2" : 'r',
    "invest0" : 'r', "invest1" : 'r', "invest2" : 'r',
    "invest3" : 'r', "invest4" : 'r', "invest5" : 'r'
}

GRAPH_PATH = "graph.png"
# TODO: Add multiple draw_states so we can generate multiple graphs
#       Also maybe split this into two files,
#       second setup for postprocessing
DRAW_STATE = {
    "used0": True, "used1": True, "used2": True,
    "used3": True, "used4": True,
    "max_capacity" : True, "budget" : True,
    "ad0" : True, "ad1" : True, "ad2" : True,
    "invest0" : True, "invest1" : True, "invest2" : True,
    "invest3" : True, "invest4" : True, "invest5" : True
}

def check_model():
    i = 0
    for d in [NAMES, INIT_STATE, RULES, COLOURS, DRAW_STATE]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES, COLOURS, DRAW_STATE]:
        for n in NAMES:
            assert n in d
    assert TOTAL_POP == sum(POP_DISTR)
    assert AD_STRATEGY in SPEND_AD
    assert INVEST_STRATEGY in SPEND_INVEST
