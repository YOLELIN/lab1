# PPHA 30537
# Spring 2024
# Homework 3

# YOUR NAME HERE Kunquan Wang

# YOUR CANVAS NAME HERE Kunquan Wang kw2641
# YOUR GITHUB USER NAME HERE YOLELIN

# Due date: Sunday May 5th before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

#NOTE: All of the plots the questions ask for should be saved and committed to
# your repo under the name "q1_1_plot.png" (for 1.1), "q1_2_plot.png" (for 1.2),
# etc. using fig.savefig. If a question calls for more than one plot, name them
# "q1_1a_plot.png", "q1_1b_plot.png",  etc.

# Question 1.1: With the x and y values below, create a plot using only Matplotlib.
# You should plot y1 as a scatter plot and y2 as a line, using different colors
# and a legend.  You can name the data simply "y1" and "y2".  Make sure the
# axis tick labels are legible.  Add a title that reads "HW3 Q1.1".

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

x = pd.date_range(start='1990/1/1', end='1991/12/1', freq='MS')
y1 = np.random.normal(10, 2, len(x))
y2 = [np.sin(v)+10 for v in range(len(x))]

plt.figure(figsize=(10, 6))
plt.scatter(x, y1, color='orange', label='y1')
plt.plot(x, y2, color='darkblue', label='y2')

plt.xticks(rotation=45)
plt.title('HW3 Q1.1')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()

plt.tight_layout()
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_1_plot.png')
plt.show()

# Question 1.2: Using only Matplotlib, reproduce the figure in this repo named
# question_2_figure.png.

## I'm not sure about this question, are we going to reproduce it as "question_2_figure.png" or "q1_2_plot.png"???
x = [10, 20]
y_blue = [20, 10]
y_red = [10, 20]

plt.figure(figsize=(8, 6))
plt.plot(x, y_blue, label='Blue', color='blue')
plt.plot(x, y_red, label='Red', color='red')


plt.title('X marks the spot')
plt.xlabel('X axis label') 
plt.ylabel('Y axis label')

plt.legend()
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_2_plot.png')
plt.show()


# Question 1.3: Load the mpg.csv file that is in this repo, and create a
# plot that tests the following hypothesis: a car with an engine that has
# a higher displacement (i.e. is bigger) will get worse gas mileage than
# one that has a smaller displacement.  Test the same hypothesis for mpg
# against horsepower and weight.
file_path = r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\mpg.csv'

mpg = pd.read_csv(file_path)

print(mpg.head())
fig, axes = plt.subplots(1, 3, figsize=(10, 6))

# Scatter plot for MPG vs. Displacement
axes[0].scatter(mpg['displacement'], mpg['mpg'], alpha=0.5, color='darkblue')
axes[0].set_title('MPG vs. Displacement')
axes[0].set_xlabel('Displacement')
axes[0].set_ylabel('MPG')

# Scatter plot for MPG vs. Horsepower
axes[1].scatter(mpg['horsepower'], mpg['mpg'], alpha=0.5, color='grey')
axes[1].set_title('MPG vs. Horsepower')
axes[1].set_xlabel('Horsepower')
axes[1].set_ylabel('MPG')

# Scatter plot for MPG vs. Weight
axes[2].scatter(mpg['weight'], mpg['mpg'], alpha=0.5, color='orange')
axes[2].set_title('MPG vs. Weight')
axes[2].set_xlabel('Weight')
axes[2].set_ylabel('MPG')

plt.tight_layout()
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_3_plot.png')
plt.show()

# Question 1.4: Continuing with the data from question 1.3, create a scatter plot 
# with mpg on the y-axis and cylinders on the x-axis.  Explain what is wrong 
# with this plot with a 1-2 line comment.  Now create a box plot using Seaborn
# that uses cylinders as the groupings on the x-axis, and mpg as the values
# up the y-axis.

plt.figure(figsize=(10, 6))
plt.scatter(mpg['cylinders'], mpg['mpg'], alpha=0.5)
plt.title('MPG vs. Cylinders')
plt.xlabel('Number of Cylinders')
plt.ylabel('Miles Per Gallon')
plt.grid(True)
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_4_1_plot.png')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='cylinders', y='mpg', data=mpg)
plt.title('Distribution of MPG by Number of Cylinders')
plt.xlabel('Number of Cylinders')
plt.ylabel('Miles Per Gallon')
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_4_2_plot.png')
plt.show()

# Question 1.5: Continuing with the data from question 1.3, create a two-by-two 
# grid of subplots, where each one has mpg on the y-axis and one of 
# displacement, horsepower, weight, and acceleration on the x-axis.  To clean 
# up this plot:
#   - Remove the y-axis tick labels (the values) on the right two subplots - 
#     the scale of the ticks will already be aligned because the mpg values 
#     are the same in all axis.  
#   - Add a title to the figure (not the subplots) that reads "Changes in MPG"
#   - Add a y-label to the figure (not the subplots) that says "mpg"
#   - Add an x-label to each subplot for the x values
# Finally, use the savefig method to save this figure to your repo.  If any
# labels or values overlap other chart elements, go back and adjust spacing.

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

variables = ['displacement', 'horsepower', 'weight', 'acceleration']
titles = ['Displacement', 'Horsepower', 'Weight', 'Acceleration']

for ax, variable, title in zip(axes.flatten(), variables, titles):
    ax.scatter(mpg[variable], mpg['mpg'], alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel(variable)

axes[0, 1].set_yticklabels([])
axes[1, 1].set_yticklabels([])

fig.suptitle('Changes in MPG')
fig.text(0.5, 0.04, 'Vehicle Characteristics', ha='center')
fig.text(0.04, 0.5, 'MPG', va='center', rotation='vertical')

plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])

plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_5_plot.png')

plt.show()

# Question 1.6: Are cars from the USA, Japan, or Europe the least fuel
# efficient, on average?  Answer this with a plot and a one-line comment.

## The cars from USA have the least fuel efficiency on average.
average_mpg_by_origin = mpg.groupby('origin')['mpg'].mean()

plt.figure(figsize=(8, 6))
sns.barplot(x=average_mpg_by_origin.index, y=average_mpg_by_origin.values, palette='viridis')
plt.title('Average MPG by Country')
plt.xlabel('Country')
plt.ylabel('Average MPG')
plt.ylim(0, average_mpg_by_origin.max() + 5) 
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_6_plot.png')
plt.show()

# Question 1.7: Using Seaborn, create a scatter plot of mpg versus displacement,
# while showing dots as different colors depending on the country of origin.
# Explain in a one-line comment what this plot says about the results of 
# question 1.6.

## A lot of cars from USA have higher displacement than cars from Europe and Japan,
## which resulted in the low fuel efficiency of USA cars.
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(data=mpg, x='displacement', y='mpg', hue='origin', palette='coolwarm', alpha=0.7)
plt.title('MPG vs. Displacement by Country')
plt.xlabel('Displacement')
plt.ylabel('MPG')
plt.legend(title='Origin', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q1_7_plot.png')
plt.show()

import statsmodels.api as sm
import statsmodels.formula.api as smf
# Question 2: The file unemp.csv contains the monthly seasonally-adjusted unemployment
# rates for US states from January 2020 to December 2022. Load it as a dataframe, as well
# as the data from the policy_uncertainty.xlsx file from homework 2 (you do not have to make
# any of the changes to this data that were part of HW2, unless you need to in order to 
# answer the following questions).
#    2.1: Merge both dataframes together
policy_uncertainty_df = pd.read_excel(r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\policy_uncertainty.xlsx')
unemp_df = pd.read_csv(r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\unemp.csv')
unemp_df['DATE'] = pd.to_datetime(unemp_df['DATE'])

unemp_df['year'] = unemp_df['DATE'].dt.year
unemp_df['month'] = unemp_df['DATE'].dt.month

## We have to change the ABBR of the stats to its full name
state_mapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

unemp_df['STATE'] = unemp_df['STATE'].map(state_mapping)

unemp_df.rename(columns={'STATE': 'state'}, inplace=True)

merged_df = pd.merge(policy_uncertainty_df, unemp_df, on=['state', 'year', 'month'], how='inner')

print(merged_df.head())

#    2.2: Calculate the log-first-difference (LFD) of the EPU-C data
merged_df['log_EPU_Composite'] = np.log(merged_df['EPU_Composite'])

merged_df['LFD_EPU_Composite'] = merged_df.groupby('state')['log_EPU_Composite'].diff()

print(merged_df[['state', 'year', 'EPU_Composite', 'log_EPU_Composite', 'LFD_EPU_Composite']].head())

#    2.2: Select five states and create one Matplotlib figure that shows the unemployment rate
#         and the LFD of EPU-C over time for each state. Save the figure and commit it with 
#         your code.

states_to_plot = ['Indiana', 'Alaska', 'New York', 'Wisconsin', 'Illinois']

fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(14, 18), sharex=True)
fig.suptitle('Unemployment Rate and LFD of EPU-C Over Time by State')

for i, state in enumerate(states_to_plot):
    state_data = merged_df[merged_df['state'] == state]
    
    axes[i, 0].plot(state_data['DATE'], state_data['unemp_rate'], label='Unemployment Rate', color='darkblue')
    axes[i, 0].set_title(f'{state} - Unemployment Rate')
    axes[i, 0].set_ylabel('Unemployment Rate (%)')
    axes[i, 0].legend(loc='upper left')

    axes[i, 1].plot(state_data['DATE'], state_data['LFD_EPU_Composite'], label='LFD EPU-C', color='orange')
    axes[i, 1].set_title(f'{state} - LFD EPU-C')
    axes[i, 1].set_ylabel('Log-First-Difference')
    axes[i, 1].legend(loc='upper left')

plt.xlabel('Date')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.savefig('C:/Users/Alienware/OneDrive - The University of Chicago/文档/Stats/q2_2_plot.png')
plt.show()

#    2.3: Using statsmodels, regress the unemployment rate on the LFD of EPU-C and fixed
#         effects for states. Include an intercept.
regression_data = merged_df.dropna(subset=['unemp_rate', 'LFD_EPU_Composite'])
formula = 'unemp_rate ~ LFD_EPU_Composite + C(state)'

model = smf.ols(formula, data=regression_data)

results = model.fit()

print(results.summary())

#    2.4: Print the summary of the results, and write a 1-3 line comment explaining the basic
#         interpretation of the results (e.g. coefficient, p-value, r-squared), the way you 
#         might in an abstract.

## The intercept is 4.1246, with p value < 0.05, which means that the intercept is stats significant.
## It means when no other factors, the average unempolyment rate is 4.1246 percent.
## The coefficient of the states means that the average unemployment rate varies amomng states by its value.
## The coefficient of LFD is -0.1595 meaning that one percent increase in the LFD, will results in 0.1595% decrease in Unemployment rate,
## The P-Value of LFD is 0.123>0.05 which is not stats significant.
##  Adjusted R-squared is 0.147, which means 14.7% of the unemployment rate is explained by the independent variables in the model. 