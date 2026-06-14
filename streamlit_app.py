import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --- Page configuration ---
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ Weather Dashboard")

# --- Load data from SQLite database with caching ---
@st.cache_data
def load_data():
    conn = sqlite3.connect('weather.db')
    query = "SELECT * FROM weather_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Ensure temperature is numeric and drop rows with missing values
    df['Temp_F'] = pd.to_numeric(df['Temperature'].str.replace(' °F', ''), errors='coerce')
    df = df.dropna(subset=['Temp_F', 'City', 'Condition', 'Day & Time'])
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filter Options")
selected_city = st.sidebar.selectbox(
    "Select a city",
    options=sorted(df['City'].unique())
)

# Filter data based on selection
filtered_df = df[df['City'] == selected_city]

# --- Metrics row ---
st.header(f"📌 Current Weather in {selected_city}")
col1, col2, col3 = st.columns(3)
if not filtered_df.empty:
    col1.metric("Temperature", f"{filtered_df.iloc[0]['Temp_F']:.1f}°F")
    col2.metric("Condition", filtered_df.iloc[0]['Condition'])
    col3.metric("Day & Time", filtered_df.iloc[0]['Day & Time'])
else:
    st.warning("No data available for this city.")

# --- Chart 1: Temperature distribution (histogram) ---
st.header("📈 Distribution of Temperatures")
fig1 = px.histogram(df, x='Temp_F', nbins=20, title="Temperature Frequency",
                    labels={'Temp_F': 'Temperature (°F)'})
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Temperature by city (bar chart) ---
st.header("🌡️ Average Temperature by City")
city_avg = df.groupby('City')['Temp_F'].mean().reset_index()
city_avg = city_avg.sort_values('Temp_F', ascending=False)
fig2 = px.bar(city_avg, x='City', y='Temp_F', color='Temp_F',
              title="Average Temperature per City",
              labels={'Temp_F': 'Avg Temperature (°F)'})
st.plotly_chart(fig2, use_container_width=True)

# --- Chart 3: Temperature trend for selected city (line chart) ---
st.header(f"📉 Temperature Trend for {selected_city}")
if len(filtered_df) > 1:
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df['Index'] = filtered_df.index
    fig3 = px.line(filtered_df, x='Index', y='Temp_F',
                   title=f"Temperature readings for {selected_city}",
                   labels={'Index': 'Observation order', 'Temp_F': 'Temperature (°F)'},
                   markers=True)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Not enough data points to show a trend line.")