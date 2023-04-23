import matplotlib.pyplot as plt

def plot_all(history, names, draw_state, colours, output):
    if len(history) == 0:
        return
    n_states = len(history[0])
    for n in names:
        if not draw_state[n]:
            continue
        xpoints = []
        ypoints = []
        for i in range(len(history)):
            xpoints.append(i)
            ypoints.append(history[i][n])
        plt.plot(xpoints, ypoints, colours[n], label=n)
    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig(output)
