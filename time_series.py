import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_data(x, y, title, xlabel='Date', ylabel='Value'):
    """ Plot graph showing trends """
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def trends(df):
    # Retail and Food Services Sales
    df_retail_food_total = df[df['KindOfBusiness'] == 'Retail and food services sales, total'].copy()
    # Sort data in ascending order
    df_retail_food_total.sort_values(by=['Date'], inplace=True)
    plot_data(df_retail_food_total['Date'], df_retail_food_total['Value'], 'Total Sales for the Retail and Food Services From 1992-2021')

    # Comparison between bookstores, sporting goods stores, and hobbies, toys, and games stores businesses
    df_sporting = df.loc[(df['KindOfBusiness'] == 'Sporting goods stores')].sort_values(by=['Date']).copy()
    df_hobbies = df.loc[df['KindOfBusiness'] == 'Hobby, toy, and game stores'].sort_values(by=['Date']).copy()
    df_book = df.loc[df['KindOfBusiness'] == 'Book stores'].sort_values(by=['Date']).copy()

    plt.plot(df_sporting['Date'],df_sporting['Value'], label='Sporting goods stores')
    plt.plot(df_hobbies['Date'],df_hobbies['Value'], label='Hobby, toy, and game stores')
    plt.plot(df_book['Date'],df_book['Value'], label='Book stores')
    plt.legend()
    plt.title('Comparison of retail businesses: bookstores, sporting goods stores, and hobbies, toys, and games stores')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()

    df = df[(df['Date'] > '1997-12-01') & (df['Date'] < '1999-01-01')]
    df_sporting = df.loc[(df['KindOfBusiness'] == 'Sporting goods stores')].sort_values(by=['Date']).copy()
    df_hobbies = df.loc[df['KindOfBusiness'] == 'Hobby, toy, and game stores'].sort_values(by=['Date']).copy()
    df_book = df.loc[df['KindOfBusiness'] == 'Book stores'].sort_values(by=['Date']).copy()

    plt.plot(df_sporting['Date'],df_sporting['Value'], label='Sporting goods stores')
    plt.plot(df_hobbies['Date'],df_hobbies['Value'], label='Hobby, toy, and game stores')
    plt.plot(df_book['Date'],df_book['Value'], label='Book stores')
    plt.legend()
    plt.title('Comparison of retail businesses: bookstores, sporting goods stores, and hobbies, toys, and games stores')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()


def percent_change(df):
    df_women = df.loc[(df['KindOfBusiness'] == "Women's clothing stores")].sort_values(by=['Date']).set_index('Date').drop(columns='KindOfBusiness').copy()
    df_men = df.loc[df['KindOfBusiness'] == "Men's clothing stores"].sort_values(by=['Date']).set_index('Date').drop(columns='KindOfBusiness').copy()

    df_women_percent = df_women.pct_change()
    df_men_percent = df_men.pct_change()

    plt.plot(df_women_percent.index,df_women_percent['Value'], label='Women')
    plt.plot(df_men_percent.index,df_men_percent['Value'], label='Men')
    plt.legend()
    plt.title("Comparison of women's clothing and men's clothing businesses")
    plt.xlabel('Date')
    plt.ylabel('Percent Change')
    plt.show()


def rolling_window(df):
    df_gas= df.loc[(df['KindOfBusiness'] == 'Gasoline stations')].sort_values(by=['Date']).copy()

    df_gas['RA_3'] = df_gas["Value"].rolling(3).mean()
    df_gas['RA_6'] = df_gas["Value"].rolling(6).mean()
    print(df_gas)

    plt.plot(df_gas['Date'],df_gas['Value'], label='Value')
    plt.plot(df_gas['Date'],df_gas['RA_3'], label='Rolling Avg 3 Months')
    plt.plot(df_gas['Date'],df_gas['RA_6'], label='Rolling Avg 6 Months')
    plt.legend()
    plt.title("Rolling Average of Gas Prices over 3 and 6 months")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()

    df_alochol= df.loc[(df['KindOfBusiness'] == 'Beer, wine, and liquor stores')].sort_values(by=['Date']).copy()

    df_alochol['RA_3'] = df_alochol["Value"].rolling(3, win_type ='triang').mean()
    df_alochol['RA_6'] = df_alochol["Value"].rolling(6, win_type ='triang').mean()

    plt.plot(df_alochol['Date'],df_alochol['Value'], label='Value')
    plt.plot(df_alochol['Date'],df_alochol['RA_3'], label='Rolling Avg 3 Months')
    plt.plot(df_alochol['Date'],df_alochol['RA_6'], label='Rolling Avg 6 Months')
    plt.legend()
    plt.title("Rolling Average of Beer, wine, and liquor stores over 3 and 6 months")
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()


def analyze(df):
    print('Analyzing the data..')
    trends(df)
    percent_change(df)
    rolling_window(df)

def test_queries(cursor):
    cursor.execute('SELECT * FROM mrts;')
    # print all the rows
    for row in cursor.fetchall():
        print(row)
    
    cursor.execute('SELECT COUNT(*) FROM mrts;')
    print(cursor.fetchone())
    
    cursor.execute('SELECT COUNT(DISTINCT KindOfBusiness) FROM mrts')
    print(cursor.fetchone())

    cursor.execute('SELECT KindOfBusiness, COUNT(*) FROM mrts GROUP BY KindOfBusiness;')
    # print all the rows
    for row in cursor.fetchall():
        print(row)

