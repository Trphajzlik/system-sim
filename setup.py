from copy import deepcopy
from rules import incl, ticket_sales, expenses, spend_ad, spend_invest, SPEND_AD, SPEND_INVEST

N_STATES = 12

NAMES = [
    "used", "max_capacity", "budget",
    "ad0", "ad1", "ad2",
    "invest0", "invest1", "invest2", "invest3", "invest4", "invest5"
]

TOTAL_POP = 500000.0


BASE_OPINION = 2/5
INIT_USED = TOTAL_POP * BASE_OPINION

INIT_MAX_CAP = 0.5 * TOTAL_POP
INIT_BUDGET = 50 * 10**6 # 50 mil

INIT_STATE = {
    # How many have used public transport in the last month
    "used" : INIT_USED,

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

def w_ticket_sales(state):
    return ticket_sales(state["used"])

def w_expenses(state):
    return expenses(state["max_capacity"])

def w_incl(history):
    ads = sum([history[-1][f"ad{i}"] for i in range(3)])
    relevant_history = list(map(lambda s: (s["used"], s["max_capacity"]), history))
    next_used = incl(TOTAL_POP, relevant_history, ads)
    # Only up to 100% of citizens can travel
    assert next_used <= TOTAL_POP
    return next_used

def w_spend_ad(ad_strategy, history):
    return spend_ad(ad_strategy, history)

def w_spend_invest(invest_strategy, history):
    return spend_invest(invest_strategy, history)

RULES = {
    # Logic if population chooses to use public transport
    "used": w_incl,

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

TESTED_STRATEGIES = [("basic","basic"), ("constant", "constant"), ("try_ad", "try_ad")]

STEPS = 120
OUTPUT_PATH = "history.csv"

def check_model(ad_strategy, invest_strategy):
    for d in [NAMES, INIT_STATE, RULES]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES]:
        for n in NAMES:
            assert n in d
    assert ad_strategy in SPEND_AD
    assert invest_strategy in SPEND_INVEST
