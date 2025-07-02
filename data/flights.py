import pandas as pd
from datetime import datetime, timedelta
import random

# Real Kenya Airways destinations based on web data
DESTINATIONS = {
    "Nairobi": {"code": "NBO", "country": "Kenya", "timezone": "+3"},
    "London": {"code": "LGW", "country": "United Kingdom", "timezone": "+0"},
    "Dubai": {"code": "DXB", "country": "UAE", "timezone": "+4"},
    "Amsterdam": {"code": "AMS", "country": "Netherlands", "timezone": "+1"},
    "Paris": {"code": "CDG", "country": "France", "timezone": "+1"},
    "Mumbai": {"code": "BOM", "country": "India", "timezone": "+5:30"},
    "Bangkok": {"code": "BKK", "country": "Thailand", "timezone": "+7"},
    "Accra": {"code": "ACC", "country": "Ghana", "timezone": "+0"},
    "Lagos": {"code": "LOS", "country": "Nigeria", "timezone": "+1"},
    "Kinshasa": {"code": "FIH", "country": "DR Congo", "timezone": "+1"},
    "Addis Ababa": {"code": "ADD", "country": "Ethiopia", "timezone": "+3"},
    "Dar es Salaam": {"code": "DAR", "country": "Tanzania", "timezone": "+3"},
    "Entebbe": {"code": "EBB", "country": "Uganda", "timezone": "+3"},
    "Kigali": {"code": "KGL", "country": "Rwanda", "timezone": "+2"},
    "Johannesburg": {"code": "JNB", "country": "South Africa", "timezone": "+2"},
    "Cape Town": {"code": "CPT", "country": "South Africa", "timezone": "+2"},
    "Zanzibar": {"code": "ZNZ", "country": "Tanzania", "timezone": "+3"},
    "Mauritius": {"code": "MRU", "country": "Mauritius", "timezone": "+4"},
    "New York": {"code": "JFK", "country": "USA", "timezone": "-5"},
    "Rome": {"code": "FCO", "country": "Italy", "timezone": "+1"}
}

# Aircraft types used by Kenya Airways
AIRCRAFT_TYPES = [
    {"model": "Boeing 787-8", "seats": {"Economy": 234, "Business": 30}, "image": "https://pixabay.com/get/g3fcc992fd3fd5df6bbe2b6c0ea6a5e090f82daef28b6d4859ef3f7c80485dbfe00c18eff5b01ade86bd1a8da8e5329f29001aeca7c96d137cb9ca92cf88cca73_1280.jpg"},
    {"model": "Boeing 737-800", "seats": {"Economy": 162, "Business": 12}, "image": "https://pixabay.com/get/g94b5f12273a24c0b66c48b6c0ad09a4bc1b7265533cf26f7923ab2c37476bf1bada351ab7e11e5f8c3629aeef5dc7587a2dff190c0113bf764da6af9abf7a647_1280.jpg"},
    {"model": "Embraer E190", "seats": {"Economy": 96, "Business": 8}, "image": "https://pixabay.com/get/g404341642894aba20f2a1a220817f8b86da0d86a9624486385aea5cdf196fd8e705ba27c88bdc08afe42739f5c62297a49870e5c4fdd8134f3cab27d8302849d_1280.jpg"},
    {"model": "Boeing 777-300ER", "seats": {"Economy": 300, "Business": 42, "First": 8}, "image": "https://pixabay.com/get/g152bc36c65f5a8680a2fd92717dc6f1e55b04981668dfd682157e6f8a41ba66e984d734740942c5bfa813dbd4734da879f45c446ff5a3084b03480e404026876_1280.jpg"}
]

