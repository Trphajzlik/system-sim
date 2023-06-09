import matplotlib.pyplot as plt

def plot_all(history, graph_names, graph_entry_names, transforms, colours, prefix, graph_paths):
    for gname in graph_names:
        plot_one(map(transforms[gname], history), graph_entry_names[gname], colours[gname], gname, prefix + graph_paths[gname])

def plot_one(it_history, entry_names, colours, plot_name, output):
    fig = plt.figure(figsize=(12.8, 9.6))
    fig.clear()
    xpoints = []
    ypoints = {name : [] for name in entry_names}
    for i, val in enumerate(it_history):
        xpoints.append(i)
        for name in entry_names:
            ypoints[name].append(val[name])
    for name in entry_names:
        plt.plot(xpoints, ypoints[name], colours[name], label=name, markersize=1, linewidth=1)
    plt.title(plot_name)
    plt.grid(linestyle=':')
    leg = plt.legend(loc='lower right', shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig(output)
    plt.close()


def plot_comparison(histories, graph_names, transforms, colours, odir, graph_paths):
    for gname in graph_names:
        plot_c_one(histories, transforms[gname], colours[gname], gname, odir + graph_paths[gname])

def plot_c_one(histories, transform, colours, plot_name, output):
    fig = plt.figure(figsize=(12.8, 9.6))
    fig.clear()
    xpoints = []
    ypoints = {name : [] for name in colours}
    ny = None
    for l, history in histories.items():
        if ny is None:
            ny = len(history)
        else:
            assert ny == len(history)

    for i in range(ny):
        xpoints.append(i)
        for name in colours:
            ypoints[name].append(transform(histories[name][i]))
    for name in colours:
        plt.plot(xpoints, ypoints[name], colours[name], label=name, markersize=1, linewidth=1)
    plt.title(plot_name)
    plt.grid(linestyle=':')
    leg = plt.legend(loc='lower right', shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig(output)