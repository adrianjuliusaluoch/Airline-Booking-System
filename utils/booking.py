import random
import string
from datetime import datetime

def generate_booking_reference():
    """Generate a unique booking reference"""
    return 'KQ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_ticket_number():
    """Generate a ticket number"""
    return '629-' + ''.join(random.choices(string.digits, k=10))

def calculate_total_price(flights, passengers, extras=None):
    """Calculate total booking price"""
    total = 0
    
    for flight in flights:
        for passenger in passengers:
            travel_class = passenger.get('class', 'Economy')
            total += flight['prices'][travel_class]
    
    # Add extras (baggage, meals, etc.)
    if extras:
        total += sum(extras.values())
    
    return total

def generate_seat_map(aircraft_model, travel_class):
    """Generate seat map for aircraft"""
    seat_configs = {
        "Boeing 787-8": {
            "Economy": {"rows": 39, "seats_per_row": "ABCDEFGHJ", "pitch": "31-32 inches"},
            "Business": {"rows": 5, "seats_per_row": "ABEF", "pitch": "60 inches"}
        },
        "Boeing 737-800": {
            "Economy": {"rows": 27, "seats_per_row": "ABCDEF", "pitch": "30-31 inches"},
            "Business": {"rows": 2, "seats_per_row": "ABEF", "pitch": "40 inches"}
        },
        "Boeing 777-300ER": {
            "Economy": {"rows": 50, "seats_per_row": "ABCDEFGHJK", "pitch": "32-34 inches"},
            "Business": {"rows": 7, "seats_per_row": "ABEF", "pitch": "78 inches"},
            "First": {"rows": 1, "seats_per_row": "AB", "pitch": "84 inches"}
        }
    }
    
    config = seat_configs.get(aircraft_model, seat_configs["Boeing 737-800"])
    class_config = config.get(travel_class, config["Economy"])
    
    seats = []
    occupied_seats = set()
    
    # Randomly occupy some seats
    total_seats = class_config["rows"] * len(class_config["seats_per_row"])
    num_occupied = random.randint(int(total_seats * 0.3), int(total_seats * 0.7))
    
    for _ in range(num_occupied):
        row = random.randint(1, class_config["rows"])
        seat_letter = random.choice(class_config["seats_per_row"])
        occupied_seats.add(f"{row}{seat_letter}")
    
    for row in range(1, class_config["rows"] + 1):
        for seat_letter in class_config["seats_per_row"]:
            seat_id = f"{row}{seat_letter}"
            seat_type = "window" if seat_letter in "AK" else "aisle" if seat_letter in "CF" else "middle"
            
            seats.append({
                "seat_id": seat_id,
                "row": row,
                "letter": seat_letter,
                "type": seat_type,
                "available": seat_id not in occupied_seats,
                "price": 0 if travel_class != "Economy" else (25 if seat_type == "window" else 15 if seat_type == "aisle" else 0)
            })
    
    return {
        "seats": seats,
        "config": class_config,
        "aircraft": aircraft_model
    }

def validate_passenger_info(passenger):
    """Validate passenger information"""
    errors = []

    if not isinstance(passenger, dict):
        errors.append("Invalid passenger data format.")
        return errors
    
    required_fields = ['first_name', 'last_name', 'date_of_birth', 'nationality', 'passport_number']
    
    for field in required_fields:
        if not passenger.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Validate passport number format (basic)
    if passenger.get('passport_number') and len(passenger['passport_number']) < 6:
        errors.append("Passport number must be at least 6 characters")
    
    # Validate date of birth
    if passenger.get('date_of_birth'):
        try:
            dob_value = passenger['date_of_birth']
            if isinstance(dob_value, datetime):
                birth_date = dob_value
            elif isinstance(dob_value, str):
                birth_date = datetime.strptime(dob_value, '%Y-%m-%d')
            else:
                raise ValueError("Unsupported date format")

            if birth_date > datetime.now():
                errors.append("Date of birth cannot be in the future")
        except Exception:
            errors.append("Invalid date of birth format")
    
    return errors

def create_booking(booking_data):
    """Create a new booking"""
    booking = {
        "booking_reference": generate_booking_reference(),
        "created_at": datetime.now().isoformat(),
        "status": "Confirmed",
        "flights": booking_data["flights"],
        "passengers": booking_data["passengers"],
        "contact": booking_data["contact"],
        "total_price": booking_data["total_price"],
        "payment_status": "Paid",
        "tickets": []
    }
    
    # Generate tickets for each passenger
    for passenger in booking_data["passengers"]:
        ticket = {
            "ticket_number": generate_ticket_number(),
            "passenger_name": f"{passenger['first_name']} {passenger['last_name']}",
            "seat": passenger.get("seat", "Not assigned"),
            "class": passenger.get("class", "Economy"),
            "special_requests": passenger.get("special_requests", [])
        }
        booking["tickets"].append(ticket)
    
    return booking
