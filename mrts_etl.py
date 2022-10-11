from cgi import test
import pandas as pd
import yaml
from etl import connect_db, disconnect_db, insert_data, unpivot_dataframe, clean_source_data, create_db, create_table
from time_series import analyze, test_queries

# Source Data Details
filename = 'mrtssales92-present.xls'
sheets = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992']

# Load properties from yaml file
db = yaml.safe_load(open('db.yaml'))

# Connect SQL Database
cnx = connect_db(db)
cursor = cnx.cursor()

# Initialize Database
create_db(cursor)

# Need to clean up sheet 2021 separately as it does not match other sheets
finaldf = pd.read_excel(filename, sheet_name='2021', skiprows=4, skipfooter=50)
finaldf.drop(finaldf.columns[[0,4,5]], axis=1, inplace=True)
# Rename columns
colnames = {'Unnamed: 1': 'KindOfBusiness', 'Feb. 2021(p)': 'Feb. 2021'}
finaldf.rename(columns=colnames, inplace=True)
# Unpivot the dataframe
finaldf = unpivot_dataframe(finaldf)
# Clean up the rows by changing (S) & (NA) to 0, dropping null rows, and creating date column
finaldf = clean_source_data(finaldf)

for sheet in sheets:
    # Skip first 4 rows and skip last 50 rows
    df = pd.read_excel(filename, sheet_name=sheet, skiprows=4, skipfooter=50)
    # Drop first column and last column
    df.drop(df.columns[[0,14]], axis=1, inplace=True)
    # Rename first column
    colnames = {'Unnamed: 1': 'KindOfBusiness'}
    df.rename(columns=colnames, inplace=True)
    # Unpivot the dataframe
    df = unpivot_dataframe(df)
    # Clean up the rows by changing (S) & (NA) to 0, dropping null rows, and creating date column
    df = clean_source_data(df)
    # Merge the data into one dataframe
    finaldf = pd.concat([finaldf,df], ignore_index=True)

print(finaldf)
print(finaldf.info())

# Loads the final dataframe into mysql database
create_table(cursor)
insert_data(cursor, finaldf)

# Commit changes to database
cnx.commit()

# Disconnect Database
disconnect_db(cursor, cnx)

# Analyze the dataset 
analyze(finaldf)