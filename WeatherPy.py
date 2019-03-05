
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=2000)
lngs = np.random.uniform(low=-180.000, high=180.000, size=2000)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it's being processed (with the city number and city name).
# 

# In[3]:


# Created a function that will pull desired data from the weather API
def check_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?"
    units = "metric"
    query_url = f"{url}appid={api_key}&units={units}&q={city}"
    response = requests.get(query_url)
    out_json = response.json()
   
    try:
        print(f"Processing record for {city}.")
        return {
            "City": city,
            "Cloudiness": out_json['clouds']['all'],
            "Country": out_json['sys']['country'],
            "Date": out_json['dt'],
            "Humidity": out_json['main']['humidity'],
            "Lat": out_json['coord']['lat'],
            "Lng": out_json['coord']['lon'],
            "Max Temp": out_json['main']['temp_max'],
            "Wind Speed": out_json['wind']['speed']
        }
       
    
    except (KeyError, IndexError):
        print(f"{city} not found...skipping...")
        return {
            "City": city,
            "Cloudiness": np.nan,
            "Country": np.nan,
            "Date": np.nan,
            "Humidity": np.nan,
            "Lat": np.nan,
            "Lng": np.nan,
            "Max Temp": np.nan,
            "Wind Speed": np.nan
        }
        


# In[4]:


# Retrieve data for the cities in cities list and make a list of dictionaries
all_cities_results = [check_weather(city) for city in cities]
all_cities_results


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[5]:


# Convert data to a dataframe
city_weather_df = pd.DataFrame(all_cities_results)
city_weather_df.head()


# In[6]:


# Check to see if we have more than 500 data points
city_weather_df.count()


# In[7]:


# Reformat Date column
city_weather_df['Date'] = city_weather_df['Date'].apply(lambda x: '{:.0f}'.format(x))
city_weather_df.head()


# In[8]:


# Save dataframe to csv file
city_weather_df.to_csv('cities_weather.csv')


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[9]:


# Generate scatter plot for latitude vs max temp
latitudes = city_weather_df['Lat']
maximum_temps = city_weather_df['Max Temp']
plt.scatter(latitudes, maximum_temps, edgecolor='black')
plt.grid()
plt.xlabel('Latitude')
plt.ylabel('Max Temperature (F)')
plt.title('City Latitude vs. Max Temperature (03/05/19)')
plt.savefig('latitude_max_temp.png')
plt.show()


# #### Latitude vs. Humidity Plot

# In[10]:


# Generate scatter plot for latitude vs humidity
latitudes = city_weather_df['Lat']
humidity = city_weather_df['Humidity']
plt.scatter(latitudes, humidity, edgecolor='black')
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.yticks(np.arange(0, 400, step=50))
plt.title('City Latitude vs. Humidity (03/05/19)')


# In[11]:


# After taking a look at the initial plot, there seemed to be an outlier point
# Identify the outlier
humidity_outlier = city_weather_df.loc[city_weather_df['Humidity'] > 100]
humidity_outlier


# In[12]:


# Make new dataframe that has cities only with humidity <= 100%
city_weather_df2 = city_weather_df[city_weather_df['Humidity'] <= 100]
city_weather_df2.loc[city_weather_df2['Humidity'] > 100]


# In[13]:


# Replot the data for new dataframe
latitudes2 = city_weather_df2['Lat']
humidity = city_weather_df2['Humidity']
plt.scatter(latitudes2, humidity, edgecolor='black')
plt.grid()
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.yticks(np.arange(0, 110, step=10))
plt.title('City Latitude vs. Humidity (03/05/19)')
plt.savefig('latitude_humidity.png')
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[14]:


# Generate plot for latitude vs cloudiness
latitudes = city_weather_df['Lat']
cloudiness = city_weather_df['Cloudiness']
plt.scatter(latitudes, cloudiness, edgecolor='black')
plt.grid()
plt.xlabel('Latitude')
plt.ylabel('Cloudiness (%)')
plt.yticks(np.arange(0, 110, step=10))
plt.title('City Latitude vs. Cloudiness (03/05/19)')
plt.savefig('latitude_cloudiness.png')
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[15]:


# Generate plot for latitude vs cloudiness
latitudes = city_weather_df['Lat']
wind_speed = city_weather_df['Wind Speed']
plt.scatter(latitudes, wind_speed, edgecolor='black')
plt.grid()
plt.xlabel('Latitude')
plt.ylabel('Wind Speed (mph)')
plt.yticks(np.arange(0, 25, step=5))
plt.title('City Latitude vs. Wind Speed (03/05/19)')
plt.savefig('latitude_wind_speed.png')
plt.show()

