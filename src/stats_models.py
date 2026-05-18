import pandas as pd
import numpy as np
import scipy.stats as stats

# This module contains functions for calculating statistical models related to stock price data, such as log returns and normality tests.

# Function to calculate log returns from a DataFrame of stock prices
def calculate_log_returns(df: pd.DataFrame) -> pd.Series:

    log_returns = np.log(df['Close'] / df['Close'].shift(1)).dropna()
    return log_returns.squeeze()


# Function to calculate normality test for log returns
def test_normality(log_returns: pd.Series) -> dict:
    data = log_returns.values.flatten()
    shapiro_test = stats.shapiro(data)
    anderson_test = stats.anderson(data, dist='norm')
    jarque_bera_test = stats.jarque_bera(data)
    kolgomorov_smirnov_test = stats.kstest(data, 'norm')

    return {
        'shapiro_statistic': shapiro_test.statistic,
        'shapiro_p_value': shapiro_test.pvalue,
        'anderson_statistic': anderson_test.statistic,
        'anderson_critical_values': anderson_test.critical_values,
        'anderson_significance_level': anderson_test.significance_level,
        'jarque_bera_statistic': jarque_bera_test.statistic,
        'jarque_bera_p_value': jarque_bera_test.pvalue,
        'kolgomorov_smirnov_statistic': kolgomorov_smirnov_test.statistic,
        'kolgomorov_smirnov_p_value': kolgomorov_smirnov_test.pvalue
    }


# Function to fit different distributions to log returns and return the best fit
def fit_distributions(log_returns: pd.Series, distr: str) -> list:
    log_returns = log_returns.dropna()
    data = log_returns.values.flatten()
    if distr == 'norm':
        params = stats.norm.fit(data)
        return list(params)
    elif distr == 'logistic':
        params = stats.logistic.fit(data)
        return list(params)
    elif distr == 'laplace':
        params = stats.laplace.fit(data)
        return list(params)
    elif distr == 't':
        params = stats.t.fit(data)
        return list(params)
    elif distr == 'lognormal':
        params = stats.lognorm.fit(data)
        return list(params)
    elif distr == 'skewnorm':
        params = stats.skewnorm.fit(data)
        return list(params)
    elif distr == 'cauchy':
        params = stats.cauchy.fit(data)
        return list(params)
    elif distr == 'johnsonsu':
        params = stats.johnsonsu.fit(data)
        return list(params)
    elif distr == 'genhyperbolic':
        params = stats.genhyperbolic.fit(data)
        return list(params)
    else:
        raise ValueError("Unsupported distribution type. Please choose from 'normal', 'logistic', 'laplace', 't', 'lognormal', 'skewnorm', 'cauchy', 'johnsonsu', or 'genhyperbolic'.")
    
