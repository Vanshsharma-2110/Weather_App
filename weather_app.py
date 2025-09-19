import streamlit as st
import requests

#------>step 1 : Title and page configuration<--------
st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="wide")
st.title("🌤️ Live Weather App 🌙")

api_key = "e6118b4ae96e4c10b07154347251609"

base_url = "http://api.weatherapi.com/v1/current.json"

st.sidebar.header("⚙️ Settings")

unit = st.sidebar.selectbox("Temperature Units ", ["Celsius (°C)", "Fahrenheit (°F)"])

days = st.sidebar.slider("Forecast Days", min_value=1, max_value=7, value=3)  # value is default value

show_humidity = st.sidebar.checkbox("Show Humidity", value=True)
show_wind = st.sidebar.checkbox("Show Wind Speed", value=True)

city = st.text_input("Enter City Name : ")

if st.button("Get Weather") and city:
    url = f"{base_url}/forecast.json?key={api_key}&q={city}&days={days}&aqi=no"

#------->step 2 : API Calls<--------

    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        icon = "https:" + data["current"]["condition"]["icon"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]

        st.subheader(f"{location}, {country}")
        st.image(icon, width=80)

        col1, col2 = st.columns(2)
        with col1:
            # st.write(f' 🌡️ Temperature: {temp} {unit[0]}')
            st.write(
                f" 🌡️ Temperature : {temp} °C"
                if unit == "Celsius (°C)"
                else f"Temperature: {temp * 9/5 + 32:.2f} °F"
            )
        with col2:
            st.write(f" 🌤️ Condition: {condition}")

        if show_humidity:
            st.write(f" 💧 Humidity: {humidity}%")

        if show_wind:
            st.write(f" 🌬️ Wind Speed: {wind} kph")

        st.markdown("---")

        st.header(f"📅 {days}-Day Forecast")

        forecast_day = data["forecast"]["forecastday"]

        for day in forecast_day:
            date = day["date"]
            if unit == "Celsius (°C)":
                max_temp = day["day"]["maxtemp_c"]
                min_temp = day["day"]["mintemp_c"]
                
            else:
                max_temp = day["day"]["maxtemp_f"] 
                min_temp = day["day"]["mintemp_f"] 

            condition1 = day["day"]["condition"]["text"]
            icon_url = "https:" + day["day"]["condition"]["icon"]

            col1,col2,col3,col4=st.columns([2,2,2,2])
            with col1:
                st.write(f'📅 {date}')
            with col2:
                st.image(icon_url, width=50)
            with col3:
                st.write(f'🌡️ Min: {min_temp} °C' if unit == "Celsius (°C)" else f'🌡️ Min: {min_temp * 9/5 + 32:.2f} °F')
            with col4:
                st.write(f'🌡️ Max: {max_temp} °C' if unit == "Celsius (°C)" else f'🌡️ Max: {max_temp * 9/5 + 32:.2f} °F')
            
            st.write(f'🌤️ Condition: {condition1}')
            st.markdown("---")
        
    else:
        st.error("City not found. Please check the city name and try again.")