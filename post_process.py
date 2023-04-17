import matplotlib.pyplot as plt

def plot_all(history, draw_state, colours, output):
    if len(history) == 0:
        return
    n_states = len(history[0])
    for n in range(n_states):
        if not draw_state[n]:
            continue
        xpoints = []
        ypoints = []
        for i in range(len(history)):
            xpoints.append(i)
            ypoints.append(history[i][n])
        plt.plot(xpoints, ypoints, colours[n])
    plt.savefig(output)