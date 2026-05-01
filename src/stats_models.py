import pandas as pd
import numpy as np
import scipy.stats as stats

# This module contains functions for calculating statistical models related to stock price data, such as log returns and normality tests.

# Function to calculate log returns from a DataFrame of stock prices
def calculate_log_returns(df: pd.DataFrame) -> pd.Series:

    log_returns = np.log(df['Close'] / df['Close'].shift(1)).dropna()
    return log_returns


# Function to calculate normality test for log returns
def test_normality(log_returns: pd.Series) -> dict:
    shapiro_test = stats.shapiro(log_returns)
    anderson_test = stats.anderson(log_returns, dist='norm')
    jarque_bera_test = stats.jarque_bera(log_returns)
    kolgomorov_smirnov_test = stats.kstest(log_returns, 'norm')

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