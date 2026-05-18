import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import custom quantitative modules
from src.utils import Date
from src.data_fetcher import fetch_stock_data
from src.stats_models import calculate_log_returns, test_normality, fit_distributions
from src.visualizations import plot_log_returns_histogram, plot_log_returns_qq, plot_log_returns_pp

# Configure the Streamlit page layout
st.set_page_config(page_title="Quantitative Analysis Platform", layout="wide")

st.title("Quantitative Analysis Platform")
st.markdown("---")

# Configuration and User Inputs
st.sidebar.header("Input Parameters")

ticker = st.sidebar.text_input("Company Ticker", value="AAPL")

# Date Pickers (Streamlit returns datetime.date objects)
start_date_input = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date_input = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

interval = st.sidebar.selectbox("Frequency", options=["1d", "1wk"], index=0)

# Dropdown for the distribution selection 
selected_dist = st.sidebar.selectbox(
    "Select Distribution for P-P Plot",
    options=["norm", "t", "laplace", "logistic", "lognorm", "skewnorm", "cauchy", "johnsonsu", "genhyperbolic"],
    index=0
)


run_analysis = st.sidebar.button("Run Analysis")


# Main execution block that runs when the user clicks the "Run Analysis" button
if run_analysis:
    st.header(f"Analysis Dashboard for {ticker.upper()}")
    
    # Convert Streamlit date objects into our custom Date class for compatibility with data fetching functions
    start_date = Date(start_date_input.strftime("%Y-%m-%d"))
    end_date = Date(end_date_input.strftime("%Y-%m-%d"))
    
    # First, download the stock data using the provided ticker and date range. This is the most time-consuming step, so we wrap it in a spinner for better UX.
    with st.spinner("Fetching data from Yahoo Finance..."):
        df = fetch_stock_data(ticker, start_date, end_date, interval)
        
    if df is not None and not df.empty:
        # Display the latest prices in an interactive table
        st.subheader("Historical Data Summary (Latest Rows)")
        st.dataframe(df.tail())
        
        # Compute log returns
        log_returns = calculate_log_returns(df)
        
        # Statistical Testing and Distribution Fitting
        normality_results = test_normality(log_returns)
        
        with st.spinner(f"Fitting {selected_dist} distribution via MLE..."):
            fitted_params = fit_distributions(log_returns, selected_dist)
        
        # Display Metrics in Columns
        st.markdown("---")
        st.subheader("Statistical Diagnostics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Shapiro-Wilk p-value", f"{normality_results['shapiro_p_value']:.4f}")
        with col2:
            st.metric("Jarque-Bera p-value", f"{normality_results['jarque_bera_p_value']:.4f}")
            
        # Display the raw parameters calculated by SciPy for transparency
        st.caption(f"**Fitted Parameters ({selected_dist}):** {fitted_params}")
        
        #  Visualizations Layer
        st.markdown("---")
        st.subheader("Distribution and Probability Charts")
        
        # Create a layout with 3 equal columns 
        chart_col1, chart_col2, chart_col3 = st.columns(3)
        
        with chart_col1:
            st.markdown("#### Histogram & Density")
            plot_log_returns_histogram(log_returns)
            st.pyplot(plt.gcf())  # Grab current matplotlib figure and send to web
            plt.clf()             # Clear figure memory immediately
            
        with chart_col2:
            st.markdown("#### Q-Q Plot")
            plot_log_returns_qq(log_returns, distr='norm') # Standardized normality check
            st.pyplot(plt.gcf())
            plt.clf()
            
        with chart_col3:
            st.markdown(f"#### P-P Plot ({selected_dist.capitalize()})")
            plot_log_returns_pp(log_returns, params=fitted_params, distr=selected_dist)
            st.pyplot(plt.gcf())
            plt.clf()
            
    else:
        st.error(f"Could not retrieve data for ticker '{ticker}'. Please verify the symbol.")