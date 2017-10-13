

from numpy import ndarray
from scipy.spatial.distance import cdist, pdist
from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-paper')

from matplotlib import animation

from JSAnimation import IPython_display


def initialize_centroids(X, k=10):
    """initializtion of k centroids
    return np array of centroids
    """

    centroids = X.copy()
    np.random.shuffle(centroids)
    return centroids[:k]


def closest_centroid(X, centroids):
    """returns an array containing the index to the nearest centroid for each point"""
    distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)


def move_centroids(X, closest, centroids):
    """returns the new centroids assigned from the points closest to them"""
    return np.array([X[closest==k].mean(axis=0) for k in range(centroids.shape[0])])


def elbow(plot_path, variance_inflation, max_k=10):
    def wcss(labels):
        return sum(np.sum(pdist(X[labels == label]))
                   for label in np.unique(labels))

    X = make_small_clusters(variance_inflation)
    ks = np.arange(max_k)
    wcss_arr = np.empty(max_k)
    for k in ks:
        kmeans = KMeans(n_clusters=k+1, max_iter=100).fit(X)
        wcss_arr[k] = wcss(kmeans.labels_)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].plot(ks, wcss_arr)
    axs[0].set_xlabel('$k$', fontsize=15)
    axs[0].set_title('WCSS', fontsize=20)
    axs[1].scatter(X[:, 0], X[:, 1])
    axs[1].set_xticklabels([])
    axs[1].set_yticklabels([])
    axs[1].set_title('How Many Clusters?', fontsize=20)
    plt.savefig(plot_path)

if __name__ == '__main__':
    #make_small_clusters(plot=True)

    fig = plt.figure()
    ax = plt.axes(xlim=(-4, 4), ylim=(-4, 4))

    iris = datasets.load_iris()
    X = iris.data[:, 0:2]
    centroids = initialize_centroids(X, 10)

    def init():
        return

    def animate(i):
        global centroids
        closest = closest_centroid(X, centroids)
        centroids = move_centroids(closest, centroids)
        ax.cla()
        ax.scatter(X[:, 0], X[:, 1], c=closest)
        ax.scatter(centroids[:, 0], centroids[:, 1], c='r', s=100)
        return animation.FuncAnimation(fig, animate, init_func=init,
                        frames=10, interval=200, blit=True)



    #plot_k_means_steps(X, k=3, base_plot_path='images/kmeans')
    #plot_initializations(X, k=3)
    #plot_elbow('images/elbow_method.png', variance_inflation=-0.05)
    #plot_elbow('images/elbow_method_bad.png', variance_inflation=0.5)
