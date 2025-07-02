import streamlit as st
from datetime import datetime, timedelta
import random
from data.flights import get_flight_status, DESTINATIONS

def show():
    st.markdown("## 📊 Flight Status")
    
    # Flight status search
    st.markdown("### 🔍 Check Flight Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Search by flight number
        st.markdown("**Search by Flight Number**")
        flight_number = st.text_input("Flight Number (e.g., KQ100)", key="status_flight_number")
        search_date = st.date_input(
            "Flight Date",
            value=datetime.now().date(),
            key="status_date"
        )
        
        if st.button("Check Status", key="check_by_number"):
            if flight_number:
                display_flight_status(flight_number, search_date)
            else:
                st.error("Please enter a flight number")
    
    with col2:
        # Search by route
        st.markdown("**Search by Route**")
        origin = st.selectbox("From", list(DESTINATIONS.keys()), key="status_origin")
        destination = st.selectbox(
            "To", 
            [city for city in DESTINATIONS.keys() if city != origin],
            key="status_destination"
        )
        
        if st.button("Find Flights", key="check_by_route"):
            display_route_flights(origin, destination, search_date)
    
    # Live flight board
    st.markdown("### 🛫 Live Departures - Nairobi (NBO)")
    display_departure_board()
    
    st.markdown("### 🛬 Live Arrivals - Nairobi (NBO)")
    display_arrival_board()
    
    # Flight alerts
    st.markdown("### 🔔 Flight Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Set Up Flight Alerts**")
        alert_flight = st.text_input("Flight Number for Alerts", key="alert_flight")
        alert_email = st.text_input("Email for Notifications", key="alert_email")
        
        alert_types = st.multiselect(
            "Alert Types",
            ["Departure Delays", "Gate Changes", "Boarding Calls", "Cancellations"],
            key="alert_types"
        )
        
        if st.button("Set Alert", key="set_alert"):
            if alert_flight and alert_email:
                st.success(f"Alert set for flight {alert_flight}")
            else:
                st.error("Please enter flight number and email")
    
    with col2:
        st.markdown("**Current Alerts**")
        # Simulate existing alerts
        st.info("📱 SMS alerts enabled for KQ100")
        st.info("📧 Email alerts enabled for KQ738")
        
        if st.button("Manage All Alerts", key="manage_alerts"):
            st.info("Redirecting to alert management...")

def display_flight_status(flight_number, flight_date):
    """Display detailed flight status"""
    status_info = get_flight_status(flight_number)
    
    st.markdown(f"### Flight {flight_number} Status")
    
    # Status banner
    status_color = {
        "On Time": "🟢",
        "Delayed": "🟡", 
        "Boarding": "🔵",
        "Departed": "✈️",
        "Arrived": "🏁",
        "Cancelled": "🔴"
    }
    
    status_emoji = status_color.get(status_info['status'], "❓")
    
    st.markdown(f"## {status_emoji} {status_info['status']}")
    
    if status_info['delay_minutes'] > 0:
        st.warning(f"⏰ Delayed by {status_info['delay_minutes']} minutes")
    
    # Flight details in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Gate Information**")
        st.markdown(f"Gate: {status_info['gate']}")
        st.markdown(f"Terminal: {status_info['terminal']}")
        
        if status_info['baggage_claim']:
            st.markdown(f"Baggage Claim: {status_info['baggage_claim']}")
    
    with col2:
        st.markdown("**Timing**")
        # Simulate schedule times
        scheduled_dep = "10:45"
        scheduled_arr = "15:30"
        
        if status_info['delay_minutes'] > 0:
            actual_dep_time = calculate_delayed_time(scheduled_dep, status_info['delay_minutes'])
            actual_arr_time = calculate_delayed_time(scheduled_arr, status_info['delay_minutes'])
            
            st.markdown(f"Scheduled Departure: ~~{scheduled_dep}~~ **{actual_dep_time}**")
            st.markdown(f"Scheduled Arrival: ~~{scheduled_arr}~~ **{actual_arr_time}**")
        else:
            st.markdown(f"Departure: {scheduled_dep}")
            st.markdown(f"Arrival: {scheduled_arr}")
    
    with col3:
        st.markdown("**Updates**")
        # Simulate recent updates
        updates = [
            "Boarding in progress",
            "All passengers aboard",
            "Gate changed to A12",
            "Delayed due to weather"
        ]
        
        recent_update = random.choice(updates)
        st.info(f"Latest: {recent_update}")
        
        st.markdown("*Last updated: 2 minutes ago*")
    
    # Flight path visualization (simplified)
    st.markdown("### ✈️ Flight Progress")
    
    # Simulate flight progress
    progress = random.randint(0, 100)
    st.progress(progress / 100)
    
    if progress == 0:
        st.markdown("🛫 Preparing for departure")
    elif progress < 50:
        st.markdown("✈️ En route")
    elif progress < 100:
        st.markdown("🛬 Approaching destination")
    else:
        st.markdown("🏁 Arrived")

def display_route_flights(origin, destination, flight_date):
    """Display flights for a specific route"""
    st.markdown(f"### Flights from {origin} to {destination}")
    st.markdown(f"**Date:** {flight_date}")
    
    # Generate mock flight data for the route
    flights = [
        {"number": "KQ100", "departure": "06:30", "arrival": "10:45", "status": "On Time"},
        {"number": "KQ200", "departure": "14:20", "arrival": "18:35", "status": "Delayed"},
        {"number": "KQ300", "departure": "22:15", "arrival": "02:30+1", "status": "On Time"},
    ]
    
    for flight in flights:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"**{flight['number']}**")
        
        with col2:
            st.markdown(f"Departure: {flight['departure']}")
        
        with col3:
            st.markdown(f"Arrival: {flight['arrival']}")
        
        with col4:
            status_color = "🟢" if flight['status'] == "On Time" else "🟡"
            st.markdown(f"{status_color} {flight['status']}")

