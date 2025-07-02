import streamlit as st
from datetime import datetime, timedelta
import random

def show():
    st.markdown("## 📝 Manage Your Booking")
    
    # Booking lookup
    st.markdown("### 🔍 Find Your Booking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        booking_ref = st.text_input(
            "Booking Reference*",
            placeholder="Enter your booking reference (e.g., KQ123456)",
            key="manage_booking_ref"
        )
        
        last_name = st.text_input(
            "Last Name*",
            placeholder="Enter passenger's last name",
            key="manage_last_name"
        )
    
    with col2:
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address",
            key="manage_email"
        )
        
        phone = st.text_input(
            "Phone Number",
            placeholder="Enter your phone number",
            key="manage_phone"
        )
    
    # Search booking
    if st.button("Find My Booking", type="primary", use_container_width=True, key="find_booking_manage"):
        if booking_ref and last_name:
            with st.spinner("Looking up your booking..."):
                booking = simulate_booking_retrieval(booking_ref, last_name)
            
            if booking:
                st.session_state.manage_booking_data = booking
                st.success("✅ Booking found!")
                st.rerun()
            else:
                st.error("❌ Booking not found. Please check your details.")
        else:
            st.error("Please enter both booking reference and last name.")
    
    # Display booking management options
    if st.session_state.get('manage_booking_data'):
        display_booking_management()

def simulate_booking_retrieval(booking_ref, last_name):
    """Simulate booking retrieval from database"""
    if len(booking_ref) >= 6 and len(last_name) >= 2:
        return {
            "booking_reference": booking_ref,
            "status": "Confirmed",
            "created_date": "2025-06-15",
            "passengers": [
                {
                    "name": f"John {last_name}",
                    "type": "Adult",
                    "seat": "12A",
                    "meal": "Standard",
                    "special_requests": []
                },
                {
                    "name": f"Jane {last_name}",
                    "type": "Adult", 
                    "seat": "12B",
                    "meal": "Vegetarian",
                    "special_requests": ["Extra legroom"]
                }
            ],
            "flights": [
                {
                    "flight_number": f"KQ{random.randint(100, 999)}",
                    "route": "Nairobi → London",
                    "departure_date": "2025-07-15",
                    "departure_time": "10:45",
                    "arrival_time": "15:30",
                    "class": "Economy",
                    "aircraft": "Boeing 787-8"
                },
                {
                    "flight_number": f"KQ{random.randint(100, 999)}",
                    "route": "London → Nairobi", 
                    "departure_date": "2025-07-22",
                    "departure_time": "21:30",
                    "arrival_time": "07:15+1",
                    "class": "Economy",
                    "aircraft": "Boeing 787-8"
                }
            ],
            "contact": {
                "email": "john.doe@email.com",
                "phone": "+254 700 123 456"
            },
            "payment": {
                "total_amount": 1890,
                "currency": "USD",
                "status": "Paid",
                "method": "Credit Card"
            },
            "extras": {
                "baggage": "Standard",
                "insurance": True,
                "meals": "Included"
            }
        }
    return None

def display_booking_management():
    """Display booking management interface"""
    booking = st.session_state.manage_booking_data
    
    # Booking overview
    st.markdown("### 📋 Booking Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**Reference:** {booking['booking_reference']}")
        st.markdown(f"**Status:** ✅ {booking['status']}")
        st.markdown(f"**Created:** {booking['created_date']}")
    
    with col2:
        st.markdown(f"**Passengers:** {len(booking['passengers'])}")
        st.markdown(f"**Flights:** {len(booking['flights'])}")
        st.markdown(f"**Total:** ${booking['payment']['total_amount']}")
    
    with col3:
        st.markdown(f"**Payment:** {booking['payment']['status']}")
        st.markdown(f"**Contact:** {booking['contact']['email']}")
        st.markdown(f"**Phone:** {booking['contact']['phone']}")
    
    # Management options tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✈️ Flight Details", 
        "👥 Passengers", 
        "💺 Seats & Meals", 
        "🧳 Add Services", 
        "🔄 Modify/Cancel"
    ])
    
    with tab1:
        display_flight_details(booking['flights'])
    
    with tab2:
        display_passenger_management(booking['passengers'])
    
    with tab3:
        display_seats_meals_management(booking)
    
    with tab4:
        display_additional_services(booking)
    
    with tab5:
        display_modify_cancel_options(booking)

