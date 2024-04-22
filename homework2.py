# PPHA 30537
# Spring 2024
# Homework 2

# YOUR NAME HERE: Kunquan Wang
# YOUR GITHUB USER NAME HERE: YOLELIN

# Due date: Sunday April 21st before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.

# PART 1: Macro Data Exploration

# Question 1.1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.
import pandas as pd
file_path = r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\NST-EST2022-ALLDATA.csv'

NST = pd.read_csv(file_path)

# Question 1.2: Your data only includes fips codes for states (STATE).  Use 
# the us library to crosswalk fips codes to state abbreviations.  Drop the
# fips codes.
import us

NST['STATE_ABBR'] = NST['STATE'].apply(lambda x: us.states.lookup(str(x).zfill(2)).abbr if us.states.lookup(str(x).zfill(2)) is not None else None)

NST_cleaned = NST.drop('STATE', axis=1)

# Question 1.3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them.  Do not 
# create plots or use groupby; we will do that in future homeworks.  
# Show the relevant exploration output with print() statements.
print(NST_cleaned.head())
#describe some features of the numbers in the dataset.
print(NST_cleaned.describe())

# Question 1.4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.
state_data = NST_cleaned[NST_cleaned['SUMLEV'] == 40]

NST_subset = state_data[['STATE_ABBR', 'POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']]

print(NST_subset)

# Question 1.5: Show only the 10 largest states by 2021 population estimates,
# in decending order.
top_states_by_population = NST_subset.sort_values('POPESTIMATE2021', ascending=False)

top_10_states = top_states_by_population.head(10)

print("Top 10 in 2021 estimation:")
print(top_10_states[['STATE_ABBR', 'POPESTIMATE2021']])

# Question 1.6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?
NST_subset['POPCHANGE'] = NST_subset['POPESTIMATE2022'] - NST_subset['POPESTIMATE2020']
print("Gained: ",(NST_subset['POPCHANGE'] > 0).sum())
print("Lost: ",(NST_subset['POPCHANGE'] < 0).sum())

# Question 1.7: Show all the states that had an estimated change in either
# direction of smaller than 1000 people. 
less_than_1000 = NST_subset[abs(NST_subset['POPCHANGE']) < 1000]
print(less_than_1000[['STATE_ABBR', 'POPCHANGE']])

# Question 1.8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.

std_dev = NST_subset['POPCHANGE'].std()
significant_change_states = NST_subset[abs(NST_subset['POPCHANGE']) > std_dev]

significant_change_states_sorted = significant_change_states.assign(abs_popchange=abs(significant_change_states['POPCHANGE']))
significant_change_states_sorted = significant_change_states_sorted.sort_values('abs_popchange', ascending=False)

print("States with population change greater than one standard deviation:")
print(significant_change_states_sorted[['STATE_ABBR', 'POPCHANGE']])

#PART 2: Data manipulation

# Question 2.1: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
# Explain in a brief (1-2 line) comment.

## We drop the POPCHANGE column because does not fit the format of years.
print(NST_subset.head())
print(NST_subset.columns)
print(NST_subset.shape)

##NST_subset.drop(['POPCHANGE'], axis=1, inplace=True)

# Having problems manipulate the data here, ValueError: Length mismatch: Expected axis has 156 elements, new values have 153 elements.
## NST_long = pd.wide_to_long(NST_subset, stubnames='POPESTIMATE', i='STATE_ABBR', j='year', suffix='\d+').reset_index()
## print(NST_long.head())

# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).
NST_subset.drop('POPCHANGE', axis=1, inplace=True)

melted_data = pd.melt(NST_subset, id_vars=['STATE_ABBR'], var_name='year', value_name='POPESTIMATE')

melted_data['year'] = melted_data['year'].str.extract('(\d+)')

print(melted_data.head())

# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.
visits_df = pd.read_excel(r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\state-visits.xlsx')
print(visits_df.head())
print(NST_subset.head())

## rename the column in visits_df
visits_df.rename(columns={'STATE': 'STATE_ABBR'}, inplace=True)

merged_df = pd.merge(NST_subset, visits_df[['STATE_ABBR', 'VISITED']], on='STATE_ABBR', how='inner')

missing_in_merged = NST_subset[~NST_subset['STATE_ABBR'].isin(merged_df['STATE_ABBR'])]

missing_in_visits = visits_df[~visits_df['STATE_ABBR'].isin(merged_df['STATE_ABBR'])]

print("Merged DataFrame:\n", merged_df)
print("\nStates in original NST_subset not in merged DataFrame:\n", missing_in_merged)
print("\nStates in visits_df not in merged DataFrame:\n", missing_in_visits)

# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.
policy_uncertainty = pd.read_excel(r'C:\Users\Alienware\OneDrive - The University of Chicago\文档\Stats\policy_uncertainty.xlsx')
print(policy_uncertainty.head())
mean_epu_df = policy_uncertainty.groupby(['state', 'year'])['EPU_Composite'].agg(['mean']).reset_index()
mean_epu_df.columns = ['state', 'year', 'Mean_EPU_Composite']

# Merge the mean values back with the original data
epu_df = policy_uncertainty.merge(mean_epu_df, on=['state', 'year'])

# Rename the columns for clarity
epu_df.columns = ['State', 'Year', 'Month', 'EPU_National', 'EPU_State', 'EPU_Composite', 'Mean_EPU_Composite']

# Print the resulting DataFrame
print(epu_df.head())
# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 
filtered_data = policy_uncertainty[policy_uncertainty['year'].isin([2020, 2021, 2022])]

wide_format_df = filtered_data.pivot_table(index='state', columns='year', values='EPU_Composite', aggfunc='mean')

wide_format_df.columns = [f'EPU_Composite_{col}' for col in wide_format_df.columns]

wide_format_df.reset_index(inplace=True)

print(wide_format_df)
print(merged_df)
# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.
state_map = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
# Replace full state names with abbreviations in 'wide_format_df'
wide_format_df['state'] = wide_format_df['state'].map(state_map)

final_df = pd.merge(merged_df, wide_format_df, left_on='STATE_ABBR', right_on='state', how='inner')

print("First few rows of the final merged DataFrame:")
print(final_df.head())

# Check if any states are missing after the merge
states_missing_in_merged = merged_df[~merged_df['STATE_ABBR'].isin(final_df['STATE_ABBR'])]
print("States missing after merge:", states_missing_in_merged['STATE_ABBR'].unique())

# Question 2.7: Using groupby on the VISITED column in the dataframe resulting 
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?
print(final_df.head())
##(a)
smallest_state = final_df.nsmallest(1, 'POPESTIMATE2022')
print("Smallest state visited:\n", smallest_state[['STATE_ABBR', 'POPESTIMATE2022']])

##(b)
largest_states = final_df.nlargest(3, 'POPESTIMATE2022')
print("Three largest states visited:\n", largest_states[['STATE_ABBR', 'POPESTIMATE2022']])

##(c)
average_epu = final_df['EPU_Composite_2022'].mean()
print("Average EPU-C 2022 for visited states:", average_epu)
# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.
print(epu_df)
def zscore(x):
    return (x - x.mean()) / x.std()
epu_df['EPU_C_zscore'] = epu_df.groupby('State')['EPU_Composite'].transform(zscore)

print(epu_df.head())