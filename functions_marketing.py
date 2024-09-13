import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def read_df_marketing():
    """
    Reads the marketing_campaign.xlsx dataset from the datasets folder into a pandas DataFrame.
    """
    url = 'datasets/marketing_campaign.xlsx'
    df_marketing = pd.read_excel(url)
    return df_marketing


def clean_df_marketing(df):  
    """
    Cleans the marketing_campaign.xlsx dataset by performing the following operations:

    1. Renames the columns to strip leading and trailing whitespace.
    2. Drops duplicate rows.
    3. Creates a new column 'Education_Level' by mapping the 'Education' column to 'High', 'Middle', or 'Low' based on the education level.
    4. Creates a new column 'Living_Status' by mapping the 'Marital_Status' column to 'Living Alone' or 'Living with Others' based on the marital status.
    5. Calculates the age of the customer by subtracting the year of birth from the year of the customer date.
    6. Creates a new column 'Is_Parent' by setting it to 1 if the customer has kids or teenagers at home, otherwise 0.
    7. Creates a new column 'Age_Range' by binning the age of the customer into ranges of 16-24, 25-34, 35-44, 45-54, 55-64, 65-74.
    8. Creates a new column 'Income_Range' by binning the income of the customer into ranges of 20k-40k, 40k-60k, 60k-80k, 80k-100k.
    9. Drops unnecessary columns.

    Returns a cleaned DataFrame
    """

    # Rename columns to strip leading and trailing whitespace
    df.columns = df.columns.str.strip()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Create a new column 'Education_Level' by mapping the 'Education' column
    education_levels = {'PhD': 'High', 'Master':'High', 
                        '2n Cycle': 'Middle', 'Graduation': 'Middle', 
                        'Basic': 'Low'
    }
    df["Education_Level"] = df['Education'].replace(education_levels) 

    # Create a new column 'Living_Status' by mapping the 'Marital_Status' column
    living_status = {'Alone': 'Living Alone', 'Absurd': 'Living Alone', 'YOLO': 'Living Alone', 'Widow': 'Living Alone', 'Single': 'Living Alone', 'Divorced': 'Living Alone',
                        'Together': 'Living with Others', 'Married': 'Living with Others'
    } 
    df['Living_Status'] = df['Marital_Status'].replace(living_status)

    # Calculate the age of the customer
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
    df["Age"] = df['Dt_Customer'].dt.year - df["Year_Birth"]

    # Create a new column 'Is_Parent' by setting it to 1 if the customer has kids or teenagers at home, otherwise 0
    df['Is_Parent'] = (df['Kidhome'] + df['Teenhome'] > 0).astype(int)
    
    # Drop rows with age > 100
    df = df[df['Age']<100]

    # Create a new column 'Age_Range' by binning the age of the customer
    bins = [16, 24, 34, 44, 54, 64, 74] 
    labels = ['16-24', '25-34', '35-44', '45-54', '55-64', '65-74']
    df['Age_Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Create a new column 'Income_Range' by binning the income of the customer
    bins = [20000, 40000, 60000, 80000, 100000]
    labels = ['20k-40k', '40k-60k', '60k-80k', '80k-100k']
    df['Income_Range'] = pd.cut(df['Income'], bins=bins, labels=labels, right=False)

    # Drop unnecessary columns
    to_drop = ['Z_CostContact', 'Year_Birth', 'ID', 'Marital_Status', 'Education','Kidhome', 'Teenhome', 'Recency', 'MntFruits','MntMeatProducts',
            'MntFishProducts', 'MntSweetProducts','MntGoldProds', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 
            'Complain', 'Z_CostContact', 'Z_Revenue', 'Response']
    df = df.drop(to_drop, axis=1)

    return df


def site_purchases_by_age(df_wine):
    """
    Creates a bar plot of the average purchases by age range
    """
    # Calculate the average purchases by age range
    age_grouped = df_wine.groupby('Age_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    # Create the bar plot
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

    # Set the x-axis label
    plt.xlabel('Age range')

    # Set the x-axis tick labels
    plt.xticks([r + bar_width*2 for r in range(len(age_grouped))], age_grouped['Age_Range'], rotation=0)

    # Set the y-axis label
    plt.ylabel('Average purchases')

    # Set the legend
    plt.legend(loc='upper left',bbox_to_anchor=(-0.1, 1))

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def site_purchases_by_income(df_wine):
    """
    Creates a bar plot of the average purchases by income range.
    """
    # Calculate the mean of the number of purchases by income range
    income_grouped = df_wine.groupby('Income_Range', observed=False).agg({
        'NumDealsPurchases': 'mean',
        'NumWebPurchases': 'mean',
        'NumCatalogPurchases': 'mean',
        'NumStorePurchases': 'mean',
    }).reset_index()

    # Set the bar width
    bar_width = 0.15

    # Get the range of income values
    income_range = np.arange(len(income_grouped))

    # Set the x values for each bar
    r1 = income_range
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    # Create the figure
    plt.figure(figsize=(10, 4))

    # Plot the bars
    plt.bar(r1, income_grouped['NumDealsPurchases'], color='#a3c2c2', width=bar_width, edgecolor='grey', label='Deals Purchases')
    plt.bar(r2, income_grouped['NumWebPurchases'], color='#f2b5d4', width=bar_width, edgecolor='grey', label='Web Purchases')
    plt.bar(r3, income_grouped['NumCatalogPurchases'], color='#c5a3ff', width=bar_width, edgecolor='grey', label='Catalog Purchases')
    plt.bar(r4, income_grouped['NumStorePurchases'], color='#f6cfb7', width=bar_width, edgecolor='grey', label='Store Purchases')

    # Set the x-axis label
    plt.xlabel('Range income')

    # Set the x-axis tick labels
    plt.xticks([r + bar_width*2 for r in range(len(income_grouped))], income_grouped['Income_Range'], rotation=0)

    # Set the y-axis label
    plt.ylabel('Average purchases')

    # Set the legend
    plt.legend()

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def web_visits_by_age(df_wine):
    """
    Creates a bar plot of the average number of website visits by age range.
    """
    # Calculate the average number of website visits by age range
    avg_visits = df_wine.groupby('Age_Range', observed=False)['NumWebVisitsMonth'].mean().reset_index()

    # Sort the dataframe by age range
    avg_visits = avg_visits.sort_values(by='Age_Range')

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the bars
    sns.barplot(x='Age_Range', y='NumWebVisitsMonth', data=avg_visits, palette='pastel', hue='Age_Range', legend=False)

    # Set the x-axis label
    plt.xlabel('Age range')

    # Set the y-axis label
    plt.ylabel('Average visits in the website')

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def purchases_by_income(df_income):
    """
    Creates a scatter plot of the relationship between income and wine purchases.
    """
    # Create the figure

    plt.figure(figsize=(10, 6))

    # Plot the scatter plot
    plt.scatter(df_income['Income'], df_income['MntWines'], color='#6a9ac4', alpha=0.7, edgecolor='k')

    # Set the x-axis label
    plt.xlabel('Incomes')

    # Set the y-axis label
    plt.ylabel('Wine purchases')

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def purchases_by_income_line(df_income):
    """
    Creates a scatter plot of the relationship between income and wine purchases with a regression line.
    """

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the scatter plot
    sns.regplot(x='Income', y='MntWines', data=df_income, 
                scatter_kws={'color': '#6a9ac4', 'alpha': 0.7, 'edgecolor': 'k'}, 
                line_kws={'color': 'red', 'lw': 2})

    # Set the x-axis label
    plt.xlabel('Incomes')

    # Set the y-axis label
    plt.ylabel('Wine purchases')

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def purchases_by_education(df):
    """
    Creates a bar plot of the average number of wine purchases by education level.
    """
    # Calculate the average number of purchases by education level
    education_mean = df.groupby('Education_Level')['MntWines'].mean().reset_index()

    # Sort the DataFrame by the average number of purchases
    education_mean = education_mean.sort_values(by='MntWines')

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the bars
    sns.barplot(x='Education_Level', y='MntWines', data=education_mean, palette='pastel', hue='Education_Level')

    # Set the x-axis label
    plt.xlabel('Education level')

    # Set the y-axis label
    plt.ylabel('Average purchases wine')

    # Rotate the x-axis labels
    plt.xticks(rotation=0)

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def son_at_home(df):
    """
    Creates a pie chart of the average number of wine purchases by customers
    with a son at home and those without a son at home.
    """
    # Calculate the mean number of purchases by customers with a son at home and those without a son at home
    parent_mean = df.groupby('Is_Parent')['MntWines'].mean().reset_index()

    # Map the values of the 'Is_Parent' column to the labels for the pie chart
    parent_mean['Is_Parent'] = parent_mean['Is_Parent'].map({0: 'Not son at home', 1: 'Son at home'})

    # Create the figure
    plt.figure(figsize=(7, 7))

    # Plot the pie chart
    plt.pie(parent_mean['MntWines'], labels=parent_mean['Is_Parent'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], startangle=140)

    # Return the figure
    return plt


def purchases_by_living_status(df):
    """
    Creates a bar plot of the average number of wine purchases by living status.
    """
    # Calculate the mean number of purchases by living status
    spend_by_livingstatus = df.groupby('Living_Status')['MntWines'].mean().reset_index()

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the bars
    ax = sns.barplot(x='Living_Status', y='MntWines', data=spend_by_livingstatus, palette='pastel', hue='Living_Status')

    # Set the x-axis label
    plt.xlabel('Living status')

    # Set the y-axis label
    plt.ylabel('Average purchases wine')

    # Add the actual values to the bars
    for i, row in spend_by_livingstatus.iterrows():
        ax.text(i, row['MntWines'] + 0.5, f'{row["MntWines"]:.2f}', ha='center')

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt


def purchases_by_month(df):
    """
    Creates a bar plot of the total number of wine purchases per month.
    """
    # Create a new column with the month of the customer
    df['Month'] = df['Dt_Customer'].dt.month

    # Calculate the total number of purchases per month
    monthly_sales = df.groupby('Month')['MntWines'].sum().reset_index()

    # Create the figure
    plt.figure(figsize=(10, 6))

    # Plot the bars
    plt.bar(monthly_sales['Month'], monthly_sales['MntWines'], color='#4a90e2')

    # Set the x-axis label
    plt.xlabel('Month')

    # Set the y-axis label
    plt.ylabel('Total purchases wine')

    # Set the x-axis tick labels
    plt.xticks(ticks=range(1, 13), labels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])

    # Set the figure layout tight
    plt.tight_layout()

    # Return the figure
    return plt