def display_flight_details(flights):
    """Display flight details with modification options"""
    st.markdown("### ✈️ Flight Information")
    
    for i, flight in enumerate(flights):
        with st.expander(f"Flight {i + 1}: {flight['flight_number']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Route:** {flight['route']}")
                st.markdown(f"**Date:** {flight['departure_date']}")
                st.markdown(f"**Departure:** {flight['departure_time']}")
                st.markdown(f"**Arrival:** {flight['arrival_time']}")
            
            with col2:
                st.markdown(f"**Class:** {flight['class']}")
                st.markdown(f"**Aircraft:** {flight['aircraft']}")
                
                # Flight status
                status = random.choice(["On Time", "Delayed", "Confirmed"])
                status_emoji = {"On Time": "🟢", "Delayed": "🟡", "Confirmed": "✅"}.get(status, "❓")
                st.markdown(f"**Status:** {status_emoji} {status}")
            
            with col3:
                if st.button(f"📊 Flight Status", key=f"status_{i}"):
                    st.info(f"Checking status for {flight['flight_number']}")
                
                if st.button(f"🎫 Check-In", key=f"checkin_{i}"):
                    st.info("Redirecting to check-in...")
                
                if st.button(f"🔄 Change Flight", key=f"change_{i}"):
                    st.info("Flight change options would be displayed here")

