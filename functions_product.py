import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def read_df_product():
    url = 'datasets/consumers.xls'
    df_product = pd.read_excel(url)
    return df_product

def clean_df_product(df):
    df = df.iloc[:,:7].copy()
    name_columns =  ['years','total','4+', '1-3', '-1','<<1','0']
    df.columns = name_columns
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

    df_both = df.loc[37:44].copy()
    df_both.index = range(1, len(df_both)+1)
    df_both['total_cons'] = df_both['4+']+df_both['1-3']+df_both['-1']+df_both['<<1']
    df_both = df_both.drop(columns=['total','4+', '1-3', '-1','<<1'])
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
    labels = ['Consumers', 'Not consumers']
    values = [df_both['total_cons'].iloc[0], df_both['0'].iloc[0]]

    colors = ['#A3E4D7', '#FAD7A0']
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    ax.axis('equal')

    return plt

def consume_m_w_by_age(df_men, df_women, x):
    if x != 2:
        df_men_filtered = df_men[df_men['years'] != 'Total']
    if x != 1:
        df_women_filtered = df_women[df_women['years'] != 'Total']

    plt.figure(figsize=(10, 6))

    if x != 2:
        plt.plot(df_men_filtered['years'], df_men_filtered['total_cons'], marker='o', label='Men', color='#a3c2c2')
        for i in range(len(df_men_filtered)):
            plt.text(i, df_men_filtered['total_cons'].iloc[i] + 1, 
                     f'{df_men_filtered["total_cons"].iloc[i]:.2f}%', 
                     ha='center', va='bottom', color='#a3c2c2')

    if x != 1:
        plt.plot(df_women_filtered['years'], df_women_filtered['total_cons'], marker='o', label='Women', color='#f2b5d4')
        for i in range(len(df_women_filtered)):
            plt.text(i, df_women_filtered['total_cons'].iloc[i] + 1, 
                     f'{df_women_filtered["total_cons"].iloc[i]:.2f}%', 
                     ha='center', va='bottom', color='#f2b5d4')

    plt.xlabel('Age range')
    plt.ylabel('Consumers (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    return plt

def consume_men_women(df_men, df_women):
    total_men = df_men[df_men['years'] == 'Total']
    total_women = df_women[df_women['years'] == 'Total']

    plt.figure(figsize=(9, 5))

    plt.bar('Men', total_men['total_cons'].values[0], color='#a3c2c2') 
    plt.bar('Women', total_women['total_cons'].values[0], color='#f2b5d4') 

    plt.ylabel('Consumers (%)')
    plt.tight_layout()

    for index, value in enumerate([total_men['total_cons'].values[0], total_women['total_cons'].values[0]]):
        plt.text(index, value + 1, f'{value:.2f}%', ha='center', va='bottom', fontsize=10, color='black')

    return plt

def consume_by_age(df_both):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='years', y='total_cons', data=df_both.loc[1:], palette='viridis',hue='total_cons', legend=False)

    plt.xlabel('Age range')
    plt.ylabel('Total consumption (%)')
    plt.xticks(rotation=30) 
    for p in ax.patches:
        height = p.get_height()
        rounded_height = round(height, 2)
        ax.annotate(f'{rounded_height}', 
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='center', 
                    xytext=(0, 5),
                    textcoords='offset points')

    plt.tight_layout()
    return plt