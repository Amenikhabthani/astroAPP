from services.llm_service import model  
import requests
from services.utilis import get_current_datetime, get_user_location, classify_question
from services.llm_service import generate_interpretation
from dotenv import load_dotenv
import os
# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ASTRO_API_KEY")
API_URL = "https://astrologer.p.rapidapi.com/api/v4/natal-aspects-data"
HEADERS = {
    "X-RapidAPI-Host": "astrologer.p.rapidapi.com",
    "X-RapidAPI-Key": API_KEY,
    "Content-Type": "application/json"
}

def process_natal_aspects_request(question: str, datetime: dict = None, location: dict = None):
    """Processes the astrology request by detecting missing values and querying the API"""

    # 🔮 Classify question to modify request parameters
    config = classify_question(question)
    if not isinstance(config, dict):  # Ensure config is always a dictionary
        raise ValueError("Invalid classification response. Expected a dictionary.")
    # 📅 Get datetime if missing
    if datetime is None:
        datetime = get_current_datetime()

    # 📍 Get location if missing
    if location is None:
        location = get_user_location()

    # 📝 Construct API request body
    request_body = {
        "subject": {
            "year": datetime["year"],
            "month": datetime["month"],
            "day": datetime["day"],
            "hour": datetime["hour"],
            "minute": datetime["minute"],
            "longitude": location["longitude"],
            "latitude": location["latitude"],
            "city": location["city"],
            "nation": location["nation"],
            "timezone": location["timezone"],
            "name": "user",
            "zodiac_type": config.get("zodiac_type"),
            "sidereal_mode": None,
            "perspective_type": config.get("perspective_type"),
            "houses_system_identifier": config.get("houses_system_identifier")
        },
        "theme": "classic",
        "language": "EN",
        "wheel_only": False
    }

    # 🚀 Call the astrology API
    response = requests.post(API_URL, json=request_body, headers=HEADERS)

    # ✅ Handle API response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.text}")

def get_natal_chart(question: str, datetime: dict, location: dict):
    return process_natal_aspects_request(question, datetime, location)

def summarize_chart(data: dict, max_aspects: int = 5, include_houses: bool = True) -> str:
    """Generate a comprehensive astrological chart summary.
    
    Args:
        data: The chart data dictionary
        max_aspects: Maximum number of aspects to display
        include_houses: Whether to include house positions
    
    Returns:
        Formatted multi-line string summary
    """
    summary = []
    
    # 1. Basic Info Header
    if 'subject' in data:
        subject = data['subject']
        summary.append(
            f"### Birth Details for {subject.get('name', 'Unknown')}\n"
            f"- Date/Time: {subject.get('iso_formatted_local_datetime', 'Unknown')}\n"
            f"- Location: {subject.get('city', 'Unknown')}, {subject.get('nation', 'Unknown')}\n"
            f"- House System: {subject.get('houses_system_name', 'Unknown')}\n"
            f"- Zodiac Type: {subject.get('zodiac_type', 'Unknown')}\n"
        )
    
    # 2. Planetary Positions Table
    planets = [
        'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
        'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
        'Chiron', 'Mean_Node'
    ]
    
    planet_rows = []
    for planet in planets:
        if planet in data:
            p = data[planet]
            retro = " (R)" if p.get('retrograde') else ""
            planet_rows.append(
                f"| {planet.ljust(8)} | {p['emoji']} {p['sign']} | "
                f"{round(p['position'], 2):>6}° | "
                f"{p.get('house', '').replace('_', ' ').ljust(12)} |"
                f"{retro.ljust(4)} |"
            )
    
    if planet_rows:
        summary.append(
            "\n### Planetary Positions\n"
            "| Planet   | Sign     | Pos   | House       | Ret |\n"
            "|----------|----------|-------|-------------|-----|"
        )
        summary.extend(planet_rows)
    
    # 3. Key Angles
    angles = []
    for angle in ['Ascendant', 'Descendant', 'Medium_Coeli', 'Imum_Coeli']:
        if angle in data:
            a = data[angle]
            angles.append(f"- {angle.replace('_', ' ')}: {a['emoji']} {a['sign']} {round(a['position'], 2)}°")
    
    if angles:
        summary.append("\n### Angular Points")
        summary.extend(angles)
    
    # 4. Aspects Analysis
    if 'aspects' in data and isinstance(data['aspects'], list):
        aspects = sorted(
            data['aspects'],
            key=lambda x: abs(x.get('orbit', 10)),
        )[:max_aspects]
        
        aspect_lines = []
        for aspect in aspects:
            p1 = aspect.get('p1_name', '?')
            p2 = aspect.get('p2_name', '?')
            aspect_type = aspect.get('aspect', 'aspect')
            orb = round(abs(aspect.get('orbit', 0)), 2)
            
            # Only show tight aspects (orb < 3° by default)
            if orb <= 3:
                aspect_lines.append(f"- {p1} {aspect_type} {p2} (orb: {orb}°)")
        
        if aspect_lines:
            summary.append("\n### Key Aspects (Tightest Orbs)")
            summary.extend(aspect_lines)
    
    # 5. Special Features
    special = []
    
    # Check for stelliums (3+ planets in one house)
    house_counts = {}
    for planet in data.values():
        if isinstance(planet, dict) and 'house' in planet:
            house_counts[planet['house']] = house_counts.get(planet['house'], 0) + 1
    
    for house, count in house_counts.items():
        if count >= 3:
            special.append(f"- Stellium in {house.replace('_', ' ')} ({count} planets)")
    
    # Check lunar phase if available
    if 'lunar_phase' in data:
        phase = data['lunar_phase']
        special.append(
            f"- Moon Phase: {phase.get('moon_phase_name', 'Unknown')} "
            f"{phase.get('moon_emoji', '')} "
            f"(Sun-Moon angle: {round(phase.get('degrees_between_s_m', 0), 1)}°)"
        )
    
    if special:
        summary.append("\n### Notable Features")
        summary.extend(special)
    
    return "\n".join(summary)

def format_astrology_prompt(summary, question, history=None):
    prompt_template = """You are a friendly traditional astrologer answering in clear, simple language. 
Translate complex concepts into everyday terms while staying true to William Lilly's methods and John Frawley rules.

**Rules:**
- Write like you're explaining to a smart friend (no jargon without explanation)
- Use simple metaphors for astrological concepts
- Keep under 150 words
- Always give a clear bottom-line answer first

**Response Template:**
[Main answer] "Yes/No/Probably, because..."
[1-2 plain English reasons from the chart]
[Any important timing clues]
[Reassuring closing note]

**Example Marriage Answer:**
"Likely yes! Your relationship house shows good potential with Venus in a strong position, though there may be some delays from Saturn's influence. The Moon's movement suggests things should improve within about a year. This looks like a case of 'good things come to those who wait.'"

**Current Chart Details:**
{summary}

**Question:** {question}

**Your Interpretation:**"""
    return prompt_template.format(summary=summary, question=question)
