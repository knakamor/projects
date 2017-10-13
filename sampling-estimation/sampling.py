import pandas as pd
import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt
import seaborn as sns


def plot_hist_basic(df, col):
    """
    Plot a histogram from the column col of dataframe df. Return a Matplotlib
    axis object.

    INPUT:
    df: (Pandas DataFrame)
    col: (str) Column from df with numeric data to be plotted

    OUTPUT:
    ax: (Matplotlib axis object) 
    """
    data = df[col]
    ax = data.hist(bins=20, normed=1, edgecolor='none', figsize=(10,7))
    ax.set_ylabel('Probability Density')
    ax.set_title(col)

    return ax

def get_sample_mean_var(df, col):
    """
    Calculate sample mean and sample variance of a 1-d array (or Series)
    INPUT:
    df: (Pandas DataFrame)
    col: (str) Column from df with numeric data to be plotted
    OUTPUT:
    sample mean (float), sample variance (float)
    """
    # by default np.var returns population variance.
    # ddof=1 to get sample var (ddof: delta degrees of freedom)
    data = df[col]
    return data.mean(), data.var(ddof=1)

def plot_mom(df, col,  ax=None, gamma=True, normal=True):
    """
    Use Method of Moments to fit Normal and/or Gamma Distributions to the data
    in df[col] and plot their PDFs against a histogram of the data.
    
    INPUT:
    df: (Pandas DataFrame)
    col: (str) Column from df with numeric data to be plotted
    ax = (Matplotlib axis object) Optional. Used for creating multiple subplots
    gamma = (bool) Fit and plot a Gamma Distribution
    normal = (bool) Fit and plot a Normal Distribution

    OUTPUT:
    ax: (Matplotlib axis object) 
    """
    if ax is None:
        ax = plot_hist_basic(df, col)
    samp_mean, samp_var = get_sample_mean_var(df, col)
    data = df[col]
    x_vals = np.linspace(data.min(), data.max())
    
    if gamma:
        alpha = samp_mean**2 / samp_var
        beta = samp_mean / samp_var
        gamma_rv = scs.gamma(a=alpha, scale=1/beta)
        gamma_p = gamma_rv.pdf(x_vals)
        ax.plot(x_vals, gamma_p, color='r', label='Gamma MOM', alpha=0.6)

    if normal:
        # scipy's scale parameter is standard dev.
        samp_std = samp_var**0.5
        normal_rv = scs.norm(loc=samp_mean, scale=samp_std)
        normal_p = normal_rv.pdf(x_vals)
        ax.plot(x_vals, normal_p, color='g', label='Normal MOM', alpha=0.6)

   
    ax.set_ylabel('Probability Density')
    # uniform axes for rainfall data
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 0.35)
    ax.legend()

    return ax

def plot_mle(df, col, ax=None, gamma=True, normal=True):
    """
    Use Maximum Likelihood Estimation to fit Normal and/or Gamma Distributions
    to the data in df[col] and plot their PDFs against a histogram of the data.
    INPUT:
    df: (Pandas DataFrame)
    col: (str) Column from df with numeric data to be plotted
    ax = (Matplotlib axis object) optional. Used for creating multiple subplots
    gamma = (bool) Fit and plot a Gamma Distribution
    normal = (bool) Fit and plot a Normal Distribution

    OUTPUT:
    ax: (Matplotlib axis object) 
    """

    data = df[col]
    x_vals = np.linspace(data.min(), data.max())

    if ax is None:
        ax = plot_hist_basic(df, col)

    if gamma:
        ahat, loc, bhat = scs.gamma.fit(data, floc=0)
        gamma_rv = scs.gamma(a=ahat, loc=loc, scale=bhat)
        gamma_p = gamma_rv.pdf(x_vals)
        ax.plot(x_vals, gamma_p, color='k', alpha=0.7, label='Gamma MLE')
    
    if normal:
        mean_mle, std_mle = scs.norm.fit(data)
        normal_rv = scs.norm(loc=mean_mle, scale=std_mle)
        normal_p = normal_rv.pdf(x_vals)
        ax.plot(x_vals, normal_p, color='g', label='Normal MLE', alpha=0.6)

    ax.set_ylabel('Probability Density')
    # uniform axes for rainfall data
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 0.35)
    ax.legend()

    return ax


def plot_year(df, cols, plot_funcs, gamma=True, normal=True):
    """
    Loop over 12 columns of data and plot fits to each column, using 
    plot_mom or plot_mle.


    INPUT:
    df: (Pandas DataFrame)
    cols: (list of str) Columns from df with numeric data to be plotted
    plot_funcs: (list of functions) plot_mom or plot_mle
    gamma = (bool) Fit and plot a Gamma Distribution
    normal = (bool) Fit and plot a Normal Distribution

    OUTPUT:
    ax: (Matplotlib axis object) 
    """
    # assuming we are plotting a 3x4 grid, so check
    if len(cols) != 12:
        ex_str = 'Expecting 12 monthly columns, got: {}'.format(len(cols))
        raise Exception(ex_str)

    # Pandas does a lexicographic sort on the column names when plotting
    # multiple histograms (with no obvious way to turn that off).
    # So to ensure consistency between the histograms and the fits,
    # use the sorted version of the columns here and in plotting the fits.
    cols_srt = sorted(cols)
    axes = df[cols_srt].hist(bins=20, normed=1,
                    grid=0, edgecolor='none',
                    figsize=(15, 10),
                    layout=(3,4))


    for month, ax in zip(cols_srt, axes.flatten()):
        for func in plot_funcs:
            func(df, month, ax=ax, gamma=gamma, normal=normal)
    plt.tight_layout()

    return ax


def poisson_likelihood(lam, ks):
    """
    Return the likelihood of observing an array different counts ks for a
    Poisson distribution with rate parameter lam.
    """
    return scs.poisson(lam).pmf(ks)

def poisson_mle(data, lambda_range):
    """
    Calculate the maximum likelihood and plot likelihoods for a Poisson 
    distribution with rate parameters in the array lambda_range, given 
    observations in the array data.

    INPUT:
    data: (Numpy array) discrete count data.
    lambda_range: (Numpy array) different lambda values to check. 
                        possibly created using np.linspace.

    OUTPUT:
    (float) the lambda value corresponding to the Maximum Likelihood of the data
    """

    sum_logs = []
    for lam in lambda_range:
        likes = poisson_likelihood(lam, data)
        sum_log_liklihood = np.sum(np.log10(likes))
        sum_logs.append(sum_log_liklihood)

    fig = plt.figure(figsize=(7,6))
    plt.plot(lambda_range, sum_logs)
    plt.ylabel('$log(L(x | \lambda))$', fontsize=14)
    plt.xlabel('$\lambda$', fontsize=14)
    
    maxlik_ind = np.argmax(sum_logs)
    return lambda_range[maxlik_ind]


def plot_kde(df, col):
    """
    Fit a Gaussian Kernal Density Estimate to some input data, plot the fit
    over a histogram of the data.
    INPUT:
    df: (Pandas DataFrame)
    col: (str) Column from df with numeric data to be plotted

    OUTPUT:
    ax: (Matplotlib axis object) 
    """
    ax = plot_hist_basic(df, col)
    data = df[col]
    density = scs.kde.gaussian_kde(data)
    x_vals = np.linspace(data.min(), data.max(), 100)
    kde_vals = density(x_vals)
    
    ax.plot(x_vals, kde_vals, 'r-')
    
    return ax
