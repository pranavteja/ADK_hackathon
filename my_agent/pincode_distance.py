from typing import Dict, Tuple

# Dummy coordinate mapping for Bengaluru Pincodes (approximate relative positions)
# In real application, use a Geocoding API or a proper database.
PINCODE_COORDS: Dict[str, Tuple[float, float]] = {
    "560038": (12.9719, 77.6412), # Indiranagar
    "560034": (12.9352, 77.6245), # Koramangala
    "560066": (12.9698, 77.7500), # Whitefield
    "560102": (12.9121, 77.6446), # HSR Layout
    "560041": (12.9250, 77.5938), # Jayanagar
    "560100": (12.8452, 77.6602), # Electronic City
    "560003": (13.0031, 77.5643), # Malleswaram
    "560076": (12.9166, 77.6101), # BTM Layout
    "560001": (12.9716, 77.5946), # MG Road / Central Bangalore
}

BANGALORE_CENTER = (12.9716, 77.5946)

AREA_MAP = {
    "indiranagar": "560038",
    "koramangala": "560034",
    "whitefield": "560066",
    "hsr layout": "560102",
    "hsr": "560102",
    "jayanagar": "560041",
    "electronic city": "560100",
    "malleswaram": "560003",
    "btm layout": "560076",
    "btm": "560076",
    "mg road": "560001",
    "central bangalore": "560001"
}

def get_coords(pincode: str) -> Tuple[float, float]:
    """Returns coords for pincode, defaulting to Central Bangalore for unknown 56xxxx pins."""
    if pincode in PINCODE_COORDS:
        return PINCODE_COORDS[pincode]
    if pincode and pincode.startswith('56'):
        return BANGALORE_CENTER
    return None

def resolve_pincode(query: str) -> str:
    """Tries to resolve an area name or pincode to a valid pincode string."""
    q = query.lower().strip()
    if q in AREA_MAP:
        return AREA_MAP[q]
    # Return as-is if it looks like a pincode, else None? 
    # For now let's assume if it's not in map but is digits, it's a pin.
    return query

def get_distance(pincode1: str, pincode2: str) -> float:
    """Calculates approximate Euclidean distance between two pincodes in Km."""
    p1 = get_coords(pincode1)
    p2 = get_coords(pincode2)
    
    if not p1 or not p2:
        return float('inf') # Infinite distance if unknown
    
    # 1 degree lat approx 111km, 1 degree lon approx 111km at equator (simplified)
    lat_diff = (p1[0] - p2[0]) * 111
    lon_diff = (p1[1] - p2[1]) * 111
    
    return (lat_diff**2 + lon_diff**2)**0.5

def find_nearby_pincodes(target_pincode: str, radius_km: float = 5.0) -> list[str]:
    """Returns a list of pincodes within the radius of the target."""
    nearby = []
    for pin in PINCODE_COORDS.keys():
        dist = get_distance(target_pincode, pin)
        if dist <= radius_km:
            nearby.append(pin)
    return nearby
