import streamlit as st
from utils.booking import generate_seat_map
from utils.session import get_search_params

def show():
    st.markdown("## 💺 Select Your Seats")
    
    if not st.session_state.booking_data:
        st.info("Please complete the booking process first.")
        return
    
    booking_data = st.session_state.booking_data
    flights = booking_data['flights']
    total_passengers = booking_data['total_passengers']
    travel_class = booking_data['travel_class']
    
    # Initialize seat selections if not exists
    if not st.session_state.seat_selections:
        st.session_state.seat_selections = {}
    
    # Display seat selection for each flight
    for i, flight in enumerate(flights):
        st.markdown(f"### Flight {flight['flight_number']} - {flight['origin']} to {flight['destination']}")
        
        # Generate seat map
        seat_map = generate_seat_map(flight['aircraft'], travel_class)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            display_seat_map(seat_map, flight['flight_number'], total_passengers)
        
        with col2:
            display_seat_info(seat_map, flight['flight_number'])
    
    # Calculate additional seat fees
    seat_fees = calculate_seat_fees()
    
    if seat_fees > 0:
        st.markdown(f"### Additional Seat Fees: ${seat_fees}")
    
    # Continue to passenger information
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Skip Seat Selection", use_container_width=True, key="skip_seat_selection"):
            st.info("Seats will be assigned automatically at check-in.")
            # Continue without seat selection
    
    with col2:
        if st.button("Continue with Selected Seats", type="primary", use_container_width=True, key="continue_with_seats"):
            # Validate seat selections
            if validate_seat_selections(flights, total_passengers):
                # Update booking data with seat selections
                booking_data['seat_selections'] = st.session_state.seat_selections
                booking_data['seat_fees'] = seat_fees
                booking_data['total_price'] += seat_fees
                
                st.success("Seat selections confirmed!")
                st.rerun()
            else:
                st.error("Please select seats for all passengers or skip seat selection.")

def display_seat_map(seat_map, flight_number, total_passengers):
    """Display interactive seat map"""
    seats = seat_map['seats']
    config = seat_map['config']
    
    st.markdown(f"**{seat_map['aircraft']} - {config['pitch']} seat pitch**")
    
    # Group seats by row
    rows = {}
    for seat in seats:
        row = seat['row']
        if row not in rows:
            rows[row] = []
        rows[row].append(seat)
    
    # Display seat map
    selected_seats = st.session_state.seat_selections.get(flight_number, [])
    
    # Seat legend
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🟢 Available")
    with col2:
        st.markdown("🔴 Occupied")
    with col3:
        st.markdown("🟡 Selected")
    with col4:
        st.markdown("💰 Premium (+fee)")
    
    # Display seats in a grid-like format
    for row_num in sorted(rows.keys())[:10]:  # Show first 10 rows for demo
        cols = st.columns(len(rows[row_num]) + 1)
        
        with cols[0]:
            st.markdown(f"**{row_num}**")
        
        for i, seat in enumerate(rows[row_num]):
            with cols[i + 1]:
                seat_id = seat['seat_id']
                
                # Determine seat color and status
                if seat_id in selected_seats:
                    emoji = "🟡"
                    disabled = True
                elif not seat['available']:
                    emoji = "🔴"
                    disabled = True
                elif seat['price'] > 0:
                    emoji = f"💰"
                    disabled = False
                else:
                    emoji = "🟢"
                    disabled = False
                
                # Seat selection button
                if st.button(
                    f"{emoji}\n{seat['letter']}",
                    key=f"seat_{flight_number}_{seat_id}",
                    disabled=disabled,
                    help=f"Row {seat['row']}, Seat {seat['letter']} - {seat['type'].title()} seat" + 
                         (f" (+${seat['price']})" if seat['price'] > 0 else "")
                ):
                    if len(selected_seats) < total_passengers:
                        if flight_number not in st.session_state.seat_selections:
                            st.session_state.seat_selections[flight_number] = []
                        st.session_state.seat_selections[flight_number].append(seat_id)
                        st.rerun()
                    else:
                        st.warning(f"You can only select {total_passengers} seat(s) for this flight.")

def display_seat_info(seat_map, flight_number):
    """Display seat selection information"""
    config = seat_map['config']
    
    st.markdown("**Seat Information**")
    st.markdown(f"• Seat pitch: {config['pitch']}")
    st.markdown(f"• Rows: {config['rows']}")
    
    # Selected seats for this flight
    selected_seats = st.session_state.seat_selections.get(flight_number, [])
    
    if selected_seats:
        st.markdown("**Selected Seats:**")
        for seat in selected_seats:
            if st.button(f"Remove {seat}", key=f"remove_{flight_number}_{seat}"):
                st.session_state.seat_selections[flight_number].remove(seat)
                st.rerun()
    
    st.markdown("**Seat Types:**")
    st.markdown("• Window: Best views")
    st.markdown("• Aisle: Easy access")
    st.markdown("• Middle: Budget option")
    
    # Seat fees information
    st.markdown("**Seat Fees:**")
    st.markdown("• Window seats: +$25")
    st.markdown("• Aisle seats: +$15")
    st.markdown("• Middle seats: Free")

def calculate_seat_fees():
    """Calculate additional fees for selected seats"""
    total_fees = 0
    
    for flight_number, seats in st.session_state.seat_selections.items():
        for seat_id in seats:
            # Simple fee calculation based on seat type
            seat_letter = seat_id[-1]
            if seat_letter in 'AK':  # Window seats
                total_fees += 25
            elif seat_letter in 'CF':  # Aisle seats
                total_fees += 15
            # Middle seats are free
    
    return total_fees

def validate_seat_selections(flights, total_passengers):
    """Validate that seat selections are complete"""
    for flight in flights:
        flight_number = flight['flight_number']
        selected_seats = st.session_state.seat_selections.get(flight_number, [])
        
        if len(selected_seats) != total_passengers and len(selected_seats) > 0:
            return False
    
    return True
