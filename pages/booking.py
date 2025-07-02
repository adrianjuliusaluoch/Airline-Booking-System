import streamlit as st
from utils.session import get_search_params
from utils.booking import calculate_total_price

def show():
    st.markdown("## ✈️ Book Your Flight")
    
    if not st.session_state.selected_flights:
        st.info("Please search and select flights first in the Search Flights tab.")
        return
    
    # Display selected flights summary
    display_flight_summary()
    
    # Passenger count validation
    params = get_search_params()
    total_passengers = params['adults'] + params['children'] + params['infants']
    
    # Contact information
    st.markdown("### 📞 Contact Information")
    col1, col2 = st.columns(2)
    
    with col1:
        contact_email = st.text_input("Email Address*", key="contact_email")
        contact_phone = st.text_input("Phone Number*", key="contact_phone")
    
    with col2:
        contact_name = st.text_input("Contact Name*", key="contact_name")
        contact_country = st.selectbox("Country Code", ["+254", "+44", "+1", "+971"], key="contact_country")
    
    # Travel insurance
    st.markdown("### 🛡️ Travel Insurance")
    travel_insurance = st.checkbox("Add comprehensive travel insurance (+$25 per person)")
    
    # Special requests
    st.markdown("### 🍽️ Special Requests")
    col1, col2 = st.columns(2)
    
    with col1:
        meal_preferences = st.multiselect(
            "Meal Preferences",
            ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free", "Low-sodium"],
            key="meal_prefs"
        )
    
    with col2:
        assistance_needed = st.multiselect(
            "Assistance Required",
            ["Wheelchair assistance", "Extra baggage", "Pet transportation", "Unaccompanied minor"],
            key="assistance"
        )
    
    # Calculate pricing
    flights = list(st.session_state.selected_flights.values())
    base_total = 0
    
    for flight in flights:
        base_total += flight['prices'][params['travel_class']] * total_passengers
    
    extras = {}
    if travel_insurance:
        extras['insurance'] = 25 * total_passengers
    
    total_price = base_total + sum(extras.values())
    
    # Pricing breakdown
    st.markdown("### 💰 Pricing Breakdown")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Flight Tickets**")
        for flight in flights:
            price_per_person = flight['prices'][params['travel_class']]
            flight_total = price_per_person * total_passengers
            st.markdown(f"• {flight['flight_number']}: ${price_per_person} × {total_passengers} = ${flight_total}")
        
        if extras:
            st.markdown("**Additional Services**")
            for service, cost in extras.items():
                st.markdown(f"• {service.title()}: ${cost}")
        
        st.markdown("**Taxes & Fees**: Included")
    
    with col2:
        st.markdown(f"### Total: ${total_price}")
        st.markdown(f"For {total_passengers} passenger(s)")
    
    # Terms and conditions
    st.markdown("### 📋 Terms & Conditions")
    accept_terms = st.checkbox("I accept the terms and conditions and privacy policy*")
    
    # Newsletter subscription
    subscribe_newsletter = st.checkbox("Subscribe to Kenya Airways newsletter for deals and updates")
    
    # Proceed to passenger information
    if st.button("Continue to Passenger Details", type="primary", use_container_width=True, key="continue_to_passenger_details"):
        if not all([contact_email, contact_phone, contact_name, accept_terms]):
            st.error("Please fill in all required fields and accept terms and conditions.")
        elif not validate_email(contact_email):
            st.error("Please enter a valid email address.")
        else:
            # Save booking data to session
            st.session_state.booking_data = {
                'flights': flights,
                'contact': {
                    'email': contact_email,
                    'phone': f"{contact_country}{contact_phone}",
                    'name': contact_name
                },
                'total_passengers': total_passengers,
                'travel_class': params['travel_class'],
                'total_price': total_price,
                'extras': extras,
                'special_requests': {
                    'meals': meal_preferences,
                    'assistance': assistance_needed
                },
                'newsletter': subscribe_newsletter
            }
            
            st.success("Booking information saved! Please proceed to enter passenger details.")
            st.rerun()

def display_flight_summary():
    """Display summary of selected flights"""
    st.markdown("### ✈️ Selected Flights")
    
    for flight_type, flight in st.session_state.selected_flights.items():
        with st.expander(f"{flight_type.title()} Flight - {flight['flight_number']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Route**: {flight['origin']} → {flight['destination']}")
                st.markdown(f"**Date**: {flight['departure_date']}")
                st.markdown(f"**Time**: {flight['departure_time']} - {flight['arrival_time']}")
            
            with col2:
                st.markdown(f"**Duration**: {flight['duration']}")
                st.markdown(f"**Aircraft**: {flight['aircraft']}")
                stops_text = "Direct" if flight['stops'] == 0 else f"{flight['stops']} stop(s)"
                st.markdown(f"**Stops**: {stops_text}")
            
            with col3:
                params = get_search_params()
                price = flight['prices'][params['travel_class']]
                st.markdown(f"**Class**: {params['travel_class']}")
                st.markdown(f"**Price**: ${price} per person")
                
                if st.button(f"Remove {flight_type.title()} Flight", key=f"remove_{flight_type}"):
                    del st.session_state.selected_flights[flight_type]
                    st.rerun()

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
