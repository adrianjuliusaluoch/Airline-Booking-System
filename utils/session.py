import streamlit as st
from datetime import datetime, timedelta

def initialize_session():
    """Initialize session state variables"""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    
    if 'selected_flights' not in st.session_state:
        st.session_state.selected_flights = {}
    
    if 'passengers' not in st.session_state:
        st.session_state.passengers = []
    
    if 'booking_data' not in st.session_state:
        st.session_state.booking_data = {}
    
    if 'current_booking' not in st.session_state:
        st.session_state.current_booking = None
    
    if 'seat_selections' not in st.session_state:
        st.session_state.seat_selections = {}
    
    if 'search_params' not in st.session_state:
        st.session_state.search_params = {
            'origin': 'Nairobi',
            'destination': 'London',
            'departure_date': datetime.now().date() + timedelta(days=7),
            'return_date': datetime.now().date() + timedelta(days=14),
            'trip_type': 'Return',
            'adults': 1,
            'children': 0,
            'infants': 0,
            'travel_class': 'Economy'
        }

def reset_booking_flow():
    """Reset booking flow session state"""
    st.session_state.search_results = None
    st.session_state.selected_flights = {}
    st.session_state.passengers = []
    st.session_state.booking_data = {}
    st.session_state.seat_selections = {}

def get_total_passengers():
    """Get total number of passengers"""
    return (st.session_state.search_params['adults'] + 
            st.session_state.search_params['children'] + 
            st.session_state.search_params['infants'])

def save_search_params(params):
    """Save search parameters to session"""
    st.session_state.search_params.update(params)

def get_search_params():
    """Get current search parameters"""
    return st.session_state.search_params
