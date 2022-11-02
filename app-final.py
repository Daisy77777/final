import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')
sns.set(color_codes=True)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

st.title('Hotel Booking Demand')
st.write('Created by Qiqi Yu and Yi Shi (team 25)')

df_hotel = pd.read_csv('hotel_bookings.csv')
df_hotel = df_hotel.sample(5000)

hotel_filter = st.sidebar.multiselect(
     'Choose the hotel',
     df_hotel.hotel.unique(),
     df_hotel.hotel.unique(),
)
df_hotel = df_hotel[df_hotel.hotel.isin(hotel_filter)]

st.subheader('Q1: Comparison of arrivals at two hotels')
fig, ax=plt.subplots(figsize=(15, 8))
df_hotel['hotel'].value_counts().plot.pie(autopct='%1.1f%%', colors=['pink', 'lightblue'])
st.pyplot(fig)

plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
sns.countplot(data=df_hotel, x='arrival_date_year', hue='hotel', palette='cool')
plt.title("Arrivals per year in two hotels ",fontweight="bold", size=20)
plt.subplot(1, 2, 2)
sns.countplot(data=df_hotel, x='arrival_date_month', hue='hotel', palette='cool', order=months)
plt.title("Arrivals per month in two hotels ",fontweight="bold", size=20)
plt.xticks(rotation=60)
st.pyplot(plt)

st.subheader('Q2: The impact of weekdays and weekends on the number of bookings and cancellations')
st.write('0 means not canceled, 1 means canceled')
fig, ax = plt.subplots(figsize=(15, 8))
df_hotel['is_canceled'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%', colors=['pink', 'lightblue'])
st.pyplot(fig)

plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
sns.countplot(x='stays_in_week_nights',hue='hotel', data=df_hotel, palette='Greens')
plt.title("Number of stays on weekday nights",fontweight="bold", size=20)
plt.subplot(1, 2, 2)
sns.countplot(data = df_hotel, x='stays_in_week_nights', hue='is_canceled', palette='Reds')
plt.title('Canceled vs. Not Canceled in weekdays',fontweight="bold", size=20)
st.pyplot(plt)

plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
sns.countplot(x='stays_in_weekend_nights',hue='hotel', data=df_hotel, palette='Blues')
plt.title("Number of stays on weekend nights",fontweight="bold", size=20)
plt.subplot(1, 2, 2)
sns.countplot(data=df_hotel, x = 'stays_in_weekend_nights', hue='is_canceled', palette='Purples')
plt.title('Canceled vs. Not Canceled on the weekend',fontweight="bold", size=20)
st.pyplot(plt)

price_slider = st.sidebar.slider('Minimal Average Daily Rate', 0, 250, 0)
df1 = df_hotel[df_hotel.adr >= price_slider] 

st.subheader('Q3: The impact of the arrival number on the price')
plt.figure(figsize=(15, 8))
sns.countplot(data=df1, x='arrival_date_month', order=months)
plt.title('Arrivals per month in two hotels', fontweight="bold", size=20)
plt.xticks(rotation=30)
st.pyplot(plt)

prices_mothly = df_hotel[['hotel', 'arrival_date_month', 'adr']].sort_values('arrival_date_month')
prices_mothly['arrival_date_month'] = pd.Categorical(prices_mothly["arrival_date_month"], categories=months, ordered=True)
plt.figure(figsize=(15, 8))
sns.lineplot(x='arrival_date_month', y='adr', hue='hotel', data=prices_mothly, palette='husl')
plt.ylabel('Average daily price')
plt.xlabel('Months')
plt.xticks(rotation=30)
plt.title('Average daily rate by months')
st.pyplot(plt)