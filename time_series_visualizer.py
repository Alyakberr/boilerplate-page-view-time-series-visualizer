import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Fix for deprecated np.float used internally by seaborn
if not hasattr(np, 'float'):
    np.float = float

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
low_percentile = df["value"].quantile(0.025)
high_percentile = df["value"].quantile(0.975)
df = df[(df["value"] >= low_percentile) & (df["value"] <= high_percentile)]


def draw_line_plot():
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar["month_name"] = df_bar.index.strftime('%B')

    # Group by year and month to get mean values
    df_grouped = df_bar.groupby(["year", "month_name"], sort=False)["value"].mean().unstack()

    # Order months correctly
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    df_grouped.columns = month_order

    # Draw bar plot
    fig = df_grouped.plot(kind='bar', figsize=(15, 10)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Save image and return
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month

    # Sort by month number for correct display
    df_box = df_box.sort_values('month_num')

    # Draw box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

    # Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return
    fig.savefig('box_plot.png')
    return fig
