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

# Custom Modern CSS with Inter Font
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    color: #111827;
}

.main-header {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-card {
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    margin: 1rem 0;
    border-left: 4px solid #1E40AF;
}

.destination-card {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    margin: 1rem 0;
    transition: transform 0.2s ease-in-out;
}

.destination-card:hover {
    transform: translateY(-4px);
}

.price-tag {
    background: #DC2626;
    color: white;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.95rem;
}

.promo-banner {
    background: linear-gradient(45deg, #DC2626, #EF4444);
    color: white;
    padding: 1rem 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 1.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

# Navigation Tabs
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

with tab1: flight_search.show()
with tab2: booking.show()
with tab3: seat_selection.show()
with tab4: passenger_info.show()
with tab5: confirmation.show()
with tab6: flight_status.show()
with tab7: check_in.show()
with tab8: manage_booking.show()

# Promo Banner
st.markdown("""
<div class="promo-banner">
    <h3>🎉 Hot Deal Sale - Limited Time Offer!</h3>
    <p>Save up to 30% on selected destinations. Book now!</p>
</div>
""", unsafe_allow_html=True)

# Popular Destinations
st.markdown("## 🌍 Popular Destinations")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="destination-card">
        <img src="https://pixabay.com/get/gbd0494f96fcace4d518162f5508f26bafaf5309a6ee1a73c2f45db1ecd880d89456bb705dc9f4f41352b319bffcb8935ad2e3bb6982ecbf6cd2911fc4fb888df_1280.jpg" width="100%" style="height: 150px; object-fit: cover;">
        <div style="padding: 1rem;">
            <h4>London</h4>
            <p>From <span class="price-tag">$945</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="destination-card">
        <img src="https://pixabay.com/get/ga36a6591b71252cf2cada611b9d2c687a2d27e5d268b6d96fcffbaa6165db4cff64a1135534ff2332ec6f01c57b6fa5f51426665a07eb2db53eee89c0a1a4ff7_1280.jpg" width="100%" style="height: 150px; object-fit: cover;">
        <div style="padding: 1rem;">
            <h4>Dubai</h4>
            <p>From <span class="price-tag">$650</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="destination-card">
        <img src="https://pixabay.com/get/gfe9e8f9afb736a9ca5ff51a1d59263d2e437f8083d126a52d8db9abaafe1ad2642dc5ab200b348c8f87a0355ff1d0aa1e4fecd48a29e9d64e20df0dd748608cc_1280.jpg" width="100%" style="height: 150px; object-fit: cover;">
        <div style="padding: 1rem;">
            <h4>Amsterdam</h4>
            <p>From <span class="price-tag">$890</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="destination-card">
        <img src="https://pixabay.com/get/g6e3d46044a29449efcc58cbe6037c511d4f86e9844e898aae72c13a3bc80c6ed91e8a8b2df2144c3160086818fe9cf357588b2b4d15f9fcadd2d52f43ac66ca3_1280.jpg" width="100%" style="height: 150px; object-fit: cover;">
        <div style="padding: 1rem;">
            <h4>Paris</h4>
            <p>From <span class="price-tag">$920</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Our Services
st.markdown("## 🛎️ Our Services")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🏆 Asante Rewards</h4>
        <p>Earn points on every flight and enjoy exclusive benefits as a loyalty member.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🌴 KQ Holidays</h4>
        <p>Complete holiday packages with flights, hotels, and experiences.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🛒 Duty Free</h4>
        <p>Shop the latest products and enjoy tax-free shopping on board.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6B7280;">
    <p>© 2025 Kenya Airways. The Pride of Africa. All rights reserved.</p>
    <p>Experience the warmth of African hospitality at 35,000 feet</p>
</div>
""", unsafe_allow_html=True)
