import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from pages import flight_search, booking, seat_selection, passenger_info, confirmation, flight_status, check_in, manage_booking
from utils.session import initialize_session

# Page configuration
st.set_page_config(
    page_title="Airline Airways - Book Your Flight",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
initialize_session()

# Custom CSS for Kenya Airways styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}

.feature-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-left: 4px solid #1E40AF;
}

.destination-card {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.price-tag {
    background: #DC2626;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: bold;
}

.promo-banner {
    background: linear-gradient(45deg, #DC2626, #EF4444);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🇰🇪 Kenya Airways</h1>
    <h3>The Pride of Africa</h3>
    <p>Experience world-class service and comfort on your journey</p>
</div>
""", unsafe_allow_html=True)

# Navigation
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🔍 Search Flights", 
    "✈️ Book Flight", 
    "💺 Select Seats", 
    "👤 Passenger Info", 
    "✅ Confirmation", 
    "📊 Flight Status", 
    "🎫 Check-In", 
    "📝 Manage Booking"
])

with tab1:
    flight_search.show()

with tab2:
    booking.show()

with tab3:
    seat_selection.show()

with tab4:
    passenger_info.show()

with tab5:
    confirmation.show()

with tab6:
    flight_status.show()

with tab7:
    check_in.show()

with tab8:
    manage_booking.show()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6B7280;">
    <p>© 2025 Kenya Airways. The Pride of Africa. All rights reserved.</p>
    <p>Experience the warmth of African hospitality at 35,000 feet</p>
</div>
""", unsafe_allow_html=True)
