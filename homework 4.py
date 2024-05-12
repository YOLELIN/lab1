# PPHA 30537
# Spring 2024
# Homework 4

# YOUR NAME HERE Kunquan Wang

# YOUR CANVAS NAME HERE Kunquan Wang kw2641
# YOUR GITHUB USER NAME HERE YOLELIN

# Due date: Sunday May 12th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

# Question 1: Explore the data APIs available from Pandas DataReader. Pick
# any two countries, and then 
#   a) Find two time series for each place
#      - The time series should have some overlap, though it does not have to
#        be perfectly aligned.
#      - At least one should be from the World Bank, and at least one should
#        not be from the World Bank.
#      - At least one should have a frequency that does not match the others,
#        e.g. annual, quarterly, monthly.
#      - You do not have to make four distinct downloads if it's more appropriate
#        to do a group of them, e.g. by passing two series titles to FRED.
import pandas_datareader as pdr
from pandas_datareader import wb
from datetime import datetime
import pandas as pd

start = datetime(2001, 1, 1)
end = datetime(2022, 12, 31)

country1 = 'USA'
df1 = pdr.wb.download(country=country1, start=start, end=end)
print(df1)
df1.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/USA.csv', index=True)

country2 = 'CHN'
df2 = pdr.wb.download(country=country2, start=start, end=end)
print(df2)
df2.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/CHN.csv', index=True)

df3 = pdr.DataReader(name="UNRATE", data_source='fred', start=start, end=end)
print(df3)
df3.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/USA_unemp.csv', index=True)


df4 = pdr.wb.download(indicator='SL.UEM.TOTL.ZS', country=country2, start=start, end=end)
print(df4)
df4.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/CHN_unemp.csv', index=True)

#   b) Adjust the data so that all four are at the same frequency (you'll have
#      to look this up), then do any necessary merge and reshaping to put
#      them together into one long (tidy) format dataframe.

## I had some problems fixing the index and merge them from above, so I reload the files again to change index to column.
USA_GDP = pd.read_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/USA.csv')
print(USA_GDP.head())
USA_unemp = pd.read_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/USA_unemp.csv')
print(USA_unemp.head())

CHN_GDP = pd.read_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/CHN.csv')
print(CHN_GDP.head())
CHN_unemp = pd.read_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/CHN_unemp.csv')
print(CHN_unemp.head())

## Fix the date into year
USA_unemp['DATE'] = pd.to_datetime(USA_unemp['DATE'])
USA_unemp['year'] = USA_unemp['DATE'].dt.year
USA_unemp_annual = USA_unemp.groupby('year').UNRATE.mean().reset_index()

# Merge, rename data
USA_merged = pd.merge(USA_GDP, USA_unemp_annual, on='year', how='inner')
USA_merged['country'] = 'United States'
USA_merged.rename(columns={'UNRATE': 'unemployment_rate'}, inplace=True)

CHN_GDP['country'] = 'China'
CHN_unemp['country'] = 'China'
CHN_merged = pd.merge(CHN_GDP, CHN_unemp, on=['country', 'year'], how='inner')
CHN_merged.rename(columns={'SL.UEM.TOTL.ZS': 'unemployment_rate'}, inplace=True)

combined_data = pd.concat([USA_merged, CHN_merged], ignore_index=True)
combined_data.rename(columns={'NY.GDP.MKTP.CD': 'GDP'}, inplace=True)
combined_data.rename(columns={'NY.GNS.ICTR.ZS': 'GNS'}, inplace=True)

print(combined_data)

#   c) Finally, go back and change your earlier code so that the
#      countries and dates are set in variables at the top of the file. Your
#      final result for parts a and b should allow you to (hypothetically) 
#      modify these values easily so that your code would download the data
#      and merge for different countries and dates.
#      - You do not have to leave your code from any previous way you did it
#        in the file. If you did it this way from the start, congrats!
#      - You do not have to account for the validity of all the possible 
#        countries and dates, e.g. if you downloaded the US and Canada for 
#        1990-2000, you can ignore the fact that maybe this data for some
#        other two countries aren't available at these dates.

## Code provided above

#   d) Clean up any column names and values so that the data is consistent
#      and clear, e.g. don't leave some columns named in all caps and others
#      in all lower-case, or some with unclear names, or a column of mixed 
#      strings and integers. Write the dataframe you've created out to a 
#      file named q1.csv, and commit it to your repo.

## This data is clean and consistent :) 
combined_data.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/q1.csv', index=False)


# Question 2: On the following Harris School website:
# https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics
# There is a list of six bullet points under "Required courses" and 12
# bullet points under "Elective courses". Using requests and BeautifulSoup: 
#   - Collect the text of each of these bullet points
#   - Add each bullet point to the csv_doc list below as strings (following 
#     the columns already specified). The first string that gets added should be 
#     approximately in the form of: 
#     'required,PPHA 30535 or PPHA 30537 Data and Programming for Public Policy I'
#   - Hint: recall that \n is the new-line character in text
#   - You do not have to clean up the text of each bullet point, or split the details out
#     of it, like the course code and course description, but it's a good exercise to
#     think about.
#   - Using context management, write the data out to a file named q2.csv
#   - Finally, import Pandas and test loading q2.csv with the read_csv function.
#     Use asserts to test that the dataframe has 18 rows and two columns.
import requests
from bs4 import BeautifulSoup

url = 'https://harris.uchicago.edu/academics/design-your-path/certificates/certificate-data-analytics'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

csv_doc = ['type,description']

find_required = soup.find('h3', string='Required courses')
find_elective = soup.find('h3', string='Elective courses')
find_required2 = soup.find('p', string='Students must complete one of the following courses:')


required_courses = find_required.find_next('ul').find_all('li')
for course in required_courses:
    course_text = course.get_text(strip=True).replace('\n', ' ')
    csv_doc.append(f"required,{course_text}")
    
required_courses2 = find_required2.find_next('ul').find_all('li')
for course in required_courses2:
    course_text = course.get_text(strip=True).replace('\n', ' ')
    csv_doc.append(f"required,{course_text}")

elective_courses = find_elective.find_next('ul').find_all('li')
for course in elective_courses:
    course_text = course.get_text(strip=True).replace('\n', ' ')
    csv_doc.append(f"elective,{course_text}")

print(csv_doc)
course_df = pd.DataFrame(csv_doc)

course_df_split = course_df[0].str.split(',', expand=True)
new_header = course_df_split.iloc[0]
course_df_cleaned = course_df_split[1:]
course_df_cleaned.columns = new_header

print(course_df_cleaned.head())

course_df_cleaned.to_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/q2.csv', index=False)

course_df_test = pd.read_csv('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/pythonhw/q2.csv')
num_rows = len(course_df_test)
num_columns = len(course_df_test.columns)
print("Number of rows:", num_rows)
print("Number of columns:", num_columns)