def display_departure_board():
    """Display live departure board"""
    departures = [
        {"flight": "KQ100", "destination": "London", "time": "10:45", "gate": "A12", "status": "Boarding"},
        {"flight": "KQ200", "destination": "Dubai", "time": "14:20", "gate": "B5", "status": "On Time"},
        {"flight": "KQ300", "destination": "Amsterdam", "time": "18:30", "gate": "A8", "status": "Delayed"},
        {"flight": "KQ400", "destination": "Mumbai", "time": "22:15", "gate": "C3", "status": "On Time"},
    ]
    
    # Create a table-like display
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
    
    # Headers
    with col1:
        st.markdown("**Flight**")
    with col2:
        st.markdown("**Destination**")
    with col3:
        st.markdown("**Time**")
    with col4:
        st.markdown("**Gate**")
    with col5:
        st.markdown("**Status**")
    
    st.markdown("---")
    
    # Data rows
    for dep in departures:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        
        with col1:
            st.markdown(dep["flight"])
        with col2:
            st.markdown(dep["destination"])
        with col3:
            st.markdown(dep["time"])
        with col4:
            st.markdown(dep["gate"])
        with col5:
            status_emoji = {"On Time": "🟢", "Boarding": "🔵", "Delayed": "🟡"}.get(dep["status"], "❓")
            st.markdown(f"{status_emoji} {dep['status']}")

def display_arrival_board():
    """Display live arrival board"""
    arrivals = [
        {"flight": "KQ101", "origin": "London", "time": "15:30", "gate": "A12", "status": "Arrived"},
        {"flight": "KQ201", "origin": "Dubai", "time": "19:45", "gate": "B5", "status": "On Time"},
        {"flight": "KQ301", "origin": "Amsterdam", "time": "23:15", "gate": "A8", "status": "Delayed"},
        {"flight": "KQ401", "origin": "Mumbai", "time": "05:30+1", "gate": "C3", "status": "En Route"},
    ]
    
    # Create a table-like display
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
    
    # Headers
    with col1:
        st.markdown("**Flight**")
    with col2:
        st.markdown("**Origin**")
    with col3:
        st.markdown("**Time**")
    with col4:
        st.markdown("**Gate**")
    with col5:
        st.markdown("**Status**")
    
    st.markdown("---")
    
    # Data rows
    for arr in arrivals:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
        
        with col1:
            st.markdown(arr["flight"])
        with col2:
            st.markdown(arr["origin"])
        with col3:
            st.markdown(arr["time"])
        with col4:
            st.markdown(arr["gate"])
        with col5:
            status_emoji = {"Arrived": "🏁", "On Time": "🟢", "Delayed": "🟡", "En Route": "✈️"}.get(arr["status"], "❓")
            st.markdown(f"{status_emoji} {arr['status']}")

def calculate_delayed_time(original_time, delay_minutes):
    """Calculate new time with delay"""
    hour, minute = map(int, original_time.split(':'))
    total_minutes = hour * 60 + minute + delay_minutes
    
    new_hour = (total_minutes // 60) % 24
    new_minute = total_minutes % 60
    
    return f"{new_hour:02d}:{new_minute:02d}"
