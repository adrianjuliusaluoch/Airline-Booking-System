import streamlit as st
from datetime import datetime, timedelta
from data.flights import DESTINATIONS, search_flights
from utils.session import save_search_params, get_search_params

def show():
    st.markdown("## 🔍 Search Flights")
    
    # Get current search parameters
    params = get_search_params()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Trip type selection
        trip_type = st.selectbox(
            "Trip Type",
            ["Return", "One Way", "Multi-City"],
            index=["Return", "One Way", "Multi-City"].index(params['trip_type'])
        )
        
        # Origin and destination
        origin = st.selectbox(
            "From",
            list(DESTINATIONS.keys()),
            index=list(DESTINATIONS.keys()).index(params['origin'])
        )
        
        destination = st.selectbox(
            "To",
            [city for city in DESTINATIONS.keys() if city != origin],
            index=[city for city in DESTINATIONS.keys() if city != origin].index(params['destination']) if params['destination'] != origin else 0
        )
        
        # Swap button
        if st.button("🔄 Swap", key="swap_destinations"):
            origin, destination = destination, origin
    
    with col2:
        # Dates
        departure_date = st.date_input(
            "Departure Date",
            value=params['departure_date'],
            min_value=datetime.now().date()
        )
        
        return_date = None
        if trip_type == "Return":
            return_date = st.date_input(
                "Return Date",
                value=params['return_date'],
                min_value=departure_date
            )
    
    # Passengers
    st.markdown("### 👥 Passengers")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        adults = st.number_input("Adults (12+)", min_value=1, max_value=9, value=params['adults'])
    
    with col2:
        children = st.number_input("Children (2-11)", min_value=0, max_value=8, value=params['children'])
    
    with col3:
        infants = st.number_input("Infants (0-2)", min_value=0, max_value=4, value=params['infants'])
    
    with col4:
        travel_class = st.selectbox(
            "Class",
            ["Economy", "Business", "First"],
            index=["Economy", "Business", "First"].index(params['travel_class'])
        )
    
    # Search button
    if st.button("🔍 Search Flights", type="primary", use_container_width=True, key="search_flights_btn"):
        if origin == destination:
            st.error("Origin and destination cannot be the same!")
            return
        
        # Save search parameters
        search_params = {
            'trip_type': trip_type,
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'adults': adults,
            'children': children,
            'infants': infants,
            'travel_class': travel_class
        }
        save_search_params(search_params)
        
        # Perform search
        with st.spinner("Searching for flights..."):
            results = search_flights(
                origin, destination, departure_date, return_date,
                adults + children + infants, travel_class
            )
            st.session_state.search_results = results
        
        st.success("Flight search completed!")
        st.rerun()
    
    # Display search results
    if st.session_state.search_results:
        display_search_results()

def display_search_results():
    """Display flight search results"""
    results = st.session_state.search_results
    
    st.markdown("---")
    st.markdown("## ✈️ Available Flights")
    
    # Outbound flights
    st.markdown("### 🛫 Outbound Flights")
    for i, flight in enumerate(results['outbound']):
        display_flight_card(flight, f"outbound_{i}")
    
    # Return flights (if applicable)
    if 'return' in results:
        st.markdown("### 🛬 Return Flights")
        for i, flight in enumerate(results['return']):
            display_flight_card(flight, f"return_{i}")

def display_flight_card(flight, flight_key):
    """Display individual flight card"""
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        st.markdown(f"**{flight['flight_number']}**")
        st.markdown(f"{flight['origin']} → {flight['destination']}")
        st.markdown(f"🕐 {flight['departure_time']} - {flight['arrival_time']}")
        st.markdown(f"⏱️ {flight['duration']}")
        
        if flight['stops'] > 0:
            st.markdown(f"🔄 {flight['stops']} stop(s)")
        else:
            st.markdown("✈️ Direct flight")
    
    with col2:
        st.markdown("**Aircraft**")
        st.markdown(flight['aircraft'])
        st.image(flight['aircraft_image'], width=150)
    
    with col3:
        st.markdown("**Amenities**")
        if flight['meal_service']:
            st.markdown("🍽️ Meal service")
        if flight['wifi_available']:
            st.markdown("📶 WiFi available")
        if flight['entertainment']:
            st.markdown("🎬 Entertainment")
    
    with col4:
        travel_class = get_search_params()['travel_class']
        price = flight['prices'][travel_class]
        seats_available = flight['seats_available'][travel_class]
        
        st.markdown(f"**${price}**")
        st.markdown(f"per person")
        st.markdown(f"💺 {seats_available} seats left")
        
        if st.button(f"Select Flight", key=f"select_{flight_key}"):
            st.session_state.selected_flights[flight_key.split('_')[0]] = flight
            st.success(f"Flight {flight['flight_number']} selected!")
            st.rerun()
    
    st.markdown("---")
