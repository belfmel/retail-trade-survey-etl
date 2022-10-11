import pandas as pd
import numpy as np
import math
import mysql.connector
import matplotlib.pyplot as plt

def unpivot_dataframe(df):
    """ Unpivots the source dataframe for each excel sheet """
    return pd.melt(df, id_vars='KindOfBusiness', value_vars=df.columns[1:])

def replace_with_zero(df, str):
    """ Replaces string value with 0 in the DataFrame """
    df.replace(str, 0, inplace=True)
    return df

def clean_source_data(df):
    """ Cleans source data for (S), (NA), null values, and column data types/renaming """
    # Replace all the (S) & (NA) to 0
    df = replace_with_zero(df, '(S)')
    df = replace_with_zero(df, '(NA)')

    # Drop all rows where there is a null value
    df.dropna(axis=0, inplace=True)

    # Convert variable column to date format
    df['Date'] = pd.to_datetime(df['variable'])
    df.drop(columns=['variable'], inplace=True)

    df.rename(columns={'value': 'Value'}, inplace=True)
    return df

def connect_db(db):
    """ Connect to the MySQL Database """
    config = {
        'user': db['user'],
        'password': db['pass'],
        'host': db['host'],
        'database': db['db'],
        'auth_plugin': 'mysql_native_password'
    }
    cnx = mysql.connector.connect(**config)
    return cnx

def disconnect_db(cursor, cnx):
    """ Disconnect from the MySQL Database """
    cursor.close()
    cnx.close()

def create_db(cursor):
    """ Create DataBase mrts """
    drop_db = 'DROP DATABASE IF EXISTS `mrts`'
    cursor.execute(drop_db)
    create_db = 'CREATE DATABASE IF NOT EXISTS `mrts`'
    cursor.execute(create_db)
    use_db = 'USE `mrts`'
    cursor.execute(use_db)
    cursor.execute('SET NAMES UTF8MB4;')
    cursor.execute('SET character_set_client = UTF8MB4;')

def create_table(cursor):
    """ Create mrts Table """
    query = (f"CREATE TABLE `mrts` (`KindOfBusiness` varchar(100) NOT NULL, `Value` float(10,2) NOT NULL, `Date` DATE NOT NULL, PRIMARY KEY (KindOfBusiness, Date))")
    cursor.execute(query)

def insert_data(cursor, df):
    """ Insert DataFrame into mrts table """
    for index, row in df.iterrows():
        cursor.execute('INSERT INTO mrts (KindOfBusiness,Value,Date) VALUES(%s, %s, %s);', (row[0], row[1], str(row[2])))


