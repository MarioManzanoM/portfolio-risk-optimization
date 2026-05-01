import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# This module contains functions for visualizing stock price data, such as plotting histograms of log returns and QQ plots.

# Function to plot histogram of log returns
def plot_log_returns_histogram(log_returns: pd.Series, bins: int = 50) -> None:
    plt.figure(figsize=(10, 6))
    plt.hist(log_returns, bins = bins, density = True, alpha = 0.6, color = 'red')
    plt.title('Histogram of Log Returns')
    plt.xlabel('Log Return')
    plt.ylabel('Density')
    plt.grid()


# Function to plot QQ plot of log returns
def plot_log_returns_qq(log_returns: pd.Series, distr = 'norm') -> None:
    plt.figure(figsize=(10, 6))
    sp.stats.probplot(log_returns, dist = distr, plot = plt)
    plt.title(f"Q-Q Plot - {distr} Distribution")
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Empirical Quantiles")
    plt.grid(True, alpha=0.3)

# Function to plot PP plot of log returns
def plot_log_returns_pp(log_returns: pd.Series, params: list, distr = 'norm') -> None:

    sorted_log_returns = np.sort(log_returns)
    n = len(log_returns)
    empirical_probs = np.arange(1, n+1) / (n+1)

    if distr == 'norm':
        theoretical_probs = sp.stats.norm.cdf(sorted_log_returns, loc = params[0], scale = params[1])
    elif distr == 't':
        theoretical_probs = sp.stats.t.cdf(sorted_log_returns, df = params[0], loc = params[1], scale = params[2])
    elif distr == 'Laplace':
        theoretical_probs = sp.stats.laplace.cdf(sorted_log_returns, loc = params[0], scale = params[1])
    elif distr == 'Logistic':
        theoretical_probs = sp.stats.logistic.cdf(sorted_log_returns, loc = params[0], scale = params[1])
    elif distr == 'Hyperbolic':
       raise NotImplementedError("Hyperbolic distribution is not implemented in scipy.stats")
    else:
        raise ValueError("Unsupported distribution type")
        
    plt.figure(figsize=(10, 6))
    plt.scatter(theoretical_probs, empirical_probs, color='blue', alpha=0.5, label='log_returns')

    plt.plot([0, 1], [0, 1], color='red', lw=2, label='Referencia')
    
    plt.title(f"P-P Plot - {distr} Distribution")
    plt.xlabel("Theoretical Probabilities")
    plt.ylabel("Empirical Probabilities")
    plt.legend()
    plt.grid(True, alpha=0.3)


