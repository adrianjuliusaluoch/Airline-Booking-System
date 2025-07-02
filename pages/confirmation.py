import streamlit as st
import qrcode
from io import BytesIO
import base64

def show():
    st.markdown("## ✅ Booking Confirmation")
    
    if not st.session_state.current_booking:
        st.info("No booking to display. Please complete a booking first.")
        return
    
    booking = st.session_state.current_booking
    
    # Success message
    st.success("🎉 Your booking has been confirmed!")
    
    # Booking reference
    st.markdown(f"### Booking Reference: `{booking['booking_reference']}`")
    st.markdown("*Please save this reference number for your records*")
    
    # Generate QR code for booking reference
    qr_code = generate_qr_code(booking['booking_reference'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Booking details
        display_booking_details(booking)
    
    with col2:
        # QR code and quick actions
        st.markdown("### 📱 Quick Access")
        st.image(qr_code, width=200)
        st.markdown("*Scan QR code for quick booking access*")
        
        # Quick action buttons
        if st.button("📧 Email Confirmation", use_container_width=True, key="email_confirmation"):
            st.info("Confirmation email sent to " + booking['contact']['email'])
        
        if st.button("📱 SMS Confirmation", use_container_width=True, key="sms_confirmation"):
            st.info("SMS confirmation sent to " + booking['contact']['phone'])
        
        if st.button("📄 Download PDF", use_container_width=True, key="download_pdf_confirmation"):
            st.info("PDF ticket downloaded (simulation)")
    
    # Flight tickets
    st.markdown("### 🎫 Your Tickets")
    
    for i, ticket in enumerate(booking['tickets']):
        with st.expander(f"Ticket {i + 1} - {ticket['passenger_name']}", expanded=i == 0):
            display_ticket_details(ticket, booking)
    
    # Important information
    st.markdown("### ℹ️ Important Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Before You Travel:**
        - ✅ Check passport validity (6+ months)
        - ✅ Verify visa requirements
        - ✅ Review baggage allowances
        - ✅ Complete online check-in (24h before)
        - ✅ Arrive at airport 3 hours early (international)
        """)
    
    with col2:
        st.markdown("""
        **Need Help?**
        - 📞 Customer Service: +254 20 327 4747
        - 💬 Live Chat: Available 24/7
        - 📧 Email: support@kenya-airways.com
        - 🌐 Manage Booking: Online portal
        """)
    
    # Travel checklist
    st.markdown("### ✈️ Travel Checklist")
    
    checklist_items = [
        "Passport and visa documents ready",
        "Flight confirmation printed/saved",
        "Baggage packed according to restrictions",
        "Transportation to airport arranged",
        "Travel insurance confirmed",
        "Emergency contacts informed",
        "Mobile boarding passes downloaded",
        "Frequent flyer number updated"
    ]
    
    for item in checklist_items:
        st.checkbox(item, key=f"checklist_{item}")
    
    # Weather and destination info
    st.markdown("### 🌤️ Destination Weather")
    
    # Simulate weather information
    destinations = [flight['destination'] for flight in booking['flights']]
    unique_destinations = list(set(destinations))
    
    for dest in unique_destinations:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{dest}**")
            st.markdown("🌤️ Partly Cloudy")
            st.markdown("🌡️ 24°C / 75°F")
        
        with col2:
            st.markdown("**Local Time**")
            st.markdown("GMT +3:00")
            st.markdown("Current: 14:30")
        
        with col3:
            st.markdown("**Currency**")
            if dest == "London":
                st.markdown("💷 British Pound")
            elif dest == "Dubai":
                st.markdown("💴 UAE Dirham")
            else:
                st.markdown("💵 Local Currency")
    
    # Booking management options
    st.markdown("### 🛠️ Manage Your Booking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✏️ Modify Booking", use_container_width=True, key="modify_booking_confirmation"):
            st.info("Redirecting to booking modification...")
    
    with col2:
        if st.button("💺 Select Seats", use_container_width=True, key="select_seats_confirmation"):
            st.info("Redirecting to seat selection...")
    
    with col3:
        if st.button("🍽️ Add Meals", use_container_width=True, key="add_meals_confirmation"):
            st.info("Redirecting to meal selection...")
    
    # Start new booking
    st.markdown("---")
    if st.button("🆕 Book Another Flight", type="primary", use_container_width=True, key="book_another_flight"):
        # Clear current booking
        st.session_state.current_booking = None
        st.session_state.search_results = None
        st.session_state.selected_flights = {}
        st.session_state.passengers = []
        st.session_state.booking_data = {}
        st.session_state.seat_selections = {}
        
        st.success("Ready for a new booking!")
        st.rerun()

def display_booking_details(booking):
    """Display detailed booking information"""
    st.markdown("### 📋 Booking Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Booking Date:** {booking['created_at'][:10]}")
        st.markdown(f"**Status:** {booking['status']}")
        st.markdown(f"**Payment Status:** {booking['payment_status']}")
    
    with col2:
        st.markdown(f"**Total Amount:** ${booking['total_price']}")
        st.markdown(f"**Passengers:** {len(booking['passengers'])}")
        st.markdown(f"**Contact:** {booking['contact']['email']}")
    
    # Flight details
    st.markdown("**Flight Details:**")
    for i, flight in enumerate(booking['flights']):
        st.markdown(f"""
        **Flight {i + 1}: {flight['flight_number']}**
        - Route: {flight['origin']} → {flight['destination']}
        - Date: {flight['departure_date']}
        - Time: {flight['departure_time']} - {flight['arrival_time']}
        - Aircraft: {flight['aircraft']}
        """)

def display_ticket_details(ticket, booking):
    """Display individual ticket details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Ticket Number:** {ticket['ticket_number']}")
        st.markdown(f"**Passenger:** {ticket['passenger_name']}")
        st.markdown(f"**Class:** {ticket['class']}")
        st.markdown(f"**Seat:** {ticket['seat']}")
    
    with col2:
        st.markdown("**Barcode Simulation:**")
        st.code(ticket['ticket_number'], language=None)
        
        if ticket['special_requests']:
            st.markdown("**Special Requests:**")
            for request in ticket['special_requests']:
                st.markdown(f"• {request}")

def generate_qr_code(booking_reference):
    """Generate QR code for booking reference"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Kenya Airways Booking: {booking_reference}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"
