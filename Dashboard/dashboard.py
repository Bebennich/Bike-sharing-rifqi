import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

def total_rent_by_days(df):
    rent_by_hour = df.groupby(by=["weekday"], observed=False).agg({"count": ["sum"]})
    return rent_by_hour

def analysis_rent_by_days(df):
    avg_rent = df.groupby("weekday", observed=True)["count"].mean().sort_values(ascending=False).reset_index()
    return avg_rent

def rent_by_weather(df):
    rent_by_weather = df.groupby("weather_category", observed=True)["count"].nunique().sort_values(ascending=False).reset_index()
    return rent_by_weather

dataset_bike = pd.read_csv("Dashboard/day_dataset.csv")
datetime_columns = ['dateday']
dataset_bike.sort_values(by="dateday", inplace=True)
dataset_bike.reset_index(inplace=True)

for column in datetime_columns:
    dataset_bike[column] = pd.to_datetime(dataset_bike['dateday'])

min_date = dataset_bike['dateday'].min()
max_date = dataset_bike['dateday'].max()

with st.sidebar:
    #logo company
    st.image("https://images.unsplash.com/photo-1496147433903-1e62fdb6f4be?q=80&w=1421&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    #Mengambil start date dan end date
    start_date, end_date = st.date_input(
        label='Rentang tanggal',
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )
    df_by_days = dataset_bike[(dataset_bike['dateday'] >= str(start_date)) & 
                              (dataset_bike['dateday'] <= str(end_date))]
    df_rent_by_days = total_rent_by_days(df_by_days)
    df_analysis_rent_days = analysis_rent_by_days(df_by_days)
    df_rent_by_weather = rent_by_weather(df_by_days)
    
st.header('Bike Sharing')
st.subheader('Jumlah penyewaan sepeda Mingguan')
total_rent = df_rent_by_days['count']['sum'].sum()
st.metric("Jumah penyewaan ", value=total_rent)
        
st.subheader("Hari dengan rata-rata penyewaan sepeda terbanyak")
colors = ['#A5DD9B', '#C5EBAA', '#F6F193', '#F2C18D']
plt.figure(figsize=(10, 5))

sns.barplot(
    y="avg_peminjaman", 
    x="hari",
    data=df_analysis_rent_days.sort_values(by="avg_peminjaman", ascending=False).head(3),
    palette=colors
)

st.subheader("Jumlah pelanggan berdasarkan kondisi cuaca")
colors = ['#FFBE98', '#FEECE2', '#F7DED0', '#E2BFB3']
plt.figure(figsize=(10, 5))
sns.barplot(
    y="count", 
    x="weather_category",
    data=df_rent_by_weather.sort_values(by="count", ascending=False),
    palette=colors
)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
st.pyplot(plt)