import streamlit as st
from datetime import datetime, timedelta
import random

def show():
    st.markdown("## 🎫 Online Check-In")
    
    # Check-in availability notice
    st.info("✈️ Online check-in is available 24 hours before departure time")
    
    # Check-in form
    st.markdown("### 📝 Check-In Form")
    
    col1, col2 = st.columns(2)
    
    with col1:
        booking_ref = st.text_input(
            "Booking Reference*",
            placeholder="Enter your booking reference (e.g., KQ123456)",
            key="checkin_booking_ref"
        )
        
        last_name = st.text_input(
            "Last Name*",
            placeholder="Enter passenger's last name",
            key="checkin_last_name"
        )
    
    with col2:
        flight_date = st.date_input(
            "Flight Date*",
            value=datetime.now().date() + timedelta(days=1),
            min_value=datetime.now().date(),
            key="checkin_date"
        )
        
        seat_preference = st.selectbox(
            "Seat Preference",
            ["No Preference", "Window", "Aisle", "Front of Aircraft", "Extra Legroom"],
            key="checkin_seat_pref"
        )
    
    # Find booking button
    if st.button("Find My Booking", type="primary", use_container_width=True, key="find_booking_checkin"):
        if booking_ref and last_name:
            # Simulate booking lookup
            with st.spinner("Looking up your booking..."):
                booking_found = simulate_booking_lookup(booking_ref, last_name)
            
            if booking_found:
                st.session_state.checkin_booking = booking_found
                st.success("✅ Booking found! Please complete your check-in below.")
                st.rerun()
            else:
                st.error("❌ Booking not found. Please check your booking reference and last name.")
        else:
            st.error("Please enter both booking reference and last name.")
    
    # Display booking details if found
    if st.session_state.get('checkin_booking'):
        display_checkin_details()

def simulate_booking_lookup(booking_ref, last_name):
    """Simulate booking lookup"""
    # In a real system, this would query the booking database
    if len(booking_ref) >= 6 and len(last_name) >= 2:
        return {
            "booking_reference": booking_ref,
            "passenger_name": f"John {last_name}",
            "flight_number": f"KQ{random.randint(100, 999)}",
            "route": "Nairobi → London",
            "departure_date": "2025-07-10",
            "departure_time": "10:45",
            "arrival_time": "15:30",
            "seat": "23A",
            "gate": "A12",
            "terminal": "1A",
            "boarding_time": "10:15",
            "class": "Economy",
            "status": "Confirmed",
            "baggage_allowance": "23kg",
            "meal_preference": "Standard",
            "checkin_available": True
        }
    return None

