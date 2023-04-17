from setup import INIT_STATE, RULES, STEPS, OUTPUT_PATH, GRAPH_PATH, N_STATES, COLOURS, DRAW_STATE
from engine import Engine
from post_process import plot_all


def check_model():
    assert N_STATES == len(INIT_STATE)
    assert N_STATES == len(RULES)
    assert N_STATES == len(COLOURS)
    assert N_STATES == len(DRAW_STATE)

def _main():
    check_model()
    engine = Engine(INIT_STATE, RULES)
    engine.simulate(STEPS)
    engine.dump_history(OUTPUT_PATH)
    plot_all(engine.history, DRAW_STATE, COLOURS, GRAPH_PATH)


if __name__ == "__main__":
    _main()