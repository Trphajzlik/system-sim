from copy import deepcopy
from public_rules import incl
from rules import ticket_sales, expenses, spend_ad, spend_invest, SPEND_STRATEGIES
from constants import TOTAL_POP, ONE_BUS_CAPACITY, PRICE_ONE_AD, PRICE_ONE_BUS

N_STATES = 12

NAMES = [
    "used", "max_capacity", "budget",
    "ad0", "ad1", "ad2",
    "invest0", "invest1", "invest2", "invest3", "invest4", "invest5"
]

BASE_OPINION = 2/5
INIT_USED = TOTAL_POP * BASE_OPINION

INIT_MAX_CAP = 0.5 * TOTAL_POP
INIT_BUDGET = 50 * 10**6 # 50 mil

INIT_STATE = {
    # How many have used public transport in the last month
    # In `persons`
    "used" : INIT_USED,

    # Max capacity of public transport
    # In `persons`
    "max_capacity" : INIT_MAX_CAP,

    # Budget of the city
    # We allow them to go into debt without any penalty
    # In `currency`
    "budget" : INIT_BUDGET,

    # States handling ads
    # In `currency / PRICE_ONE_AD`
    "ad0" : 0, "ad1" : 0, "ad2" : 0,

    # States handling investments into increasing
    # capacity of public transport
    # In `currency / PRICE_ONE_BUS`
    "invest0" : 0, "invest1" : 0, "invest2" : 0,
    "invest3" : 0, "invest4" : 0, "invest5" : 0
}

def GET_INIT_STATE():
    return deepcopy(INIT_STATE)

# Wrapper and helpincler functions for rules

def sum_curr_ads(state):
    return sum([state[f"ad{i}"] for i in range(3)])

def w_incl(history):
    # In `persons`, returns how many will use this month
    relevant_history = list(map(lambda s: (s["used"], s["max_capacity"], sum_curr_ads(s)), history))
    next_used = incl(relevant_history)
    # Only up to 100% of citizens can travel
    assert next_used >= 0
    assert next_used <= TOTAL_POP
    return next_used

def w_ticket_sales(state):
    # In `currency`
    return ticket_sales(state["used"])

def w_expenses(state):
    # In `currency`
    return expenses(state["max_capacity"])

def w_budget(strategy, history, data):
    # In `currency`
    curr_budget = history[-1]["budget"]
    earn_tickets = w_ticket_sales(history[-1])
    fuel_payed = w_expenses(history[-1])
    spent_on_ads = spend_ad(strategy, history, data)
    spent_on_buying = spend_invest(strategy, history, data)
    return curr_budget + earn_tickets - fuel_payed - spent_on_ads - spent_on_buying

RULES = {
    # Logic if population chooses to use public transport
    "used": (lambda h, d: w_incl(h)),

    # Capacity increases after 6 months after deciding to invest
    "max_capacity" : (lambda h, d: h[-1]["max_capacity"] + ONE_BUS_CAPACITY * h[-1]["invest5"]),

    # Budget changes based on ticket sales, buying fuel,
    # spending on ads, and spending on buying new buses
    "budget" : (lambda h, d: 0/0),

    # Ads are in circulation for 3 months
    "ad0" : (lambda h, d: 0/0),
    "ad1" : (lambda h, d: h[-1]["ad0"]), "ad2" : (lambda h, d: h[-1]["ad1"]),

    # It takes 6 months to buy a bus
    # Spending 5 milion will increase max capacity by 5000
    "invest0" : (lambda h, d: 0/0),
    "invest1" : (lambda h, d: h[-1]["invest0"]), "invest2" : (lambda h, d: h[-1]["invest1"]),
    "invest3" : (lambda h, d: h[-1]["invest2"]), "invest4" : (lambda h, d: h[-1]["invest3"]),
    "invest5" : (lambda h, d: h[-1]["invest4"])
}

def GET_RULES(strategy):
    rules = deepcopy(RULES)
    rules["budget"] = (lambda h, d: w_budget(strategy, h, d))
    rules["ad0"] = (lambda h, d: spend_ad(strategy, h, d) / PRICE_ONE_AD)
    rules["invest0"] = (lambda h, d: spend_invest(strategy, h, d) / PRICE_ONE_BUS)
    return rules

TESTED_STRATEGIES = [
    n for n in SPEND_STRATEGIES
]

STEPS = 240
OUTPUT_PATH = "history.csv"

def check_model(strategy):
    for d in [NAMES, INIT_STATE, RULES]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES]:
        for n in NAMES:
            assert n in d
    assert strategy in SPEND_STRATEGIES
