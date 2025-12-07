from typing import Dict, Tuple, Optional

# Approximate Lat/Lon for Demo purposes (Clustered by region)
# Central: 12.97, 77.59
# North (Hebbal/Yelahanka): 13.05, 77.60
# South (Jayanagar/BTM): 12.91, 77.60
# East (Whitefield/Indiranagar): 12.98, 77.66
# West (Rajajinagar/Malleshwaram): 13.00, 77.55

PINCODE_COORDS = {
    # Central
    "560001": (12.9716, 77.5946), "560009": (12.9750, 77.5700), "560025": (12.9700, 77.6000),
    "560046": (13.0000, 77.6000), "560052": (12.9900, 77.5900), "560002": (12.9600, 77.5800),
    # North
    "560003": (13.0031, 77.5643), "560006": (13.0200, 77.5900), "560024": (13.0300, 77.5900),
    "560032": (13.0200, 77.6000), "560064": (13.1000, 77.6000), "560092": (13.0600, 77.5800),
    "560094": (13.0400, 77.5800), "560097": (13.0800, 77.5600), "560022": (13.0300, 77.5500),
    # South
    "560004": (12.9400, 77.5700), "560011": (12.9300, 77.5800), "560034": (12.9350, 77.6200),
    "560041": (12.9200, 77.5800), "560050": (12.9200, 77.5500), "560060": (12.9000, 77.5000),
    "560070": (12.9100, 77.5700), "560076": (12.9166, 77.6101), "560078": (12.9000, 77.5900),
    "560083": (12.8700, 77.5900), "560100": (12.8452, 77.6602), "560102": (12.9100, 77.6400),
    "560035": (12.9100, 77.7000),
    # East
    "560007": (12.9600, 77.6200), "560008": (12.9700, 77.6300), "560017": (12.9600, 77.6500),
    "560037": (12.9500, 77.7000), "560038": (12.9784, 77.6408), "560048": (12.9900, 77.6800),
    "560066": (12.9700, 77.7200), "560093": (12.9800, 77.6700), "560103": (12.9300, 77.6800),
    "560016": (13.0100, 77.6700), "560043": (13.0200, 77.6500),
    # West
    "560010": (12.9900, 77.5500), "560040": (12.9600, 77.5300), "560058": (13.0300, 77.5200),
    "560072": (12.9600, 77.5100), "560079": (12.9800, 77.5400), "560098": (12.9300, 77.5100),
    "560044": (12.9800, 77.5400)
}

BANGALORE_CENTER = (12.9716, 77.5946)

AREA_MAP = {
    "bangalore": "560001", "bengaluru": "560001",
    "bangalore gpo": "560001", "basavanagudi": "560004", "fraser town": "560005", "jc nagar": "560006",
    "agram": "560007", "hal 2nd stage": "560008", "hal": "560008", "gandhinagar": "560009", "kg road": "560009",
    "rajajinagar": "560010", "jayanagar": "560041", "jayanagar 4th block": "560011", "vasanth nagar": "560052",
    "benson town": "560046", "banaswadi": "560043", "btm layout": "560076", "btm": "560076", "bannerghatta": "560083",
    "banashankari": "560050", "basaveshwaranagar": "560079", "koramangala": "560034", "indiranagar": "560038",
    "whitefield": "560066", "marathahalli": "560037", "hsr layout": "560102", "hsr": "560102", "electronic city": "560100",
    "bellandur": "560103", "hebbal": "560024", "yelahanka": "560064", "kodigehalli": "560092", "hennur": "560043",
    "horamavu": "560043", "kr puram": "560036", "ramamurthy nagar": "560016", "jp nagar": "560078",
    "nagarbhavi": "560072", "peenya": "560058", "rr nagar": "560098", "malleswaram": "560003",
    "shivajinagar": "560051", "mg road": "560001", "ulsoor": "560008", "domlur": "560071",
    "airport road": "560017", "murugeshpalya": "560017", "kadubeesanahalli": "560103", "kundalahalli": "560037",
    "mahadevapura": "560048", "hoodi": "560048", "kaggadasapura": "560093", "cv raman nagar": "560093",
    "bellary road": "560032", "ganganagar": "560032", "rt nagar": "560032", "sadashivanagar": "560080",
    "vidyaranyapura": "560097", "sahakar nagar": "560092", "sanjay nagar": "560094", "kalyan nagar": "560043",
    "hrbr layout": "560043", "hbr layout": "560043", "lingarajapuram": "560084", "thanisandra": "560077",
    "nagawara": "560045", "hebbal kempapura": "560024", "yeshwanthpur": "560022", "vijayanagar": "560040",
    "chandra layout": "560040", "kengeri": "560060", "attibele": "562107", "sarjapur road": "560035",
    "harlur road": "560102", "kasavanahalli": "560035"
}

def get_coords(pincode: str) -> Tuple[float, float]:
    """Returns coords for pincode, using explicit map or falling back."""
    if pincode in PINCODE_COORDS:
        return PINCODE_COORDS[pincode]
    if pincode and pincode.startswith('56'):
        return BANGALORE_CENTER
    return None

import difflib

def resolve_pincode(query: str) -> str:
    """Tries to resolve an area name or pincode to a valid pincode string.
       Supports fuzzy matching for typos (e.g. 'indiranager' -> 'indiranagar').
    """
    q = query.lower().strip()
    
    # 1. Exact Match
    if q in AREA_MAP:
        return AREA_MAP[q]
        
    # 2. Fuzzy Match
    # Cutoff 0.6 allows for reasonable typos (e.g. "indiranagr") without too many false positives
    matches = difflib.get_close_matches(q, AREA_MAP.keys(), n=1, cutoff=0.6)
    if matches:
        return AREA_MAP[matches[0]]
        
    return query

def get_distance(pincode1: str, pincode2: str) -> float:
    """Calculates approximate Euclidean distance between two pincodes in Km."""
    p1 = get_coords(pincode1)
    p2 = get_coords(pincode2)
    
    if not p1 or not p2:
        return float('inf') # Infinite distance if unknown
    
    # 1 degree lat approx 111km, 1 degree lon approx 111km at equator (simplified)
    # Adjust lon degree length for Bangalore latitude (~13 deg): cos(13) ~= 0.97
    lat_diff = (p1[0] - p2[0]) * 111
    lon_diff = (p1[1] - p2[1]) * 111 * 0.97
    
    return (lat_diff**2 + lon_diff**2)**0.5
