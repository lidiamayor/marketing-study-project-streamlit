import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def read_df_click():
    """
    Reads the adsclicking.csv dataset from the datasets folder into a pandas DataFrame.
    """
    url = 'datasets/adsclicking.csv'
    df_click = pd.read_csv(url).copy()
    return df_click


def clean_df_click(df):
    """
    Clean the adsclicking dataset by removing unnecessary columns and
    creating two new columns: Income_Range and Age_Range.
    """
    # Drop unnecessary columns
    df = df.drop(columns=['Unnamed: 0', 'Location', 'Device', 'Time_Spent_on_Site', 'Number_of_Pages_Viewed'])
    
    # Create the Income_Range column
    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, include_lowest=True)
    
    # Create the Age_Range column
    bins = [16, 24, 34, 44, 54, 90]
    labels = ['16-24', '25-34', '35-44', '45-54', '55+']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)

    return df


def click_by_category(df, size):
    """
    Creates a bar plot of the percentage of ad clicks by category.
    """
    # Create a pivot table of the ad clicks by category and click status
    df_pivot = df.pivot_table(index='Interest_Category', columns='Click', aggfunc='size', fill_value=0)

    # Calculate the percentage of ad clicks by category
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

    # Create a bar plot of the percentage of ad clicks by category
    ax = df_pivot_percentage.plot(kind='bar', figsize=(8, 6), color=['#d9e6f2', '#4a90e2'])

    # Set the y-axis limits
    ax.set_ylim(size[0], size[1])

    # Set the x-axis label
    plt.xlabel('Category')

    # Set the y-axis label
    plt.ylabel('Percentage (%)')

    # Rotate the x-axis labels
    plt.xticks(rotation=0)

    # Set the legend
    plt.legend(title='Click', labels=['No Click', 'Click'])

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def click_by_category_income(df):
    """
    Creates a bar plot of the percentage of ad clicks by category
    and income range.
    """
    # Create a pivot table of the ad clicks by category, income range, and click status
    df_grouped = df.groupby(['Income_Range', 'Interest_Category', 'Click'], observed=False).size().unstack(fill_value=0)

    # Calculate the total number of clicks by category and income range
    df_grouped['Total'] = df_grouped[0] + df_grouped[1]

    # Calculate the percentage of clicks by category and income range
    df_grouped['Percentage_Click'] = df_grouped[1] / df_grouped['Total'] * 100

    # Create a pivot table of the percentage of clicks by category and income range
    df_pivot = df_grouped.reset_index().pivot(index='Income_Range', columns='Interest_Category', values='Percentage_Click')

    # Create a bar plot of the percentage of clicks by category and income range
    plt.figure(figsize=(10, 6))

    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    ax.set_ylim(39, 61)

    # Set the x-axis label
    plt.xlabel('Income range')

    # Set the y-axis label
    plt.ylabel('Click (%)')

    # Set the legend
    plt.legend(title='Category')

    # Rotate the x-axis labels
    plt.xticks(rotation=0)

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def click_by_category_age(df):
    """
    Creates a bar plot of the percentage of ad clicks by category
    and age range.
    """
    # Create a pivot table of the ad clicks by category and age range
    df_grouped = df.groupby(['Age_Range', 'Interest_Category'], observed=False).agg({'Click': ['sum', 'count']})

    # Rename the columns of the grouped DataFrame
    df_grouped.columns = ['Total_Clicks', 'Total_Count']

    # Calculate the percentage of clicks by category and age range
    df_grouped['Percentage_Click'] = df_grouped['Total_Clicks'] / df_grouped['Total_Count'] * 100

    # Create a pivot table of the percentage of clicks by category and age range
    df_pivot = df_grouped.reset_index()
    df_pivot = df_pivot.pivot(index='Age_Range', columns='Interest_Category', values='Percentage_Click')

    # Create a bar plot of the percentage of clicks by category and age range
    plt.figure(figsize=(10, 6))

    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    ax.set_ylim([40, 60])

    # Set the x-axis label
    plt.xlabel('Age range')

    # Set the y-axis label
    plt.ylabel('Click (%)')

    # Set the legend
    plt.legend(title='Category', loc=('upper left'))

    # Rotate the x-axis labels
    plt.xticks(rotation=0)

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt