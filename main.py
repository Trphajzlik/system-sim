from copy import deepcopy

from setup import check_model, TESTED_STRATEGIES, GET_INIT_STATE, NAMES, GET_RULES, STEPS, OUTPUT_PATH, N_STATES
from postprocess_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES
from comp_pp_setup import check_c_pp_setup, get_name, C_GRAPH_NAMES, C_TRANSFORM, C_COLOURS, C_GRAPH_PATHS

#from simple_setup import check_model, INIT_STATE, NAMES, RULES, STEPS, OUTPUT_PATH, N_STATES
#from simple_pp_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES

from engine import Engine
from post_process import plot_all, plot_comparison

def _main():
    histories = dict()
    check_postprocess_setup()
    check_c_pp_setup(TESTED_STRATEGIES)

    for ad, spend in TESTED_STRATEGIES:
        check_model(ad, spend)

        engine = Engine(NAMES, GET_INIT_STATE(), GET_RULES(ad, spend))
        engine.simulate(STEPS)

        prefix = f"{ad}|{spend}-"
        engine.dump_history(prefix + OUTPUT_PATH)
        plot_all(engine.history, GRAPH_NAMES, GRAPH_ENTRY_NAMES, TRANSFORM, COLOURS, prefix, GRAPH_PATHS)
        histories[get_name((ad, spend))] = deepcopy(engine.history)
    plot_comparison(histories, C_GRAPH_NAMES, list(map(get_name, TESTED_STRATEGIES)), C_TRANSFORM, C_COLOURS, C_GRAPH_PATHS)

if __name__ == "__main__":
    _main()
