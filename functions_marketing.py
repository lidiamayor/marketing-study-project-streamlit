import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def read_df_marketing():
    url = 'datasets/marketing_campaign.xlsx'
    df_marketing = pd.read_excel(url)
    return df_marketing

def clean_df_marketing(df):  
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

    education_levels = {'PhD': 'High', 'Master':'High', 
                        '2n Cycle': 'Middle', 'Graduation': 'Middle', 
                        'Basic': 'Low'
    }
    df["Education_Level"] = df['Education'].replace(education_levels) 

    living_status = {'Alone': 'Living Alone', 'Absurd': 'Living Alone', 'YOLO': 'Living Alone', 'Widow': 'Living Alone', 'Single': 'Living Alone', 'Divorced': 'Living Alone',
                        'Together': 'Living with Others', 'Married': 'Living with Others'
    } 
    df['Living_Status'] = df['Marital_Status'].replace(living_status)

    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
    df["Age"] = df['Dt_Customer'].dt.year - df["Year_Birth"]

    df['Is_Parent'] = (df['Kidhome'] + df['Teenhome'] > 0).astype(int)
    
    df = df[df['Age']<100]
    bins = [16, 24, 34, 44, 54, 64, 74] 
    labels = ['16-24', '25-34', '35-44', '45-54', '55-64', '65-74']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, right=False)

    to_drop = ['Z_CostContact', 'Year_Birth', 'ID', 'Marital_Status', 'Education','Kidhome', 'Teenhome', 'Recency', 'MntFruits','MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts','MntGoldProds', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 
            'Complain', 'Z_CostContact', 'Z_Revenue', 'Response']
    df = df.drop(to_drop, axis=1)

    return df

def site_purchases_by_age(df_wine):
    age_grouped = df_wine.groupby('Age_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    bar_width = 0.15
    age_range = np.arange(len(age_grouped))

    r1 = age_range
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    plt.figure(figsize=(9, 4))

    plt.bar(r1, age_grouped['NumDealsPurchases'], color='#a3c2c2', width=bar_width, edgecolor='grey', label='Deals Purchases')
    plt.bar(r2, age_grouped['NumWebPurchases'], color='#f2b5d4', width=bar_width, edgecolor='grey', label='Web Purchases')
    plt.bar(r3, age_grouped['NumCatalogPurchases'], color='#c5a3ff', width=bar_width, edgecolor='grey', label='Catalog Purchases')
    plt.bar(r4, age_grouped['NumStorePurchases'], color='#f6cfb7', width=bar_width, edgecolor='grey', label='Store Purchases')

    plt.xlabel('Age range')
    plt.xticks([r + bar_width*2 for r in range(len(age_grouped))], age_grouped['Age_Range'], rotation=0)
    plt.ylabel('Average purchases')

    plt.legend(loc='upper left',bbox_to_anchor=(-0.1, 1))

    plt.tight_layout()
    return plt

def site_purchases_by_income(df_wine):   
    income_grouped = df_wine.groupby('Income_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    bar_width = 0.15
    income_range = np.arange(len(income_grouped))

    r1 = income_range
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    plt.figure(figsize=(10, 4))

    plt.bar(r1, income_grouped['NumDealsPurchases'], color='#a3c2c2', width=bar_width, edgecolor='grey', label='Deals Purchases')
    plt.bar(r2, income_grouped['NumWebPurchases'], color='#f2b5d4', width=bar_width, edgecolor='grey', label='Web Purchases')
    plt.bar(r3, income_grouped['NumCatalogPurchases'], color='#c5a3ff', width=bar_width, edgecolor='grey', label='Catalog Purchases')
    plt.bar(r4, income_grouped['NumStorePurchases'], color='#f6cfb7', width=bar_width, edgecolor='grey', label='Store Purchases')

    plt.xlabel('Range income')
    plt.xticks([r + bar_width*2 for r in range(len(income_grouped))], income_grouped['Income_Range'], rotation=0)
    plt.ylabel('Average purchases')

    plt.legend()

    plt.tight_layout()
    return plt


def web_visits_by_age(df_wine):
    avg_visits = df_wine.groupby('Age_Range', observed=False)['NumWebVisitsMonth'].mean().reset_index()

    avg_visits = avg_visits.sort_values(by='Age_Range')

    plt.figure(figsize=(10, 6))

    sns.barplot(x='Age_Range', y='NumWebVisitsMonth', data=avg_visits, palette='pastel', hue='Age_Range', legend=False)

    plt.xlabel('Age range')
    plt.ylabel('Average visits in the website')

    plt.tight_layout()
    return plt

def purchases_by_income(df_income):
    plt.figure(figsize=(10, 6))
    plt.scatter(df_income['Income'], df_income['MntWines'], color='#6a9ac4', alpha=0.7, edgecolor='k')

    plt.xlabel('Incomes')
    plt.ylabel('Wine purchases')

    plt.tight_layout()
    return plt

def purchases_by_income_line(df_income):
    plt.figure(figsize=(10, 6))

    sns.regplot(x='Income', y='MntWines', data=df_income, scatter_kws={'color': '#6a9ac4', 'alpha': 0.7, 'edgecolor': 'k'}, line_kws={'color': 'red', 'lw': 2})

    plt.xlabel('Incomes')
    plt.ylabel('Wine purchases')

    plt.tight_layout()
    return plt

def purchases_by_education(df):
    education_mean = df.groupby('Education_Level')['MntWines'].mean().reset_index()

    education_mean = education_mean.sort_values(by='MntWines')

    plt.figure(figsize=(10, 6))

    sns.barplot(x='Education_Level', y='MntWines', data=education_mean, palette='pastel', hue='Education_Level')

    plt.xlabel('Education level')
    plt.ylabel('Average purchases wine')
    plt.xticks(rotation=0)

    plt.tight_layout()
    return plt

def son_at_home(df):
    parent_mean = df.groupby('Is_Parent')['MntWines'].mean().reset_index()

    parent_mean['Is_Parent'] = parent_mean['Is_Parent'].map({0: 'Not son at home', 1: 'Son at home'})

    plt.figure(figsize=(7, 7))

    plt.pie(parent_mean['MntWines'], labels=parent_mean['Is_Parent'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=140)

    return plt

def purchases_by_living_status(df):
    spend_by_livingstatus = df.groupby('Living_Status')['MntWines'].mean().reset_index()

    plt.figure(figsize=(10, 6))

    ax = sns.barplot(x='Living_Status', y='MntWines', data=spend_by_livingstatus, palette='pastel', hue='Living_Status')

    plt.xlabel('Living status')
    plt.ylabel('Average purchases wine')

    for i, row in spend_by_livingstatus.iterrows():
        ax.text(i, row['MntWines'] + 0.5, f'{row["MntWines"]:.2f}', ha='center')

    plt.tight_layout()
    return plt

def purchases_by_month(df):
    df['Month'] = df['Dt_Customer'].dt.month

    monthly_sales = df.groupby('Month')['MntWines'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(monthly_sales['Month'], monthly_sales['MntWines'], color='#4a90e2')

    plt.xlabel('Month')
    plt.ylabel('Total purchases wine')
    plt.xticks(ticks=range(1, 13), labels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])

    plt.tight_layout()
    return plt