import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu
import matplotlib.dates as mdates
import os
import sys 
import calmap

# --- Part 1: Data Loading and Preparation ---
def load_and_prepare_real_data(filepath='data/city_day.csv'):
    """
    Main data prep function. Loads the CSV, filters for Delhi, cleans,
    and adds the 'policy_status' column needed for the analysis.
    """
    print(f"Loading data from '{filepath}'...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        # Standard error handling if the data file is missing.
        print(f"\n[ERROR] Data file not found at '{filepath}'.")
        print("Please ensure 'city_day.csv' is inside a 'data' subfolder.")
        sys.exit() 
        
    # --- Data Cleaning ---
    df_delhi = df[df['City'] == 'Delhi'].copy()
    print(f"Found {len(df_delhi):,} rows for Delhi.")
    
    # Set Date as a proper datetime index for time-series operations.
    df_delhi['Date'] = pd.to_datetime(df_delhi['Date'])
    df_delhi.set_index('Date', inplace=True)
    
    # Simplify column names for easier access.
    df_delhi.rename(columns={'PM2.5': 'pm25', 'NO2': 'no2'}, inplace=True)
    
    # Forward-fill missing values - a reasonable assumption for daily data.
    df_delhi['pm25'].ffill(inplace=True)
    df_delhi['no2'].ffill(inplace=True)
    
    # Drop any rows that still have NaNs (likely at the start).
    df_delhi.dropna(inplace=True)
    
    # --- Feature Engineering ---
    # This function creates the categories we'll use to compare periods.
    policy_periods = {
        'Phase 1': {'start': '2016-01-01', 'end': '2016-01-15'},
        'Phase 2': {'start': '2016-04-15', 'end': '2016-04-30'},
        'Phase 3': {'start': '2017-11-13', 'end': '2017-11-17'},
        'Phase 4': {'start': '2019-11-04', 'end': '2019-11-15'}
    }
    
    def get_policy_status(date):
        for phase, dates in policy_periods.items():
            start = pd.to_datetime(dates['start'])
            end = pd.to_datetime(dates['end'])
            delta = end - start
            
            if start <= date <= end:
                return f'During {phase}'
            # 'Before' period is same duration as the policy, right before it.
            if (start - delta - pd.Timedelta(days=1)) <= date < start:
                return f'Before {phase}'
            # 'Control' period is the same date range, but from the previous year.
            if (start - pd.DateOffset(years=1)) <= date <= (end - pd.DateOffset(years=1)):
                return f'Control {phase}'
        return 'Normal Day'

    df_delhi['policy_status'] = df_delhi.index.to_series().apply(get_policy_status)
    
    print("Data preparation complete.")
    return df_delhi

# --- Part 2: Statistical Analysis ---
def perform_statistical_analysis(df, phase='Phase 1'):
    """
    Runs a Mann-Whitney U test to see if the difference between the
    'During' and 'Control' periods is statistically significant.
    """
    print(f"\n--- Statistical Analysis for {phase} ---")
    
    during_data = df[df['policy_status'] == f'During {phase}']['pm25']
    control_data = df[df['policy_status'] == f'Control {phase}']['pm25']
    
    if during_data.empty or control_data.empty:
        print("Not enough data for a meaningful statistical test.")
        return

    # One-sided test: we're checking if pollution was specifically *lower* during the policy.
    stat, p_value = mannwhitneyu(during_data, control_data, alternative='less')
    
    print(f"Comparing '{phase}' vs. Control Period for PM2.5:")
    print(f"  - Mean PM2.5 During Policy: {during_data.mean():.2f}")
    print(f"  - Mean PM2.5 Control Period: {control_data.mean():.2f}")
    print(f"  - Mann-Whitney U test p-value: {p_value:.4f}")
    
    # A p-value below 0.05 is the standard threshold for statistical significance.
    if p_value < 0.05:
        print("  - Result: The reduction in PM2.5 is statistically significant.")
    else:
        print("  - Result: The reduction in PM2.5 is NOT statistically significant.")

# --- Part 3: High-Impact Data Visualization ---
def create_visualizations(df, phase='Phase 1'):
    """Generates presentation-quality visuals to tell the story of the findings."""
    print("\n--- Generating Visualizations (close each plot to see the next) ---")
    
    # Prep a smaller dataframe for the comparison plots.
    comp_df = df[df['policy_status'].isin([f'During {phase}', f'Control {phase}'])].copy()
    comp_df['period'] = comp_df['policy_status'].apply(lambda x: 'During Policy' if 'During' in x else 'Control (Prior Year)')
    
    # --- Viz 1: The Main Result Bar Chart ---
    plt.style.use('seaborn-v0_8-talk')
    fig1, ax1 = plt.subplots(figsize=(10, 7))
    
    mean_data = comp_df.groupby('period')[['pm25']].mean().reset_index()
    
    # Calculate the percentage change for the annotation.
    control_pm25 = mean_data.loc[mean_data['period'] == 'Control (Prior Year)', 'pm25'].iloc[0]
    during_pm25 = mean_data.loc[mean_data['period'] == 'During Policy', 'pm25'].iloc[0]
    pct_change = ((during_pm25 - control_pm25) / control_pm25) * 100
    
    sns.barplot(data=mean_data, x='period', y='pm25', palette=['#ff9999', '#66b3ff'], ax=ax1)
    
    ax1.set_title(f'Impact of Odd-Even {phase} on Average PM2.5', fontsize=20, pad=20, weight='bold')
    ax1.set_ylabel('Average PM2.5 Concentration (µg/m³)', fontsize=14)
    ax1.set_xlabel('')
    
    # Add clear data labels on top of the bars.
    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():.1f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', fontsize=14, color='black', xytext=(0, 10),
                     textcoords='offset points')
    
    # Add a prominent annotation showing the percentage change.
    ax1.text(0.5, 0.5, f'{pct_change:+.1f}% Change',
             ha='center', va='center', transform=ax1.transAxes, fontsize=22, color='white',
             weight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="black", alpha=0.8))
    
    plt.tight_layout()
    plt.show()

    # --- Viz 2: Distribution Deep Dive (Violin Plot) ---
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    
    sns.violinplot(data=comp_df, x='period', y='pm25', ax=ax2, inner='quartile', palette=['#ff9999', '#66b3ff'])
    sns.stripplot(data=comp_df, x='period', y='pm25', ax=ax2, color='black', alpha=0.3, jitter=0.1)
    
    ax2.set_title(f'PM2.5 Distribution: Policy vs. Control ({phase})', fontsize=20, pad=20, weight='bold')
    ax2.set_xlabel('')
    ax2.set_ylabel('Daily PM2.5 Concentration (µg/m³)', fontsize=14)
    plt.tight_layout()
    plt.show()

    # --- Viz 3: Day-by-Day Calendar Heatmap ---
    control_series = df[df['policy_status'] == f'Control {phase}']['pm25']
    during_series = df[df['policy_status'] == f'During {phase}']['pm25']
    
    fig3, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    
    calmap.yearplot(control_series, year=control_series.index.year[0], ax=axes[0], cmap='YlOrRd')
    axes[0].set_title(f'Control Year: Daily PM2.5 ({control_series.index.year[0]})', fontsize=16)
    
    calmap.yearplot(during_series, year=during_series.index.year[0], ax=axes[1], cmap='YlOrRd')
    axes[1].set_title(f'Policy Year: Daily PM2.5 ({during_series.index.year[0]})', fontsize=16)
    
    fig3.suptitle(f'Daily Pollution Calendar: {phase} vs. Control', fontsize=20, weight='bold', y=1.05)
    plt.tight_layout()
    plt.show()

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Load and prepare data.
    processed_df = load_and_prepare_real_data()
    
    # 2. Run the statistical test for Phase 1.
    perform_statistical_analysis(processed_df, phase='Phase 1')
    
    # 3. Generate and display the visualizations.
    create_visualizations(processed_df, phase='Phase 1')
