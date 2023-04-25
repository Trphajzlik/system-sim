from copy import deepcopy

from setup import check_model, TESTED_STRATEGIES, GET_INIT_STATE, NAMES, GET_RULES, STEPS, OUTPUT_PATH, N_STATES
from postprocess_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES
from comp_pp_setup import check_c_pp_setup, C_GRAPH_NAMES, C_TRANSFORM, C_COLOURS, C_GRAPH_PATHS

#from simple_setup import check_model, INIT_STATE, NAMES, RULES, STEPS, OUTPUT_PATH, N_STATES
#from simple_pp_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES

from engine import Engine
from post_process import plot_all, plot_comparison

OUTPUT_DIR = "data/"

def _main():
    histories = dict()
    check_postprocess_setup()
    check_c_pp_setup(TESTED_STRATEGIES)

    for strategy in TESTED_STRATEGIES:
        check_model(strategy)

        engine = Engine(NAMES, GET_INIT_STATE(), GET_RULES(strategy))
        engine.simulate(STEPS)

        prefix = f"{strategy}-"
        engine.dump_history(OUTPUT_DIR + prefix + OUTPUT_PATH)
        plot_all(engine.history, GRAPH_NAMES, GRAPH_ENTRY_NAMES, TRANSFORM, COLOURS, OUTPUT_DIR + prefix, GRAPH_PATHS)
        histories[strategy] = deepcopy(engine.history)
    plot_comparison(histories, C_GRAPH_NAMES, TESTED_STRATEGIES, C_TRANSFORM, C_COLOURS, OUTPUT_DIR, C_GRAPH_PATHS)

if __name__ == "__main__":
    _main()
