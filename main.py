from setup import check_model, INIT_STATE, NAMES, RULES, STEPS, OUTPUT_PATH, N_STATES
from postprocess_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES

#from simple_setup import check_model, INIT_STATE, NAMES, RULES, STEPS, OUTPUT_PATH, N_STATES
#from simple_pp_setup import check_postprocess_setup, TRANSFORM, COLOURS, GRAPH_PATHS, GRAPH_NAMES, GRAPH_ENTRY_NAMES

from engine import Engine
from post_process import plot_all

def _main():
    check_model()
    check_postprocess_setup()
    engine = Engine(NAMES, INIT_STATE, RULES)
    engine.simulate(STEPS)
    engine.dump_history(OUTPUT_PATH)
    plot_all(engine.history, GRAPH_NAMES, GRAPH_ENTRY_NAMES, TRANSFORM, COLOURS, GRAPH_PATHS)

if __name__ == "__main__":
    _main()