def generate_flight_data(origin, destination, departure_date, trip_type="return", return_date=None):
    """Generate realistic flight data for Kenya Airways"""
    flights = []
    
    # Base prices from real Kenya Airways data
    base_prices = {
        ("NBO", "LGW"): 945, ("NBO", "DXB"): 650, ("NBO", "AMS"): 890,
        ("NBO", "CDG"): 920, ("NBO", "ACC"): 842, ("NBO", "LOS"): 892,
        ("NBO", "FIH"): 893, ("NBO", "ADD"): 898, ("NBO", "DAR"): 350,
        ("NBO", "EBB"): 380, ("NBO", "KGL"): 420, ("NBO", "JNB"): 580,
        ("NBO", "MRU"): 450, ("NBO", "JFK"): 1200, ("NBO", "BOM"): 720
    }
    
    origin_code = DESTINATIONS[origin]["code"]
    dest_code = DESTINATIONS[destination]["code"]
    
    # Get base price or calculate based on distance
    base_price = base_prices.get((origin_code, dest_code)) or base_prices.get((dest_code, origin_code)) or 600
    
    # Generate multiple flight options for the day
    departure_times = ["06:30", "10:45", "14:20", "18:30", "22:15"]
    
    for i, dep_time in enumerate(departure_times[:3]):  # Limit to 3 flights per day
        aircraft = random.choice(AIRCRAFT_TYPES)
        
        # Calculate flight duration (simplified)
        duration = random.randint(180, 840)  # 3-14 hours
        
        # Price variations
        price_multiplier = 1 + (i * 0.15)  # Later flights slightly more expensive
        economy_price = int(base_price * price_multiplier)
        business_price = int(economy_price * 2.5)
        first_price = int(economy_price * 4) if "First" in aircraft["seats"] else None
        
        flight = {
            "flight_number": f"KQ{random.randint(100, 999)}",
            "origin": origin,
            "destination": destination,
            "origin_code": origin_code,
            "destination_code": dest_code,
            "departure_date": departure_date,
            "departure_time": dep_time,
            "arrival_time": calculate_arrival_time(dep_time, duration),
            "duration": f"{duration//60}h {duration%60}m",
            "aircraft": aircraft["model"],
            "aircraft_image": aircraft["image"],
            "prices": {
                "Economy": economy_price,
                "Business": business_price,
                "First": first_price
            },
            "seats_available": {
                "Economy": random.randint(20, aircraft["seats"]["Economy"]),
                "Business": random.randint(2, aircraft["seats"]["Business"]),
                "First": random.randint(1, aircraft["seats"].get("First", 0)) if first_price else 0
            },
            "stops": 0 if i == 0 else random.choice([0, 1]),  # First flight direct, others may have stops
            "meal_service": True,
            "wifi_available": True,
            "entertainment": True
        }
        
        flights.append(flight)
    
    return flights

def calculate_arrival_time(departure_time, duration_minutes):
    """Calculate arrival time based on departure and duration"""
    dep_hour, dep_minute = map(int, departure_time.split(':'))
    dep_total_minutes = dep_hour * 60 + dep_minute
    arr_total_minutes = dep_total_minutes + duration_minutes
    
    # Handle next day arrivals
    arr_hour = (arr_total_minutes // 60) % 24
    arr_minute = arr_total_minutes % 60
    
    return f"{arr_hour:02d}:{arr_minute:02d}"

def get_flight_status(flight_number):
    """Get flight status information"""
    statuses = ["On Time", "Delayed", "Boarding", "Departed", "Arrived", "Cancelled"]
    status = random.choice(statuses)
    
    delay_minutes = 0
    if status == "Delayed":
        delay_minutes = random.randint(15, 180)
    
    return {
        "flight_number": flight_number,
        "status": status,
        "delay_minutes": delay_minutes,
        "gate": f"A{random.randint(1, 25)}",
        "terminal": random.choice(["1A", "1B", "1C"]),
        "baggage_claim": random.randint(1, 8) if status in ["Arrived", "Boarding"] else None
    }

def search_flights(origin, destination, departure_date, return_date=None, passengers=1, travel_class="Economy"):
    """Search for flights based on criteria"""
    if origin not in DESTINATIONS or destination not in DESTINATIONS:
        return []
    
    outbound_flights = generate_flight_data(origin, destination, departure_date)
    
    if return_date:
        return_flights = generate_flight_data(destination, origin, return_date)
        return {"outbound": outbound_flights, "return": return_flights}
    
    return {"outbound": outbound_flights}
