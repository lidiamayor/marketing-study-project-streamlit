import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from functions_product import read_df_product, clean_df_product, consume_wine, consume_m_w_by_age, consume_men_women, consume_by_age
from functions_marketing import read_df_marketing, clean_df_marketing, site_purchases_by_age, site_purchases_by_income, web_visits_by_age, purchases_by_income, purchases_by_income_line, purchases_by_education, son_at_home, purchases_by_living_status, purchases_by_month
from functions_click import read_df_click, clean_df_click, click_by_category, click_by_category_income, click_by_category_age


def main():
    """
    Main function of the Streamlit app. It contains the layout and 
    functionality of the app.

    The app is divided into three sections: Wine Consumption Study, Marketing Study and Click Study.
    """

    st.title('Data-Analysis marketing strategy for a wine company')
    st.write('##### Our goal is to thoroughly analyze the available data to craft the most effective marketing campaign.')
    st.write('##### We will focus on three key areas:')
    st.write('##### Identifying the largest consumer group: By examining demographic factors such as age, gender, and income, we will pinpoint who the top wine consumers are. This will enable us to create highly targeted and personalized campaigns for the right audience.')
    st.write('##### Understanding the most popular purchasing channels: We will assess whether customers prefer to buy in physical stores, through catalogs, or online. This information will help direct marketing efforts toward the most effective sales channels.')
    st.write('##### Optimizing ad click-through rates: By analyzing consumer interests (fashion, technology, travel, sports, etc.), we will identify which types of ads generate the highest engagement and clicks, especially across different income groups. This will allow us to create compelling ads that resonate with the target audience.')
    
    ######################## Wine Consumption Section #############################################
    
    st.divider()
    total_conclusions1 = []
    # Load data 
    df_product = read_df_product()
    df_both, df_men, df_women = clean_df_product(df_product)

    st.title('Wine consume study')
    st.page_link('https://www.ine.es/jaxi/Tabla.htm?path=/t15/p419/p02/a2003/l0/&file=02086.px&L=0', label='Wine consume Dataset from INEbase', icon="🍷")
    st.divider()
    st.sidebar.header("Filters product study") 

    # By age
    st.write('#### Percentage spanish people >16 consumers/not consumers')
    age_filter1 = st.selectbox("Select age range", df_both['years'].unique())
    filtered_wine = df_both[df_both['years'] == age_filter1]
    plt = consume_wine(filtered_wine)
    st.pyplot(plt)

    c1 = st.text_input('Conclusion 1: ')
    total_conclusions1.append(c1)


    st.write('#### Percentage of spanish people who consumes wine by age')
    age_filter2 = st.multiselect("Select age range", df_both['years'].unique())
    filtered_wine = df_both[df_both['years'].isin(age_filter2)]
    plt = consume_by_age(filtered_wine)
    st.pyplot(plt)

    c2 = st.text_input('Conclusion 2: ')
    total_conclusions1.append(c2)

    # By genre
    st.write('#### Percentage consumers by genres')
    genre_filter = st.radio("Select genre", ['Both', 'Men', 'Women'])
    
    if genre_filter=='Both':
        plt = consume_m_w_by_age(df_men, df_women, 0)
        st.pyplot(plt)
    elif genre_filter=='Men':
        plt = consume_m_w_by_age(df_men, df_women, 1)
        st.pyplot(plt)
    elif genre_filter=='Women':
        plt = consume_m_w_by_age(df_men, df_women, 2)
        st.pyplot(plt)

    st.write('#### Comparing both percentage of total consumers')
    plt = consume_men_women(df_men, df_women)
    st.pyplot(plt)

    c3 = st.text_input('Conclusion 3: ')
    total_conclusions1.append(c3)


    see1 = st.sidebar.toggle('See product conclusions')
    
    if see1 == True:
        st.write('### Summary conclusion about consume of wine in Spain:')
        for conc in total_conclusions1:
            if conc != '':
                st.write(f'##### - {conc}')


    ######################## Marketing Study Section #############################################
    
    st.divider()
    total_conclusions2 = []
    # Load data 
    df_marketing = read_df_marketing()
    df_marketing = clean_df_marketing(df_marketing)

    st.title('Marketing Study')
    st.page_link('https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign', label='Marketing campaign Dataset from Kaggle', icon="🛍️")
    st.divider()
    st.sidebar.divider()
    st.sidebar.header("Filters marketing study")

    wine_range = st.sidebar.slider('Select range of total amount spent on wine', value=[df_marketing['MntWines'].min(), df_marketing['MntWines'].max()])
    df_wine = df_marketing[(df_marketing['MntWines']>wine_range[0]) & (df_marketing['MntWines']<wine_range[1])]

    st.write('#### Average purchases by age and different channel')
    plt = site_purchases_by_age(df_wine)
    st.pyplot(plt)
    c4 = st.text_input('Conclusion 4: ')
    total_conclusions2.append(c4)

    st.write('#### Average purchases by income and different channel')
    plt = site_purchases_by_income(df_wine)
    st.pyplot(plt)

    c5 = st.text_input('Conclusion 5: ')
    total_conclusions2.append(c5) 
    c6 = st.text_input('Conclusion 6: ')
    total_conclusions2.append(c6)


    st.write('#### Average visits in the website by age')
    plt = web_visits_by_age(df_wine)
    st.pyplot(plt)
    c7 = st.text_input('Conclusion 7: ')
    total_conclusions2.append(c7)
    

    income_range = st.slider('Select range income', 6000.0, 110000.0, value=[6000.0, 110000.0])
    df_income = df_wine[(df_wine['Income']>income_range[0]) & (df_wine['Income']<income_range[1])]
    adjust = st.checkbox('Linear fit')

    st.write('#### Purchases by income')
    if adjust == False:
        plt = purchases_by_income(df_income)
        st.pyplot(plt)
    else:
        plt = purchases_by_income_line(df_income)
        st.pyplot(plt)

    c8 = st.text_input('Conclusion 8: ')
    total_conclusions2.append(c8)


    st.write('#### Average wine purchases by education')
    plt = purchases_by_education(df_wine)
    st.pyplot(plt)

    c9 = st.text_input('Conclusion 9: ')
    total_conclusions2.append(c9)


    st.write('#### Percentage wine purchases with son or without son at home')
    plt = son_at_home(df_wine)
    st.pyplot(plt)

    c10 = st.text_input('Conclusion 10: ')
    total_conclusions2.append(c10)


    st.write('#### Average wine purchases by living status')
    plt = purchases_by_living_status(df_wine)
    st.pyplot(plt)

    c11 = st.text_input('Conclusion 11: ')
    total_conclusions2.append(c11)


    st.write('#### Total wine purchases by month')
    plt = purchases_by_month(df_wine)
    st.pyplot(plt)

    c12 = st.text_input('Conclusion 12: ')
    total_conclusions2.append(c12)


    see2 = st.sidebar.toggle('See marketing conclusions')  
    if see2 == True:
        st.write('### Summary conclusion about the marketing:')
        for conc in total_conclusions2:
            if conc != '':
                st.write(f'##### - {conc}')


    ######################## Click Study Section #############################################
    
    st.divider()
    total_conclusions3 = []
    # Load data 
    df_click = read_df_click()
    df_click = clean_df_click(df_click)

    st.title('Click Study')
    st.page_link('https://www.kaggle.com/datasets/natchananprabhong/online-ad-click-prediction-dataset', label='Ad Click Prediction Dataset from Kaggle', icon="📣")
    st.divider()
    st.sidebar.divider()
    st.sidebar.header("Filters click study")

    income_rng = st.sidebar.slider('Select range income', 20000.0, 100000.0, value=[20000.0, 100000.0])
    filtered_click = df_click[(df_click['Income']>income_rng[0]) & (df_click['Income']<income_rng[1])]

    age_rng = st.sidebar.slider('Select range age', 16, 64, value=[16, 64])
    filtered2_click = filtered_click[(filtered_click['Age']>age_rng[0]) & (filtered_click['Age']<age_rng[1])]

    zoom_range = st.slider('Select size zoom', 20, 70, value=[20, 70])
    
    st.write('#### Percentage click by category')
    plt = click_by_category(filtered2_click, zoom_range)
    st.pyplot(plt)

    c13 = st.text_input('Conclusion 13: ')
    total_conclusions3.append(c13)


    st.write('#### Percentage click by category and income')
    plt = click_by_category_income(filtered2_click)
    st.pyplot(plt)

    c14 = st.text_input('Conclusion 14: ')
    total_conclusions3.append(c14)


    st.write('#### Percentage click by category and age')
    plt = click_by_category_age(filtered_click)
    st.pyplot(plt)

    c15 = st.text_input('Conclusion 15: ')
    total_conclusions3.append(c15)


    see3 = st.sidebar.toggle('See click conclusions')
    if see3 == True:
        st.write('### Summary conclusion about the marketing:')
        for conc in total_conclusions3:
            if conc != '':
                st.write(f'##### - {conc}')


    ############################## SUMMARY CONCLUSIONS #########################
    
    st.divider()

    total_conclusions = total_conclusions1 + total_conclusions2 + total_conclusions3

    st.write('## Conclusions: ')
    for conclusion in total_conclusions:
        if conclusion != '':
            st.write(f'##### - {conclusion}')


    
if __name__ == '__main__':
    main()