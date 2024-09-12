import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def read_df_click():
    url = 'datasets/adsclicking.csv'
    df_click = pd.read_csv(url).copy()
    return df_click


def clean_df_click(df):
    df = df.drop(columns=['Unnamed: 0', 'Location', 'Device', 'Time_Spent_on_Site', 'Number_of_Pages_Viewed'])
    
    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, include_lowest=True)

    bins = [16, 24, 34, 44, 54, 90]
    labels = ['16-24', '25-34', '35-44', '45-54', '55+']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)

    return df

def click_by_category(df, size):
    df_pivot = df.pivot_table(index='Interest_Category', columns='Click', aggfunc='size', fill_value=0)

    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

    ax = df_pivot_percentage.plot(kind='bar', figsize=(8, 6), color=['#d9e6f2', '#4a90e2'])

    ax.set_ylim(size[0], size[1])

    plt.xlabel('Category')
    plt.ylabel('Percentage (%)')
    plt.xticks(rotation=0)

    plt.legend(title='Click', labels=['No Click', 'Click'])

    plt.tight_layout()

    return plt

def click_by_category_income(df):
    df_grouped = df.groupby(['Income_Range', 'Interest_Category', 'Click'], observed=False).size().unstack(fill_value=0)
    df_grouped['Total'] = df_grouped[0] + df_grouped[1]
    df_grouped['Percentage_Click'] = df_grouped[1] / df_grouped['Total'] * 100

    df_pivot = df_grouped.reset_index().pivot(index='Income_Range', columns='Interest_Category', values='Percentage_Click')

    plt.figure(figsize=(10, 6))

    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    ax.set_ylim(39, 61)

    plt.xlabel('Income range')
    plt.ylabel('Click (%)')

    plt.legend(title='Category')
    plt.xticks(rotation=0)
    plt.tight_layout()

    return plt

def click_by_category_age(df):
    df_grouped = df.groupby(['Age_Range', 'Interest_Category'], observed=False).agg({'Click': ['sum', 'count']})
    df_grouped.columns = ['Total_Clicks', 'Total_Count']
    df_grouped['Percentage_Click'] = df_grouped['Total_Clicks'] / df_grouped['Total_Count'] * 100

    df_pivot = df_grouped.reset_index()
    df_pivot =df_pivot.pivot(index='Age_Range', columns='Interest_Category', values='Percentage_Click')

    plt.figure(figsize=(10, 6))

    ax = df_pivot.plot(kind='bar', stacked=False, colormap='tab10', width=0.8, ax=plt.gca())
    ax.set_ylim([40, 60])

    plt.xlabel('Age range')
    plt.ylabel('Click (%)')

    plt.legend(title='Category', loc=('upper left'))
    plt.xticks(rotation=0)
    plt.tight_layout()

    return plt