def display_checkin_details():
    """Display check-in details and options"""
    booking = st.session_state.checkin_booking
    
    st.markdown("### ✈️ Flight Details")
    
    # Flight information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Flight:** {booking['flight_number']}")
        st.markdown(f"**Route:** {booking['route']}")
        st.markdown(f"**Date:** {booking['departure_date']}")
        st.markdown(f"**Class:** {booking['class']}")
    
    with col2:
        st.markdown(f"**Departure:** {booking['departure_time']}")
        st.markdown(f"**Arrival:** {booking['arrival_time']}")
        st.markdown(f"**Boarding:** {booking['boarding_time']}")
        st.markdown(f"**Gate:** {booking['gate']}")
    
    with col3:
        st.markdown(f"**Terminal:** {booking['terminal']}")
        st.markdown(f"**Seat:** {booking['seat']}")
        st.markdown(f"**Baggage:** {booking['baggage_allowance']}")
        st.markdown(f"**Status:** ✅ {booking['status']}")
    
    # Passenger information
    st.markdown("### 👤 Passenger Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Name:** {booking['passenger_name']}")
        st.markdown(f"**Meal Preference:** {booking['meal_preference']}")
        
        # Update meal preference
        new_meal = st.selectbox(
            "Update Meal Preference",
            ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free"],
            index=0,
            key="checkin_meal_update"
        )
    
    with col2:
        st.markdown("**Special Requests**")
        special_requests = st.multiselect(
            "Select any special assistance needed",
            ["Wheelchair assistance", "Extra baggage", "Priority boarding", "Dietary requirements"],
            key="checkin_special_requests"
        )
    
    # Seat selection
    st.markdown("### 💺 Seat Selection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Current Seat:** {booking['seat']}")
        
        # Seat map (simplified)
        display_simplified_seat_map()
    
    with col2:
        st.markdown("**Seat Information**")
        st.markdown("🪟 Window seat")
        st.markdown("✅ Standard seat")
        st.markdown("🔄 Change available")
        
        if st.button("Change Seat", key="change_seat_checkin"):
            st.info("Seat change options would be displayed here")
    
    # Baggage information
    st.markdown("### 🧳 Baggage Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Included Baggage:**")
        st.markdown(f"• Carry-on: 7kg")
        st.markdown(f"• Checked: {booking['baggage_allowance']}")
        
        # Additional baggage
        extra_baggage = st.number_input(
            "Additional Baggage (kg)",
            min_value=0,
            max_value=50,
            step=5,
            key="extra_baggage_checkin"
        )
        
        if extra_baggage > 0:
            cost = extra_baggage * 15  # $15 per kg
            st.markdown(f"**Additional cost:** ${cost}")
    
    with col2:
        st.markdown("**Baggage Tips:**")
        st.markdown("• Arrive 3 hours early for international flights")
        st.markdown("• No liquids over 100ml in carry-on")
        st.markdown("• Pack electronics in carry-on")
        st.markdown("• Tag your bags with contact info")
    
    # Travel documents reminder
    st.markdown("### 📄 Travel Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Required Documents:**")
        documents = [
            "Valid passport (6+ months validity)",
            "Visa (if required)",
            "COVID-19 vaccination certificate",
            "Return/onward ticket",
            "Travel insurance"
        ]
        
        for doc in documents:
            st.checkbox(doc, key=f"doc_{doc}")
    
    with col2:
        st.markdown("**Destination Requirements:**")
        st.info("🇬🇧 UK: Electronic Travel Authorization required")
        st.info("💉 COVID-19: Check latest requirements")
        st.info("🛂 Customs: Declare items over allowance")
    
    # Mobile boarding pass
    st.markdown("### 📱 Mobile Boarding Pass")
    
    col1, col2 = st.columns(2)
    
    with col1:
        phone_number = st.text_input(
            "Mobile Number for Boarding Pass",
            placeholder="+254 700 000 000",
            key="checkin_mobile"
        )
        
        email_address = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            key="checkin_email"
        )
    
    with col2:
        st.markdown("**Boarding Pass Options:**")
        send_options = st.multiselect(
            "Send boarding pass via",
            ["SMS", "Email", "WhatsApp", "App Notification"],
            default=["Email"],
            key="checkin_send_options"
        )
    
    # Complete check-in
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Save Changes", use_container_width=True, key="save_changes_checkin"):
            st.success("✅ Changes saved successfully!")
    
    with col2:
        if st.button("🎫 Complete Check-In", type="primary", use_container_width=True, key="complete_checkin"):
            if booking['checkin_available']:
                complete_checkin(booking, phone_number, email_address, send_options)
            else:
                st.error("Check-in not available yet. Please try again 24 hours before departure.")

def display_simplified_seat_map():
    """Display a simplified seat map for check-in"""
    st.markdown("**Select Your Seat:**")
    
    # Simple seat grid
    seats = ["21A", "21B", "21C", "21D", "21E", "21F"]
    available_seats = ["21A", "21C", "21E", "21F"]
    
    cols = st.columns(6)
    
    for i, seat in enumerate(seats):
        with cols[i]:
            if seat in available_seats:
                if st.button(f"✅\n{seat}", key=f"seat_select_{seat}"):
                    st.session_state.checkin_booking['seat'] = seat
                    st.success(f"Seat {seat} selected!")
                    st.rerun()
            else:
                st.button(f"❌\n{seat}", disabled=True, key=f"seat_occupied_{seat}")

