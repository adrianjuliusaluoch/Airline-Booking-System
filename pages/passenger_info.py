import streamlit as st
from datetime import datetime, date
from utils.booking import validate_passenger_info, create_booking
from utils.session import get_search_params

def show():
    st.markdown("## 👤 Passenger Information")
    
    if not st.session_state.booking_data:
        st.info("Please complete the booking process first.")
        return
    
    booking_data = st.session_state.booking_data
    total_passengers = booking_data['total_passengers']
    params = get_search_params()
    
    # Display booking summary
    with st.expander("📋 Booking Summary", expanded=False):
        display_booking_summary()
    
    # Passenger information forms
    st.markdown("### 👥 Enter Passenger Details")
    
    passengers = []
    passenger_types = []
    
    # Determine passenger types
    for i in range(params['adults']):
        passenger_types.append(('Adult', i + 1))
    for i in range(params['children']):
        passenger_types.append(('Child', i + 1))
    for i in range(params['infants']):
        passenger_types.append(('Infant', i + 1))
    
    # Create passenger forms
    for i, (passenger_type, number) in enumerate(passenger_types):
        with st.expander(f"Passenger {i + 1} - {passenger_type} {number}", expanded=i == 0):
            passenger = create_passenger_form(i, passenger_type)
            passengers.append(passenger)
    
    # Terms and additional information
    st.markdown("### 📋 Additional Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        frequent_flyer = st.text_input("Frequent Flyer Number (Optional)", key="frequent_flyer")
        emergency_contact_name = st.text_input("Emergency Contact Name*", key="emergency_name")
    
    with col2:
        emergency_contact_phone = st.text_input("Emergency Contact Phone*", key="emergency_phone")
        emergency_relationship = st.selectbox("Relationship", ["Parent", "Spouse", "Sibling", "Friend", "Other"], key="emergency_rel")
    
    # Passport/ID upload simulation
    st.markdown("### 📄 Document Upload")
    st.info("In a real system, you would upload passport/ID copies here.")
    
    # API/Web integration information
    st.markdown("### 🌐 Travel Information")
    visa_required = st.checkbox("I need visa assistance")
    if visa_required:
        st.info("Our travel team will contact you regarding visa requirements.")
    
    travel_insurance_upgrade = st.checkbox("Upgrade to premium travel insurance (+$50 per person)")
    
    # Final validation and booking creation
    if st.button("Complete Booking", type="primary", use_container_width=True, key="complete_booking_btn"):
        # Validate all passenger information
        all_valid = True
        for i, passenger in enumerate(passengers):
            errors = validate_passenger_info(passenger)
            if errors:
                st.error(f"Passenger {i + 1} has errors: {', '.join(errors)}")
                all_valid = False
        
        # Check required fields
        if not emergency_contact_name or not emergency_contact_phone:
            st.error("Emergency contact information is required.")
            all_valid = False
        
        if all_valid:
            # Calculate final price with upgrades
            final_price = booking_data['total_price']
            if travel_insurance_upgrade:
                final_price += 50 * total_passengers
            
            # Create booking
            booking_request = {
                'flights': booking_data['flights'],
                'passengers': passengers,
                'contact': booking_data['contact'],
                'total_price': final_price,
                'extras': booking_data.get('extras', {}),
                'seat_selections': booking_data.get('seat_selections', {}),
                'special_requests': booking_data.get('special_requests', {}),
                'emergency_contact': {
                    'name': emergency_contact_name,
                    'phone': emergency_contact_phone,
                    'relationship': emergency_relationship
                },
                'frequent_flyer': frequent_flyer,
                'visa_assistance': visa_required,
                'premium_insurance': travel_insurance_upgrade
            }
            
            # Create the booking
            booking = create_booking(booking_request)
            st.session_state.current_booking = booking
            
            st.success("🎉 Booking completed successfully!")
            st.balloons()
            
            # Clear booking data
            st.session_state.booking_data = {}
            
            st.rerun()

def create_passenger_form(index, passenger_type):
    """Create a passenger information form"""
    passenger = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        passenger['first_name'] = st.text_input("First Name*", key=f"first_name_{index}")
        passenger['last_name'] = st.text_input("Last Name*", key=f"last_name_{index}")
        passenger['date_of_birth'] = st.date_input(
            "Date of Birth*", 
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key=f"dob_{index}"
        )
        passenger['gender'] = st.selectbox("Gender*", ["Male", "Female", "Other"], key=f"gender_{index}")
    
    with col2:
        passenger['nationality'] = st.selectbox(
            "Nationality*", 
            ["Kenyan", "British", "American", "Canadian", "South African", "Nigerian", "Other"],
            key=f"nationality_{index}"
        )
        passenger['passport_number'] = st.text_input("Passport/ID Number*", key=f"passport_{index}")
        passenger['passport_expiry'] = st.date_input(
            "Passport Expiry Date*",
            min_value=date.today(),
            key=f"passport_expiry_{index}"
        )
        passenger['issuing_country'] = st.text_input("Issuing Country*", key=f"issuing_country_{index}")
    
    # Special requirements for this passenger
    passenger['meal_preference'] = st.selectbox(
        "Meal Preference",
        ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free"],
        key=f"meal_{index}"
    )
    
    if passenger_type in ['Child', 'Infant']:
        passenger['accompanying_adult'] = st.text_input(
            "Accompanying Adult Name*",
            key=f"adult_{index}"
        )
    
    # Seat assignment (if seats were selected)
    if st.session_state.seat_selections:
        selected_seats = []
        for flight_number, seats in st.session_state.seat_selections.items():
            if index < len(seats):
                selected_seats.append(f"{flight_number}: {seats[index]}")
        
        if selected_seats:
            passenger['assigned_seats'] = selected_seats
            st.info(f"Assigned seats: {', '.join(selected_seats)}")
    
    passenger['passenger_type'] = passenger_type
    passenger['class'] = get_search_params()['travel_class']
    
    return passenger

def display_booking_summary():
    """Display a summary of the current booking"""
    booking_data = st.session_state.booking_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Flights:**")
        for flight in booking_data['flights']:
            st.markdown(f"• {flight['flight_number']}: {flight['origin']} → {flight['destination']}")
        
        st.markdown(f"**Passengers:** {booking_data['total_passengers']}")
        st.markdown(f"**Class:** {booking_data['travel_class']}")
    
    with col2:
        st.markdown(f"**Base Price:** ${booking_data['total_price'] - sum(booking_data.get('extras', {}).values())}")
        
        if booking_data.get('extras'):
            st.markdown("**Extras:**")
            for extra, cost in booking_data['extras'].items():
                st.markdown(f"• {extra.title()}: ${cost}")
        
        st.markdown(f"**Total:** ${booking_data['total_price']}")
