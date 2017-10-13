import scipy.stats as scs
import numpy as np
import matplotlib.pyplot as plt


def make_draws(dist, params, size=200):
    """
    Draw samples of random variables from a specified distribution, with given 
    parameters return these in an array.

    INPUT:
    dist: (Scipy.stats distribution object) Distribution with a .rvs method
    params: (dict) Parameters to define the distribution dist.
                e.g. if dist = scipy.stats.binom then params could be:
                {'n': 100, 'p': 0.25}

    OUTPUT:
    (Numpy array) Sample of random variables 
    """
    return dist(**params).rvs(size)


def plot_means(dist, params, size=200, repeats=5000):
    """
    Draw samples of specified size from a Scipy.stats distribution and calculate 
    the sample mean.  Repeat this a specified number of times to build out a
    sampling distribution of the sample mean.  Plot the results.
    
    INPUT:
    dist: (Scipy.stats distribution object) 
                Accepts: scipy.stats:   .uniform,
                                        .poisson,
                                        .binom,
                                        .expon,
                                        .geom
        
    params: (dict) Parameters to define the distribution dist.
                e.g. if dist = scipy.stats.binom then params could be:
                {'n': 100, 'p': 0.25}
    size: (int) Number of examples to draw.
    repeats: (int) Number of sample means to calculate.
    """
    
    dist_instance = dist(**params)
    
    mean_vals = []
    for _ in xrange(repeats):
        values = dist_instance.rvs(size)
        mean_vals.append(np.mean(values))
        
    d_label = {scs.uniform: ['Uniform', 'Mean of randomly drawn values from a uniform'],
            scs.poisson: ['Poisson', 'Mean events happening in an interval'],
            scs.binom: ['Binomial', 'Mean number of successes'],
            scs.expon: ['Exponential', 'Mean of waiting time before an event'],
            scs.geom: ['Geometric', 'Mean trials until first success']
           }
    
    dist_name = d_label[dist][0]
    xlabel = d_label[dist][1]
    title_str = 'Mean of {0} samples with size {1} drawn from {2} distribution'
    
    plt.hist(mean_vals, bins=30)
    plt.xlabel(xlabel)
    plt.ylabel('Counts')
    plt.title(title_str.format(repeats, size, dist_name), fontsize=14)
    plt.show()

## In practice we should work to generalize our plot_means func rather than 
## create a new function. We will ignore that core programming principle here, 
## for the sake of readability of plot_means.
def plot_maxs(dist, params, size=200, repeats=5000):
    """
    See plot_means.  Substituting np.max for np.mean.
    """
    
    dist_instance = dist(**params)
    
    mean_vals = []
    for _ in xrange(repeats):
        values = dist_instance.rvs(size)
        mean_vals.append(np.max(values)) #SWITCHED HERE
        
    d_label = {scs.uniform: 'Uniform',
            scs.poisson: 'Poisson',
            scs.binom: 'Binomial', 
            scs.expon: 'Exponential', 
            scs.geom: 'Geometric'
           }
    
    dist_name = d_label[dist]
    title_str = 'Max of {0} samples with size {1} drawn from {2} distribution'
    
    plt.hist(mean_vals, bins=30)
    plt.xlabel(dist_name)
    plt.ylabel('Counts')
    plt.title(title_str.format(repeats, size, dist_name), fontsize=14)
    plt.show()


def sample_sd(arr):
    """
    Sample Standard Deviation.  
    ddof=1 means Delta Degrees of Freedom, changes denom. to N-1.
    """
    return np.std(arr, ddof=1)


def standard_error(arr):
    return sample_sd(arr) / np.sqrt(len(arr))


def bootstrap(arr, iterations=10000):
    """
    Create a series of bootstrapped samples of an input array.
    INPUT:
    arr: (Numpy array) 1-d numeric data
    iterations: (int) number of bootstrapped samples to create.
    
    OUTPUT:
    boot_samples: (list of arrays) A list of length iterations,
                    each element is an array of size of input arr
    """
    if type(arr) != np.ndarray:
        arr = np.array(arr)

    if len(arr.shape) < 2:
        arr = arr[:, np.newaxis]

    nrows = arr.shape[0]
    boot_samples = []
    for _ in xrange(iterations):
        row_inds = np.random.randint(nrows, size=nrows)
        boot_sample = arr[row_inds, :]
        boot_samples.append(boot_sample)
    return boot_samples


def bootstrap_ci(sample, stat_function=np.mean, iterations=1000, ci=95):
    """
    Calculate the confidence interval of a chosen sample statistic using 
    bootstrap sampling.
    
    INPUT:
    sample: (Numpy array) 1-d numeric data
    stat_function: (Func) Function for calculating as sample statistic on data
    iterations: (int) Number of bootstrap samples to create
    ci: (int) Percent of distribution encompassed by CI, 0<ci<100
    
    OUTPUT:
    lower_ci, upper_ci: (float, float) lower and upper bounds of CI
    bootstrap_samples_statistic: (Numpy array) sample stat from each bootstrap sample
    """
    boostrap_samples = bootstrap(sample, iterations=iterations)
    bootstrap_samples_stat = map(stat_function, boostrap_samples)
    low_bound = (100 - ci) / 2
    high_bound = 100 - low_bound
    lower_ci, upper_ci = np.percentile(bootstrap_samples_stat, [low_bound, high_bound])
    return lower_ci, upper_ci, bootstrap_samples_stat


def pearson_correlation(arr, p_val=False):
    """
    Calculate the Pearson Correlation in a two-dimensional data set.
    Optionally return a P-value of the significance of the correlation.
    
    INPUT:
    arr: (Numpy array) Numeric array of size N x 2 
    p_val: (bool) Return P-value if True
    
    OUTPUT:
    corr_coeff: (float) The Pearson Correlation Coefficient
    p_val: (float) Optional. 
    """
    col1 = arr[:, 0]
    col2 = arr[:, 1]
    corr_coeff, pval = scs.stats.pearsonr(col1, col2)
    if not p_val:
        return corr_coeff
    else:
        return corr_coeff, pval