def complete_checkin(booking, phone, email, send_options):
    """Complete the check-in process"""
    if not phone and not email:
        st.error("Please provide at least one contact method for your boarding pass.")
        return
    
    # Simulate check-in completion
    with st.spinner("Completing your check-in..."):
        # Generate boarding pass
        boarding_pass = generate_boarding_pass(booking)
        st.session_state.boarding_pass = boarding_pass
    
    st.success("🎉 Check-in completed successfully!")
    st.balloons()
    
    # Display boarding pass
    display_boarding_pass(boarding_pass)
    
    # Send confirmation
    if "SMS" in send_options and phone:
        st.info(f"📱 Boarding pass sent via SMS to {phone}")
    
    if "Email" in send_options and email:
        st.info(f"📧 Boarding pass sent to {email}")
    
    # Important reminders
    st.markdown("### ⚠️ Important Reminders")
    st.warning("🕐 Arrive at the airport at least 3 hours before international departure")
    st.info("🛂 Have your passport and boarding pass ready at security")
    st.info("🚪 Boarding typically begins 45 minutes before departure")

def generate_boarding_pass(booking):
    """Generate boarding pass information"""
    return {
        "passenger_name": booking['passenger_name'],
        "flight_number": booking['flight_number'],
        "route": booking['route'],
        "departure_date": booking['departure_date'],
        "departure_time": booking['departure_time'],
        "boarding_time": booking['boarding_time'],
        "seat": booking['seat'],
        "gate": booking['gate'],
        "terminal": booking['terminal'],
        "class": booking['class'],
        "booking_reference": booking['booking_reference'],
        "barcode": f"*{booking['booking_reference']}*{booking['flight_number']}*",
        "sequence": random.randint(1, 200)
    }

def display_boarding_pass(boarding_pass):
    """Display the boarding pass"""
    st.markdown("### 🎫 Your Boarding Pass")
    
    # Boarding pass design
    st.markdown(f"""
    <div style="
        border: 2px solid #1E40AF;
        border-radius: 10px;
        padding: 20px;
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        margin: 20px 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>🇰🇪 KENYA AIRWAYS</h2>
                <p>BOARDING PASS</p>
            </div>
            <div style="text-align: right;">
                <h3>{boarding_pass['flight_number']}</h3>
                <p>{boarding_pass['departure_date']}</p>
            </div>
        </div>
        
        <hr style="border-color: white; margin: 20px 0;">
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
            <div>
                <strong>PASSENGER</strong><br>
                {boarding_pass['passenger_name']}<br><br>
                <strong>ROUTE</strong><br>
                {boarding_pass['route']}
            </div>
            <div>
                <strong>DEPARTURE</strong><br>
                {boarding_pass['departure_time']}<br><br>
                <strong>BOARDING</strong><br>
                {boarding_pass['boarding_time']}
            </div>
            <div>
                <strong>SEAT</strong><br>
                {boarding_pass['seat']}<br><br>
                <strong>GATE</strong><br>
                {boarding_pass['gate']}
            </div>
        </div>
        
        <hr style="border-color: white; margin: 20px 0;">
        
        <div style="text-align: center;">
            <p>BOOKING REFERENCE: {boarding_pass['booking_reference']}</p>
            <p style="font-family: monospace; font-size: 18px;">
                {boarding_pass['barcode']}
            </p>
            <p>Sequence: {boarding_pass['sequence']} | Class: {boarding_pass['class']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF", use_container_width=True, key="download_pdf_checkin"):
            st.info("PDF boarding pass downloaded")
    
    with col2:
        if st.button("📱 Add to Wallet", use_container_width=True, key="add_wallet_checkin"):
            st.info("Added to mobile wallet")
    
    with col3:
        if st.button("📧 Email Again", use_container_width=True, key="email_again_checkin"):
            st.info("Boarding pass emailed again")
