!pip instal matplotlib
!pip instal seaborn

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


df1 = pd.read_csv("/content/all_data.csv")

df1.sort_values(by="datetime").reset_index()
datetime_columns = ["datetime"]

for column in datetime_columns:
    df1[column] = pd.to_datetime(df1[column])

# Filter data
min_date = df1["datetime"].min()
max_date = df1["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df1[(df1["datetime"] >= str(start_date)) & 
                (df1["datetime"] <= str(end_date))]


# Menyiapkan berbagai dataframe
weather = create_weather(main_df)
season = create_season(main_df)
count_by_day = create_count_by_day(main_df)


# Barplot Rata-Rata Total Pengguna Bike Sharing Harian berdasarkan Kondisi Cuaca
st.subheader("Barplot Rata-Rata Total Pengguna Bike Sharing Harian berdasarkan Kondisi Cuaca")

total_users=round(weather.total_count.max(),2)
st.metric("Rata-Rata Total Pengguna Bike Sharing pada Cuaca Cerah (Clear)",value=total_users)

total_users=round(weather.total_count.min(),2)
st.metric("Rata-Rata Total Pengguna Bike Sharing pada Cuaca Hujan (Light_RainSnow)",value=total_users)  

fig, ax = plt.subplots(figsize=(7, 3))
sns.barplot(x='total_count', y='weather_condition', hue='weather_condition', data=weather, palette='viridis', dodge=False, ax=ax)
ax.set_title('Rata - Rata Total Pengguna Bike Sharing Harian berdasarkan Kondisi Cuaca')
ax.set_xlabel('Total pengguna')
ax.set_ylabel('Kondisi Cuaca')
st.pyplot(fig)

# Barplot Pengaruh Musim Terhadap Rata-Rata Jumlah Pengguna Bike-Sharing Harian
st.subheader("Barplot Pengaruh Musim Terhadap Rata-Rata Jumlah Pengguna Bike-Sharing Harian")

total_user=round(season.total_count.max(),2)
st.metric("Rata-Rata Total Pengguna Bike Sharing pada Musim Salju (Winter)",value=total_user)

total_user=round(season.total_count.min(),2)
st.metric("Rata-Rata Total Pengguna Bike Sharing pada Cuaca Hujan (Light_RainSnow)",value=total_user)  

names = ['Spring', 'Summer', 'Fall', 'Winter']
fig, ax = plt.subplots(figsize=(7,3))
sns.barplot(x=names, y=season['total_count'], ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata jumlah pengguna')
ax.set_title('Pengaruh Musim Terhadap rata-rata jumlah Pengguna Bike-Sharing Harian')
st.pyplot(fig)

# Line Plot Total Pengguna Bikes Sharing Harian
st.subheader("Line Plot Total Pengguna Bikes Sharing Harian")

total_use=round(count_by_day.total_count.max(),2)
st.metric("Total Pengguna (Casual+Registered) Terbanyak: ",value=total_use)

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# Assuming count_by_day has columns 'total_count', 'casual', and 'registered'
ax.plot(count_by_day.index, count_by_day['total_count'], label='Total Bikes Sharing')
ax.plot(count_by_day.index, count_by_day['casual'], label='Pengguna Kasual')
ax.plot(count_by_day.index, count_by_day['registered'], label='Pengguna Register')

max_x = count_by_day['total_count'].idxmax()
max_y = count_by_day['total_count'].max()
ax.annotate(f'Max: ({max_x})', xy=(max_x, max_y), xytext=(max_x, max_y + 500), arrowprops=dict(facecolor='black', shrink=0.05))

ax.set_xlabel('Waktu')
ax.set_ylabel('Total Pengguna')
ax.set_title('Total Pengguna Bikes Sharing Harian')
ax.legend()
ax.grid(True)

st.pyplot(fig)
ax.legend()
ax.grid(True)

st.pyplot(fig)

