import quandl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from tqdm import tqdm

# API Key
quandl.ApiConfig.api_key = "[ENTER API KEY]"

# Collect data
table = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH')

# Create region ID set
regions = set(table['region_id'])

# Create region dictionary
regional_data = {}

# Create dictionary for median, mean, std
stat_measures  = {}

# Loop over regions and extract data
for region in regions:
    regional_data[region] = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id=region)
    
    # Create price plots for each region
    fig, graph = plt.subplots()
    half_year_locator = mdates.MonthLocator(interval=12)
    graph.xaxis.set_major_locator(half_year_locator)
    graph.xaxis.set_tick_params(rotation=90)
    graph.plot(regional_data[region].date, regional_data[region].value)
    graph.set_xlabel('Date')
    graph.set_ylabel('Value')
    graph.set_title(f'Zillow Real Estate Plot (Region ID: {region})')
    plt.show()
    
    # Calculate mean, median, and standard deviation
    mean_value = regional_data[region].value.mean()
    median_value = regional_data[region].value.median()
    std_deviation = regional_data[region].value.std()
    
    # Add information to stat_measures dict
    stat_measures[region] = {
        'mean': mean_value,
        'median': median_value,
        'std_deviation': std_deviation
    }

    # Create labels for x-axis
    x_labels = ['Mean', 'Median', 'Std_deviation']
    x_positions = range(len(x_labels))

    # Get y-values
    y_values = [mean_value, median_value, std_deviation]

    # Create bar chart
    fig, bar_graph = plt.subplots()
    bar_graph.bar(x_positions, y_values)
    bar_graph.set_xticks(x_positions)
    bar_graph.set_xticklabels(x_labels)
    bar_graph.set_xlabel('Statistical Measures')
    bar_graph.set_ylabel('Value')
    bar_graph.set_title(f'Statistical Measures (Region ID: {region})')


# Create variables
max_mean = 0
max_median = 0
max_mean_region = ''
max_median_region = ''

# Extract the highest value from stat_measures
for region, stats in stat_measures.items():
    
    # Initialize variables
    region_mean = stats['mean']
    region_median = stats['median']
    region_name = region
    
    # Create conditional logic
    if region_mean > max_mean:
        max_mean = region_mean
        max_mean_region = region_name
        
    if region_median > max_median:
        max_median = region_median
        max_median_region = region_name
        
# Create dictionary for max values
highest_vals = {
    'highest_mean': {'region': max_mean_region, 'mean_val': max_mean},
    'highest_median': {'region': max_median_region, 'median_val': max_median}
    }

# Print out the values
for key, inner_dict in highest_vals.items():
    print("Key:", key)
    print("Inner Dictionary:", inner_dict)
    print("Region:", inner_dict['region'])
    if 'mean_val' in inner_dict:
        print("Mean Value:", inner_dict['mean_val'])
    if 'median_val' in inner_dict:
        print("Median Value:", inner_dict['median_val'])
    print("-------------------")
    
# Find data for North East
#---------------------------------------------#

# Extract the regional data
region_data = quandl.get_table('ZILLOW/REGIONS', paginate=True)

# Find regions only in North East
ne_states = ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']

# Extract regional data for these states
ne_regions = []

for index, row in region_data.iterrows():
    region_abbreviation = row['region']
    
    if any(state in region_abbreviation for state in ne_states):
        ne_regions.append(row['region_id'])
        
# Retrieve the values for the regions
#---------------------------------------------#

# NE housing data
ne_housing_data = {}

for region in tqdm(ne_regions, total = len(ne_regions)):
    ne_housing_data[region] = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id=region)


# broke off operation for taking too long

# Calculate average for every time period
#---------------------------------------------#

# Create a list of dataframes for each region's data
dataframes = []
for region, data in ne_housing_data.items():
    dataframes.append(data)

# Concatenate dataframes into a single dataframe
combined_data = pd.concat(dataframes)

# Group by 'date' and calculate the mean for each group
averages = combined_data.groupby('date')['value'].mean()

# Create a DataFrame from the calculated averages
average_df = pd.DataFrame({'date': averages.index, 'average_value': averages.values})

# Create plot of average prices for NE region

# Extract date and value
date = average_df['date']
value = average_df['average_value']

# Create line graph
fig, graph = plt.subplots()
year_locator = mdates.MonthLocator(interval=12)
graph.xaxis.set_major_locator(year_locator)
graph.xaxis.set_tick_params(rotation=90)
graph.plot(date, value)
graph.set_xlabel('Date')
graph.set_ylabel('Value')
graph.set_title('Average Single Family Home Price Chart for NE Region (USA)')


# Evaluate Trend from 2018-2023 when interest rates were slashed by FED during COVID

# Convert the 'date' column to datetime format
#average_df['date'] = pd.to_datetime(average_df['date'])

# Filter data for the desired date range
start_date = '2018-01-01'

# Set to latest date
end_date = average_df['date'].max()

filtered_data = average_df[(average_df['date'] >= start_date) & (average_df['date'] <= end_date)]

# Create a line plot
plt.figure(figsize=(10, 5))
plt.plot(filtered_data['date'], filtered_data['average_value'])
plt.xlabel('Date')
plt.ylabel('Average Value')
plt.title('Average Value Trend (2018 - 2023)')
plt.xticks(rotation=45)
plt.tight_layout()













