import matplotlib.pyplot as plt

# plots data on a graph
def plot_data(arr, heading="_"):
    plt.style.use('dark_background')
    plt.scatter(
        arr[:, 0],
        arr[:, 1],
        )
    plt.title(heading, fontsize=24)
    plt.show()


# plots data using cluster labels for point colors
def plot_labeled_data(arr, labels, heading=""):
    plt.style.use('dark_background')
    plt.scatter(
        arr[:, 0],
        arr[:, 1],
        c=labels
    )
    plt.title(heading, fontsize=24)
    plt.show()