def display_passenger_management(passengers):
    """Display passenger information with edit options"""
    st.markdown("### 👥 Passenger Information")
    
    for i, passenger in enumerate(passengers):
        with st.expander(f"Passenger {i + 1}: {passenger['name']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Editable passenger info
                new_name = st.text_input(
                    "Full Name",
                    value=passenger['name'],
                    key=f"passenger_name_{i}"
                )
                
                new_meal = st.selectbox(
                    "Meal Preference",
                    ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free"],
                    index=["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free"].index(passenger['meal']),
                    key=f"passenger_meal_{i}"
                )
            
            with col2:
                current_seat = passenger['seat']
                st.markdown(f"**Current Seat:** {current_seat}")
                
                if st.button(f"Change Seat", key=f"change_seat_{i}"):
                    st.info("Seat selection interface would open here")
                
                # Special requests
                special_requests = st.multiselect(
                    "Special Requests",
                    ["Wheelchair assistance", "Extra legroom", "Priority boarding", "Special meal"],
                    default=passenger['special_requests'],
                    key=f"special_requests_{i}"
                )
            
            # Save changes button
            if st.button(f"💾 Save Changes", key=f"save_passenger_{i}"):
                st.success(f"Changes saved for {passenger['name']}")

def display_seats_meals_management(booking):
    """Display seat and meal management"""
    st.markdown("### 💺 Seats & Meals Management")
    
    # Current seat assignment
    st.markdown("**Current Seat Assignments:**")
    
    for flight in booking['flights']:
        st.markdown(f"**{flight['flight_number']} - {flight['route']}**")
        
        col1, col2, col3 = st.columns(3)
        
        for i, passenger in enumerate(booking['passengers']):
            with [col1, col2, col3][i % 3]:
                st.markdown(f"• {passenger['name']}: {passenger['seat']}")
                
                if st.button(f"Change Seat", key=f"seat_change_{flight['flight_number']}_{i}"):
                    display_seat_selection_interface(flight, passenger)
    
    # Meal preferences
    st.markdown("---")
    st.markdown("**Meal Preferences:**")
    
    for i, passenger in enumerate(booking['passengers']):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{passenger['name']}**")
            current_meal = passenger['meal']
            
            new_meal = st.selectbox(
                "Meal Preference",
                ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free", "Child Meal"],
                index=["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free", "Child Meal"].index(current_meal) if current_meal in ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-free", "Child Meal"] else 0,
                key=f"meal_update_{i}"
            )
        
        with col2:
            if new_meal != current_meal:
                st.info(f"Meal preference will be updated to: {new_meal}")
                
                if st.button(f"Update Meal", key=f"update_meal_{i}"):
                    st.success(f"Meal preference updated for {passenger['name']}")

def display_seat_selection_interface(flight, passenger):
    """Display seat selection interface"""
    st.markdown(f"### Select New Seat for {passenger['name']}")
    st.markdown(f"**Flight:** {flight['flight_number']} - {flight['route']}")
    
    # Simplified seat map
    st.markdown("**Available Seats:**")
    
    available_seats = ["12A", "12C", "15A", "15B", "15C", "18D", "18E", "18F"]
    
    cols = st.columns(4)
    
    for i, seat in enumerate(available_seats):
        with cols[i % 4]:
            seat_type = "🪟" if seat[-1] in "AF" else "🚪" if seat[-1] in "CF" else "🪑"
            price = "+$25" if seat[-1] in "AF" else "+$15" if seat[-1] in "CF" else "Free"
            
            if st.button(f"{seat_type} {seat}\n{price}", key=f"select_seat_{seat}_{flight['flight_number']}"):
                st.success(f"Seat {seat} selected for {passenger['name']}")

def display_additional_services(booking):
    """Display additional services that can be added"""
    st.markdown("### 🧳 Additional Services")
    
    # Baggage services
    st.markdown("**Baggage Services:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Allowance:**")
        st.markdown("• Carry-on: 7kg included")
        st.markdown("• Checked: 23kg included")
        
        # Add extra baggage
        extra_baggage = st.number_input(
            "Additional Baggage (kg)",
            min_value=0,
            max_value=50,
            step=5,
            key="extra_baggage_manage"
        )
        
        if extra_baggage > 0:
            cost = extra_baggage * 15
            st.markdown(f"**Cost:** ${cost}")
            
            if st.button("Add Extra Baggage", key="add_extra_baggage_btn"):
                st.success(f"Added {extra_baggage}kg extra baggage")
    
    with col2:
        st.markdown("**Premium Services:**")
        
        services = {
            "Priority Boarding": 25,
            "Extra Legroom Seat": 50,
            "Lounge Access": 75,
            "Premium Meal": 35,
            "WiFi Package": 20
        }
        
        selected_services = []
        
        for service, price in services.items():
            if st.checkbox(f"{service} (+${price})", key=f"service_{service}"):
                selected_services.append((service, price))
        
        if selected_services:
            total_cost = sum(price for _, price in selected_services)
            st.markdown(f"**Additional Cost:** ${total_cost}")
            
            if st.button("Add Selected Services", key="add_selected_services_btn"):
                st.success("Services added to your booking")
    
    # Travel insurance
    st.markdown("---")
    st.markdown("**Travel Insurance:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_insurance = booking['extras']['insurance']
        st.markdown(f"**Current:** {'✅ Included' if current_insurance else '❌ Not included'}")
        
        if not current_insurance:
            insurance_options = st.radio(
                "Add Travel Insurance",
                ["No Insurance", "Basic Coverage (+$25)", "Premium Coverage (+$50)"],
                key="insurance_options"
            )
            
            if insurance_options != "No Insurance":
                if st.button("Add Insurance", key="add_insurance_btn"):
                    st.success("Travel insurance added to your booking")
    
    with col2:
        st.markdown("**Insurance Benefits:**")
        st.markdown("• Trip cancellation coverage")
        st.markdown("• Medical emergency coverage")
        st.markdown("• Baggage loss protection")
        st.markdown("• Flight delay compensation")

def display_modify_cancel_options(booking):
    """Display booking modification and cancellation options"""
    st.markdown("### 🔄 Modify or Cancel Booking")
    
    # Modification options
    st.markdown("**Modification Options:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Change Flight:**")
        st.markdown("• Date change: $150 fee")
        st.markdown("• Route change: $200 fee")
        st.markdown("• Class upgrade: Price difference")
        
        if st.button("Change Flight Details", use_container_width=True, key="change_flight_details_btn"):
            st.info("Flight change interface would open here")
        
        st.markdown("**Name Change:**")
        st.markdown("• Minor corrections: $50 fee")
        st.markdown("• Complete name change: $100 fee")
        
        if st.button("Change Passenger Name", use_container_width=True, key="change_passenger_name_btn"):
            st.info("Name change form would open here")
    
    with col2:
        st.markdown("**Add Passengers:**")
        st.markdown("• Subject to availability")
        st.markdown("• Same fare rules apply")
        
        if st.button("Add Passenger", use_container_width=True, key="add_passenger_btn"):
            st.info("Add passenger interface would open here")
        
        st.markdown("**Transfer Booking:**")
        st.markdown("• Transfer to another person")
        st.markdown("• $200 transfer fee")
        
        if st.button("Transfer Booking", use_container_width=True, key="transfer_booking_btn"):
            st.info("Booking transfer form would open here")
    
    # Cancellation options
    st.markdown("---")
    st.markdown("**Cancellation Policy:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Refund Information:**")
        
        # Calculate refund based on booking date and current date
        booking_date = datetime.strptime(booking['created_date'], '%Y-%m-%d')
        days_to_departure = 7  # Simulated
        
        if days_to_departure > 24:
            refund_amount = booking['payment']['total_amount'] * 0.8  # 80% refund
            st.markdown(f"• Full refund: ${refund_amount:.0f} (80%)")
            st.markdown(f"• Cancellation fee: ${booking['payment']['total_amount'] - refund_amount:.0f}")
        elif days_to_departure > 7:
            refund_amount = booking['payment']['total_amount'] * 0.5  # 50% refund
            st.markdown(f"• Partial refund: ${refund_amount:.0f} (50%)")
            st.markdown(f"• Cancellation fee: ${booking['payment']['total_amount'] - refund_amount:.0f}")
        else:
            st.markdown("• No refund available")
            st.markdown("• Non-refundable period")
    
    with col2:
        st.markdown("**Cancellation Process:**")
        st.markdown("1. Request cancellation")
        st.markdown("2. Pay applicable fees")
        st.markdown("3. Receive refund confirmation")
        st.markdown("4. Refund processed in 7-14 days")
        
        if st.button("🚫 Cancel Booking", type="primary", use_container_width=True, key="cancel_booking_btn"):
            display_cancellation_form(booking)

def display_cancellation_form(booking):
    """Display booking cancellation form"""
    st.markdown("### ⚠️ Cancel Booking")
    
    st.warning("Are you sure you want to cancel this booking? This action cannot be undone.")
    
    # Cancellation reason
    cancellation_reason = st.selectbox(
        "Reason for Cancellation",
        [
            "Change of plans",
            "Medical emergency", 
            "Work commitment",
            "Family emergency",
            "Travel restrictions",
            "Other"
        ],
        key="cancellation_reason"
    )
    
    if cancellation_reason == "Other":
        other_reason = st.text_area("Please specify", key="other_cancellation_reason")
    
    # Refund method
    refund_method = st.radio(
        "Refund Method",
        ["Original payment method", "Bank transfer", "Travel voucher (+10% bonus)"],
        key="refund_method"
    )
    
    # Confirmation
    confirm_cancellation = st.checkbox(
        "I understand the cancellation policy and wish to proceed",
        key="confirm_cancellation"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("↩️ Keep Booking", use_container_width=True, key="keep_booking_btn"):
            st.success("Booking retained. No changes made.")
    
    with col2:
        if st.button("✅ Confirm Cancellation", type="primary", use_container_width=True, key="confirm_cancellation_btn"):
            if confirm_cancellation:
                st.success("Booking cancellation processed. Confirmation email sent.")
                st.balloons()
            else:
                st.error("Please confirm that you understand the cancellation policy.")
