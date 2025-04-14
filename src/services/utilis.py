from datetime import datetime
from tzlocal import get_localzone
import geocoder
from dotenv import load_dotenv
import os
import json
import spacy
import geocoder
from transformers import pipeline

def get_current_datetime():
    """Auto-detects user's system time with timezone"""
    tz = get_localzone()
    now = datetime.now(tz)
    
    # Get the timezone name directly from the tzinfo object
    timezone_name = tz.zone if hasattr(tz, 'zone') else str(tz)
    
    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "timezone": timezone_name
    }
#...........run this when testing locally
def get_user_location():
    g = geocoder.ip("me")   #get the IP adress of the server
    if g.ok:
        # Check if 'timezone' is available, otherwise use a default
        timezone = g.timezone if hasattr(g, 'timezone') else 'UTC'  # Default to UTC if no timezone
        return {
            "longitude": g.lng,
            "latitude": g.lat,
            "city": g.city,
            "nation": g.country,
            "timezone": timezone
        }
    else:
        raise Exception("❌ Unable to detect location. Check your internet connection.")

#...............if using ios run this instead to get the IP adress of the client
"""
from fastapi import Request

def get_user_location_from_request(request: Request):
    client_ip = request.client.host
    g = geocoder.ip(client_ip)
    if g.ok:
        timezone = g.timezone if hasattr(g, 'timezone') else 'UTC'  # Default to UTC if no timezone
        return {
            "longitude": g.lng,
            "latitude": g.lat,
            "city": g.city,
            "nation": g.country,
            "timezone": timezone
        }
    else:
        raise Exception("❌ Unable to detect location.")
"""

# Load the spaCy model for text processing
nlp = spacy.load("en_core_web_sm")


# Load zero-shot classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_question(question: str):
    labels = [
        "Horoscope", "Compatibility", "Zodiac Sign Analysis", "Past Life Reading",
        "Birth Chart Interpretation", "Transit Forecast", "House System",
        "Planetary Aspects", "Career Astrology", "Financial Astrology",
        "Relationship Forecast", "Electional Astrology", "Medical Astrology", "Spiritual Astrology"
    ]
    
    # Run zero-shot classification
    result = classifier(question, labels)
    intent = result["labels"][0]  # Get the highest-confidence label
    
    # Mapping astrology attributes based on intent
    astrology_mapping = {
        "Horoscope": ("Tropic", "Apparent Geocentric", "P"),
        "Compatibility": ("Tropic", "Heliocentric", "W"),
        "Zodiac Sign Analysis": ("Tropic", "Apparent Geocentric", "P"),
        "Past Life Reading": ("Sidereal", "Sidereal Geocentric", "W"),
        "Birth Chart Interpretation": ("Tropic", "Apparent Geocentric", "P"),
        "Transit Forecast": ("Tropic", "Apparent Geocentric", "P"),
        "House System": ("Tropic", "Apparent Geocentric", "E"),  # Direct question about house system
        "Planetary Aspects": ("Tropic", "Apparent Geocentric", "P"),
        "Career Astrology": ("Tropic", "Apparent Geocentric", "P"),
        "Financial Astrology": ("Tropic", "Apparent Geocentric", "P"),
        "Relationship Forecast": ("Tropic", "Apparent Geocentric", "W"),
        "Electional Astrology": ("Tropic", "Apparent Geocentric", "R"),
        "Medical Astrology": ("Tropic", "Apparent Geocentric", "P"),
        "Spiritual Astrology": ("Sidereal", "Sidereal Geocentric", "W")
    }
    
    # Get astrology attributes (default to Placidus if unknown)
    zodiac_type, perspective_type, houses_system_identifier = astrology_mapping.get(intent, ("Tropic", "Apparent Geocentric", "Placidus"))

    return {
        "intent": intent,
        "zodiac_type": zodiac_type,
        "perspective_type": perspective_type,
        "houses_system_identifier": houses_system_identifier
    }
