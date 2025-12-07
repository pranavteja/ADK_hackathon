import csv
import os
from typing import List, Dict, Optional, Tuple
from .pincode_distance import get_distance, resolve_pincode

# Get directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCOMING_JOBS_CSV = os.path.join(BASE_DIR, 'gig_jobs.csv')
HISTORICAL_JOBS_CSV = os.path.join(BASE_DIR, 'historical_jobs.csv')
PROFILES_CSV = os.path.join(BASE_DIR, 'worker_profiles.csv')

def read_csv(filepath: str) -> List[Dict]:
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def analyze_historical_rates(trade: str, description_keywords: str) -> str:
    """
    Analyzes historical jobs to estimate costs based on similarity.
    """
    history = read_csv(HISTORICAL_JOBS_CSV)
    similar_jobs = []
    
    keywords = description_keywords.lower().split()
    
    for job in history:
        # Match Trade
        if trade.lower() in job['trade'].lower():
            # Simple keyword matching for description similarity
            job_desc = job['job_description'].lower()
            match_count = sum(1 for k in keywords if k in job_desc)
            if match_count > 0 or not keywords: # If no keywords, return general trade stats
                job['match_score'] = match_count
                similar_jobs.append(job)
                
    if not similar_jobs:
        return f"No historical data found for {trade} matching '{description_keywords}'."
        
    # Sort by match score
    similar_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
    top_jobs = similar_jobs[:5]
    
    rates = [float(j['final_rate_charged']) for j in top_jobs]
    avg_rate = sum(rates) / len(rates)
    max_rate = max(rates)
    min_rate = min(rates)
    
    return (f"Historical Analysis for '{trade}' ({len(similar_jobs)} matches):\n"
            f"- Avg Final Cost: ₹{avg_rate:.2f}\n"
            f"- Range: ₹{min_rate} - ₹{max_rate}\n"
            f"- Similar Job: {top_jobs[0]['job_description']} in {top_jobs[0].get('area', 'Unknown')} (Charged: ₹{top_jobs[0]['final_rate_charged']})")


def _get_historical_estimate(trade: str, desc: str) -> str:
    """Helper to get a quick rate range string for a job."""
    # We reuse analyze logic but simplified returning just the range string
    history = read_csv(HISTORICAL_JOBS_CSV)
    similar_rates = []
    keywords = desc.lower().split()
    
    for h in history:
        if trade.lower() in h['trade'].lower():
            # Check for decent overlap or just general trade stats
            if any(k in h['job_description'].lower() for k in keywords):
                 similar_rates.append(float(h['final_rate_charged']))
                 
    if not similar_rates:
        # Fallback to all trade jobs if no keyword match
        similar_rates = [float(h['final_rate_charged']) for h in history if trade.lower() in h['trade'].lower()]
        
    if not similar_rates:
        return "N/A"
        
    avg = sum(similar_rates) / len(similar_rates)
    return f"₹{min(similar_rates):.0f} - ₹{max(similar_rates):.0f} (Avg: ₹{avg:.0f})"

def search_jobs(category: str, location_query: Optional[str] = None, range_km: float = 20.0) -> str:
    """
    Searches for INCOMING jobs from gig_jobs.csv.
    """
    jobs = read_csv(INCOMING_JOBS_CSV)
    results = []
    
    if not category or not category.strip():
        return "ERROR: Missing Trade/Category."

    resolved_pincode = resolve_pincode(location_query) if location_query else None

    # Typos: We trust the agent handles 'plumbinng' -> 'Plumber' via LLM logic usually.
    # But let's be safe: simple substring match
    
    for job in jobs:
        # Robust check: if 'plum' in category, match Plumber? 
        # Better: let's rely on loose text match
        if category.lower() in job['required_trade'].lower():
            results.append(job)
            
    # Distance Filter
    if resolved_pincode:
        nearby_jobs = []
        for job in results:
            job_pincode = job.get('location_zip', '')
            dist = get_distance(resolved_pincode, job_pincode)
            if dist <= range_km:
                job['distance'] = dist
                nearby_jobs.append(job)
        nearby_jobs.sort(key=lambda x: x['distance'])
        results = nearby_jobs
    
    if not results:
        return f"No incoming jobs found for {category}.do you want to search for other area?"

    output = f"Incoming Jobs ({len(results)}):\n"
    for job in results:
        dist_info = f" ({job['distance']:.1f} km)" if 'distance' in job else ""
        urgency = job.get('urgency_level', 'Normal')
        area = job.get('area', 'Unknown Area')
        contact = job.get('contact_number', 'N/A')
        
        # Calculate dynamic estimate
        est_rate = _get_historical_estimate(job['required_trade'], job['problem_description'])
        
        output += (f"- ID: {job['job_id']} [{urgency} Urgency] @ {area} ({job['location_zip']}){dist_info}\n"
                   f"  Problem: {job['problem_description']}\n"
                   f"  Est. Rate: {est_rate}\n"
                   f"  Contact Owner: {contact}\n")
    return output

def list_all_jobs() -> str:
    jobs = read_csv(INCOMING_JOBS_CSV)
    output = "All Incoming Jobs:\n"
    for job in jobs:
        output += f"- {job['job_id']}: {job['problem_description']} ({job['required_trade']})\n"
    return output

def check_worker_availability(trade: str, pincode: str) -> str:
    """Finds available workers for a specific trade and location."""
    workers = read_csv(PROFILES_CSV)
    available = []
    
    resolved_pincode = resolve_pincode(pincode)
    if not resolved_pincode: 
        return "Invalid location."
        
    for w in workers:
        if trade.lower() in w['trade'].lower() and w['is_available'] == 'True':
             # Distance check
            dist = get_distance(resolved_pincode, w['service_area_zip'])
            if dist < 15:
                w['distance'] = dist
                available.append(w)
                
    if not available:
        return "No accessible workers available right now."
        
    output = f"Available {trade}s near {pincode} ({resolve_pincode(pincode) or 'Location'}):\n"
    for w in available:
        area = w.get('area', w['service_area_zip'])
        output += (f"- {w['name']} ({area}) - Rating: {w['rating_average']}\n"
                   f"  Level: {w['expertise_level']} - Rate: ₹{w['base_hourly_rate']}/hr\n")
    return output
