import streamlit as st
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import joblib

# Wczytaj model
model_xgboost = joblib.load('model.json')

# Mappings
starting_airport_mapping = {'ATL': 0, 'BOS': 1, 'CLT': 2, 'DEN': 3, 'DFW': 4, 'DTW': 5, 'EWR': 6, 'IAD': 7, 'JFK': 8, 'LAX': 9, 'LGA': 10, 'MIA': 11, 'OAK': 12, 'ORD': 13, 'PHL': 14, 'SFO': 15}
destination_airport_mapping = {'BOS': 0, 'CLT': 1, 'DEN': 2, 'DFW': 3, 'DTW': 4, 'EWR': 5, 'IAD': 6, 'JFK': 7, 'LAX': 8, 'LGA': 9, 'MIA': 10, 'ORD': 11, 'PHL': 12, 'SFO': 13, 'ATL': 14, 'OAK': 15}
airline_name_mapping = {'Delta': 0, 'JetBlue Airways': 1, 'American Airlines': 2, 'Frontier Airlines': 3, 'United': 4, 'Spirit Airlines': 5, 'Alaska Airlines': 6}

# Tytuł aplikacji
st.title('Prognoza Ceny Biletu Lotniczego 🌈')

# Wybór lotniska początkowego
starting_airport = st.selectbox('Lotnisko Początkowe 💖', list(starting_airport_mapping.keys()))
starting_airport_code = starting_airport_mapping[starting_airport]

# Wybór lotniska docelowego
destination_airport = st.selectbox('Lotnisko Docelowe 💛', list(destination_airport_mapping.keys()))
destination_airport_code = destination_airport_mapping[destination_airport]

# Wybór linii lotniczej
airline = st.selectbox('Linia Lotnicza 💚', list(airline_name_mapping.keys()))
airline_code = airline_name_mapping[airline]

# Wybór liczby dni do lotu
days_between_search_and_flight = st.slider('Liczba Dni do Lotu 💜', min_value=1, max_value=18, value=10)

# Wybór klasy ekonomicznej
is_basic_economy = st.checkbox('Klasa Ekonomiczna', value=False)

# Przycisk do wyszukiwania
if st.button('Szukaj'):
    # Przygotowanie danych wejściowych
    input_data = {
        'startingAirport': [starting_airport_code],
        'destinationAirport': [destination_airport_code],
        'isBasicEconomy': [is_basic_economy],
        'segmentsAirlineName': [airline_code],
        'daysBetweenSearchAndFlight': [days_between_search_and_flight]
    }
    input_df = pd.DataFrame(input_data)

    # Predykcja ceny
    predicted_fare = model_xgboost.predict(input_df)
    lower_bound = round(predicted_fare[0] * 0.8)
    upper_bound = round(predicted_fare[0] * 1.2)
    
    # Wyświetlanie przewidywanego zakresu cen bez miejsc po przecinku
    st.markdown(f"<div style='text-align: center; font-size: 24px;'>Przewidywany Zakres Cen dla Wyszukiwanego Połączenia:</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 36px; font-weight: bold;'>${lower_bound} - ${upper_bound}</div>", unsafe_allow_html=True)