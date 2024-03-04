import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_weather(df):
    weather = df.groupby('weather_condition')['total_count'].mean().reset_index().sort_values("total_count")
    return weather

def create_season(df):
    season = df.groupby('season')['total_count'].mean().reset_index().sort_values("total_count")
    return season

def create_count_by_day(df):
    count_by_day = df.groupby('datetime')[['total_count', 'casual', 'registered']].mean()
    return count_by_day

# Load the dataset
df1 = pd.read_csv("/content/all_data.csv")

# Sort and convert datetime columns
df1.sort_values(by="datetime").reset_index()
datetime_columns = ["datetime"]

for column in datetime_columns:
    df1[column] = pd.to_datetime(df1[column])

# Filter data based on selected date range
min_date = df1["datetime"].min()
max_date = df1["datetime"].max()

with st.sidebar:
    # Add company logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Date range selection
    start_date, end_date = st.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df1[(df1["datetime"] >= str(start_date)) & (df1["datetime"] <= str(end_date))]

# Prepare dataframes
weather = create_weather(main_df)
season = create_season(main_df)
count_by_day = create_count_by_day(main_df)

# Barplot of Average Daily Bike Sharing Users by Weather Condition
st.subheader("Barplot of Average Daily Bike Sharing Users by Weather Condition")

col1, col2 = st.columns(2)

with col1:
  total_users_clear = round(weather.total_count.max(), 2)
  st.metric("Average Daily Bike Sharing Users on Clear Weather", value=total_users_clear)

  total_users_rain = round(weather.total_count.min(), 2)
  st.metric("Average Daily Bike Sharing Users on Rainy Weather", value=total_users_rain)

with col2: 
  fig, ax = plt.subplots(figsize=(7, 3))
  sns.barplot(x='total_count', y='weather_condition', hue='weather_condition', data=weather, palette='viridis', dodge=False, ax=ax)
  ax.set_title('Average Daily Bike Sharing Users by Weather Condition')
  ax.set_xlabel('Total Users')
  ax.set_ylabel('Weather Condition')
  st.pyplot(fig)

# Barplot of the Influence of Season on Average Daily Bike-Sharing Users
st.subheader("Barplot of the Influence of Season on Average Daily Bike-Sharing Users")

col1, col2 = st.columns(2)

with col2:
  total_users_winter = round(season.total_count.max(), 2)
  st.metric("Average Daily Bike Sharing Users in Winter Season", value=total_users_winter)

  total_users_summer = round(season.total_count.min(), 2)
  st.metric("Average Daily Bike Sharing Users in Summer Season", value=total_users_summer)

with col1:
  names = ['Spring', 'Summer', 'Fall', 'Winter']
  fig, ax = plt.subplots(figsize=(7, 3))
  sns.barplot(x=names, y=season['total_count'], ax=ax)
  ax.set_xlabel('Season')
  ax.set_ylabel('Average Users Count')
  ax.set_title('Influence of Season on Average Daily Bike-Sharing Users')
  st.pyplot(fig)

# Line Plot of Total Daily Bike Sharing Users
st.subheader("Line Plot of Total Daily Bike Sharing Users")

col1, col2 = st.columns(2)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))

    # Assuming count_by_day has columns 'total_count', 'casual', and 'registered'
    ax.plot(count_by_day.index, count_by_day['total_count'], label='Total Bike Sharing Users')
    ax.plot(count_by_day.index, count_by_day['casual'], label='Casual Users')
    ax.plot(count_by_day.index, count_by_day['registered'], label='Registered Users')

    max_x = count_by_day['total_count'].idxmax()
    max_y = count_by_day['total_count'].max()
    ax.annotate(f'Max: ({max_x})', xy=(max_x, max_y), xytext=(max_x, max_y + 500), arrowprops=dict(facecolor='black', shrink=0.05))

    ax.set_xlabel('Time')
    ax.set_ylabel('Total Users')
    ax.set_title('Total Daily Bike Sharing Users')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with col1:
    total_users_max = round(count_by_day.total_count.max(), 2)
    st.metric("Maximum Total Users (Casual+Registered): ", value=total_users_max)

