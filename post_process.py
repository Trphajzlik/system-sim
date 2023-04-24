import matplotlib.pyplot as plt

def plot_all(history, graph_names, graph_entry_names, transforms, colours, graph_paths):
    for gname in graph_names:
        plot_one(map(transforms[gname], history), graph_entry_names[gname], colours[gname], gname, graph_paths[gname])

def plot_one(t_history, entry_names, colours, plot_name, output):
    fig = plt.figure()
    fig.clear()
    xpoints = []
    ypoints = {name : [] for name in entry_names}
    for i, val in enumerate(t_history):
        xpoints.append(i)
        for name in entry_names:
            ypoints[name].append(val[name])
    for name in entry_names:
        plt.plot(xpoints, ypoints[name], colours[name], label=name)
    plt.title(plot_name)
    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig(output)
