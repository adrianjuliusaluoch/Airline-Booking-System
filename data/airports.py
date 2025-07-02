# Airport information for Kenya Airways destinations
AIRPORTS = {
    "NBO": {
        "name": "Jomo Kenyatta International Airport",
        "city": "Nairobi",
        "country": "Kenya",
        "terminals": ["1A", "1B", "1C"],
        "facilities": ["Duty Free", "Restaurants", "Lounges", "WiFi", "ATM"],
        "image": "https://pixabay.com/get/g380a79f1050757a2fc8256ee8a9300119973c75c0ee0cf0107c374f4f963a99f7ded031ea55820175003d05b356bca7171d803303442003d93e89db31825b09d_1280.jpg"
    },
    "LGW": {
        "name": "London Gatwick Airport",
        "city": "London",
        "country": "United Kingdom",
        "terminals": ["North", "South"],
        "facilities": ["Duty Free", "Restaurants", "Lounges", "WiFi", "ATM", "Shopping"],
        "image": "https://pixabay.com/get/gbbb9b6cfb99dff26bc7c17a14392438dd5d489e4a361969f09a8607efe530d94da9dd9dde3c87574f3e578e9c640e67c61d986029f936560735bef213a8bfc94_1280.jpg"
    },
    "DXB": {
        "name": "Dubai International Airport",
        "city": "Dubai",
        "country": "UAE",
        "terminals": ["1", "2", "3"],
        "facilities": ["Duty Free", "Restaurants", "Lounges", "WiFi", "ATM", "Shopping", "Spa"],
        "image": "https://pixabay.com/get/gf37067b7e8e7dfa9059940d47e20102a00ff70125daf78c5632f21651774e966b7cfc2e451ae6b5991ad9d053b4db02c91b48af1fa148803ee56468b7af8fc8f_1280.jpg"
    },
    "AMS": {
        "name": "Amsterdam Airport Schiphol",
        "city": "Amsterdam",
        "country": "Netherlands",
        "terminals": ["1", "2", "3"],
        "facilities": ["Duty Free", "Restaurants", "Lounges", "WiFi", "ATM", "Shopping"],
        "image": "https://pixabay.com/get/g6b41d6a12ff6c318e50a5db59ad9518154d8e2977fb1d303fe75d2cd204145648e0413c7015c45c4877cc61e46f71d65f356de720e7ad1c66aac5b16058d40e0_1280.jpg"
    }
}

def get_airport_info(airport_code):
    """Get detailed airport information"""
    return AIRPORTS.get(airport_code, {
        "name": f"Airport {airport_code}",
        "city": "Unknown",
        "country": "Unknown",
        "terminals": ["Main"],
        "facilities": ["Basic Services"],
        "image": "https://pixabay.com/get/g380a79f1050757a2fc8256ee8a9300119973c75c0ee0cf0107c374f4f963a99f7ded031ea55820175003d05b356bca7171d803303442003d93e89db31825b09d_1280.jpg"
    })
