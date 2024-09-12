import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def read_df_product():
    """
    Reads the consumers.xls dataset from the datasets folder into a pandas DataFrame.
    """
    url = 'datasets/consumers.xls'
    df_product = pd.read_excel(url)
    return df_product

def clean_df_product(df):
    """
    Clean the consumers.xls dataset by performing the following operations:

    1. Rename columns to strip leading and trailing whitespace.
    2. Drop duplicate rows.
    3. Replace values in the 'years' column with more readable labels.
    4. Create a new column 'total_cons' by summing the '4+', '1-3', '-1', and '<<1' columns.
    5. Drop the 'total', '4+', '1-3', '-1', and '<<1' columns.
    6. Split the dataset into three DataFrames: df_both, df_men, and df_women.

    Returns a tuple of three DataFrames: df_both, df_men, and df_women.
    """
    # Rename columns to strip leading and trailing whitespace
    df = df.iloc[:,:7].copy()
    name_columns =  ['years','total','4+', '1-3', '-1','<<1','0']
    df.columns = name_columns

    # Replace values in the 'years' column with more readable labels
    df['years'] = df['years'].replace({
        '        Total':'Total',
        '        De 16 a 24 años': '16-24',
        '        De 25 a 34 años': '25-34',
        '        De 35 a 44 años': '35-44',
        '        De 45 a 54 años': '45-54',
        '        De 55 a 64 años': '55-64',
        '        De 65 a 74 años': '65-74',
        '        De 75 y más años': '75+'
    })

    # Create a new column 'total_cons' by summing the '4+', '1-3', '-1', and '<<1' columns
    df_both = df.loc[37:44].copy()
    df_both.index = range(1, len(df_both)+1)
    df_both['total_cons'] = df_both['4+']+df_both['1-3']+df_both['-1']+df_both['<<1']

    # Drop the 'total', '4+', '1-3', '-1', and '<<1' columns
    df_both = df_both.drop(columns=['total','4+', '1-3', '-1','<<1'])

    # Split the dataset into three DataFrames: df_both, df_men, and df_women
    df_men = df.loc[46:53].copy()
    df_men.index = range(1, len(df_men)+1)
    df_men['total_cons'] = df_men['4+']+df_men['1-3']+df_men['-1']+df_men['<<1']
    df_men = df_men.drop(columns=['total', '4+', '1-3', '-1','<<1'])

    df_women = df.loc[55:62].copy()
    df_women.index = range(1, len(df_women)+1)
    df_women['total_cons'] = df_women['4+']+df_women['1-3']+df_women['-1']+df_women['<<1']
    df_women = df_women.drop(columns=['total', '4+', '1-3', '-1','<<1'])

    return df_both, df_men, df_women


def consume_wine(df_both):
    """
    Creates a pie chart of the average number of wine purchases by customers
    with a son at home and those without a son at home.
    """
    # Get the labels and values for the pie chart
    labels = ['Consumers', 'Not consumers']
    values = [df_both['total_cons'].iloc[0], df_both['0'].iloc[0]]

    # Set the colors for the pie chart
    colors = ['#A3E4D7', '#FAD7A0']

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the pie chart
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Set the axis to be equal
    ax.axis('equal')

    # Return the figure
    return plt

def consume_m_w_by_age(df_men, df_women, x):
    """
    Creates a bar chart of the percentage of consumers by age range for men and women.
    """
    # Filter the data to only include the age ranges (not the total)
    if x != 2:
        df_men_filtered = df_men[df_men['years'] != 'Total']
    if x != 1:
        df_women_filtered = df_women[df_women['years'] != 'Total']

    # Create the figure and axis
    plt.figure(figsize=(10, 6))

    # Plot the men's data if requested
    if x != 2:
        plt.plot(df_men_filtered['years'], df_men_filtered['total_cons'], marker='o', label='Men', color='#a3c2c2')
        # Add the percentages as text
        for i in range(len(df_men_filtered)):
            plt.text(i, df_men_filtered['total_cons'].iloc[i] + 1, 
                     f'{df_men_filtered["total_cons"].iloc[i]:.2f}%', 
                     ha='center', va='bottom', color='#a3c2c2')

    # Plot the women's data if requested
    if x != 1:
        plt.plot(df_women_filtered['years'], df_women_filtered['total_cons'], marker='o', label='Women', color='#f2b5d4')
        # Add the percentages as text
        for i in range(len(df_women_filtered)):
            plt.text(i, df_women_filtered['total_cons'].iloc[i] + 1, 
                     f'{df_women_filtered["total_cons"].iloc[i]:.2f}%', 
                     ha='center', va='bottom', color='#f2b5d4')

    # Set the x and y labels
    plt.xlabel('Age range')
    plt.ylabel('Consumers (%)')

    # Add a legend
    plt.legend()

    # Add a grid
    plt.grid(True, linestyle='--', alpha=0.7)

    # Set the layout to be tight
    plt.tight_layout()

    # Return the figure
    return plt

def consume_men_women(df_men, df_women):
    """
    Creates a bar chart of the percentage of consumers for men and women.
    """
    total_men = df_men[df_men['years'] == 'Total']
    total_women = df_women[df_women['years'] == 'Total']

    # Create the figure and axis
    plt.figure(figsize=(9, 5))

    # Plot the men's data
    plt.bar('Men', total_men['total_cons'].values[0], color='#a3c2c2') 
    # Plot the women's data
    plt.bar('Women', total_women['total_cons'].values[0], color='#f2b5d4') 

    # Set the y-axis label
    plt.ylabel('Consumers (%)')
    # Set the layout to be tight
    plt.tight_layout()

    # Add the percentages as text
    for index, value in enumerate([total_men['total_cons'].values[0], total_women['total_cons'].values[0]]):
        plt.text(index, value + 1, f'{value:.2f}%', ha='center', va='bottom', fontsize=10, color='black')

    # Return the figure
    return plt

def consume_by_age(df_both):
    """
    Creates a bar chart of the total consumption of wine for each age range.
    """
    # Create the figure with the specified size
    plt.figure(figsize=(10, 6))
    # Create the bar plot with the specified data and colors
    ax = sns.barplot(x='years', y='total_cons', data=df_both.loc[1:], palette='viridis',hue='total_cons', legend=False)

    # Set the x-axis label
    plt.xlabel('Age range')
    # Set the y-axis label
    plt.ylabel('Total consumption (%)')
    # Rotate the x-axis tick labels
    plt.xticks(rotation=30) 
    # Iterate over the bars and add the percentages as text
    for p in ax.patches:
        height = p.get_height()
        rounded_height = round(height, 2)
        ax.annotate(f'{rounded_height}', 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='center', 
                    xytext=(0, 5),
                    textcoords='offset points')

    # Set the layout to be tight
    plt.tight_layout()
    # Return the figure
    return plt
