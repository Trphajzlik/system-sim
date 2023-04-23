from setup import INIT_STATE, NAMES, RULES, STEPS, OUTPUT_PATH, GRAPH_PATH, N_STATES, COLOURS, DRAW_STATE
from engine import Engine
from post_process import plot_all


def check_model():
    for d in [NAMES, INIT_STATE, RULES, COLOURS, DRAW_STATE]:
        assert N_STATES == len(d)
    for d in [INIT_STATE, RULES, COLOURS, DRAW_STATE]:
        for n in NAMES:
            assert n in d

def _main():
    check_model()
    engine = Engine(NAMES, INIT_STATE, RULES)
    engine.simulate(STEPS)
    engine.dump_history(OUTPUT_PATH)
    plot_all(engine.history, NAMES, DRAW_STATE, COLOURS, GRAPH_PATH)


if __name__ == "__main__":
    _main()
