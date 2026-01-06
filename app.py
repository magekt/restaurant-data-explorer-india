"""Restaurant Data Explorer - Python Flask Backend
Integrates multiple APIs (Geoapify, Zomato, Google Maps) for Indian restaurant data
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
from flask import Flask, request, jsonify
rom flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
ZOMATI_API_KEY = os.getenv('ZOMATO_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

class GeoapifyRestaurantFetcher:
    """Fetch restaurant data from Geoapify Places API (OSM-based)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.geoapify.com/v2/places"
    
    def search_restaurants(self, location: str, radius: int = 5000) -> List[Dict]:
        """Search for restaurants using Geoapify Places API"""
        try:
            # Geocode the location first
            geocode_url = "https://api.geoapify.com/v1/geocode/search"
            geocode_params = {
                "text": location,
                "apiKey": self.api_key,
                "limit": 1
            }
            geocode_response = requests.get(geocode_url, params=geocode_params, timeout=10)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
            
            if not geocode_data.get("features"):
                return []
            
            coords = geocode_data["features"][0]["geometry"]["coordinates"]
            lat, lon = coords[1], coords[0]
            
            # Search for restaurants
            params = {
                "lat": lat,
                "lon": lon,
                "radius": radius,
                "categories": "catering.restaurant",
                "limit": 50,
                "apiKey": self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            restaurants = []
            for place in data.get("features", []):
                props = place.get("properties", {})
                coords = place.get("geometry", {}).get("coordinates", [])
                
                restaurant = {
                    "name": props.get("name", "Unknown"),
                    "address": props.get("formatted", ""),
                    "latitude": coords[1] if len(coords) > 1 else None,
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "map_link": f"https://www.google.com/maps/?q={coords[1]},{coords[0]}" if len(coords) > 1 else None,
                    "rating": props.get("rating"),
                    "website": props.get("website"),
                    "phone": props.get("phone"),
                    "source": "Geoapify"
                }
                restaurants.append(restaurant)
            
            return restaurants
        
        except requests.exceptions.RequestException as e:
            print(f"Geoapify API Error: {str(e)}")
            return []

# Flask Application
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the HTML frontend"""
    return jsonify({"message": "Restaurant Data Explorer API", "version": "1.0", "endpoints": {"POST /api/restaurants": "Fetch restaurant data", "GET /api/health": "Health check"}})

@app.route('/api/restaurants', methods=['POST'])
def get_restaurants():
    """API endpoint to fetch restaurant data"""
    try:
        data = request.get_json()
        location = data.get('location', '').strip()
        api_provider = data.get('api_provider', 'geoapify')
        radius = data.get('radius', 5000)
        fields = data.get('fields', {})
        
        if not location:
            return jsonify({"error": "Location is required"}), 400
        
        if api_provider == "geoapify":
            fetcher = GeoapifyRestaurantFetcher(GEOAPIFY_API_KEY)
            restaurants = fetcher.search_restaurants(location, radius)
        else:
            restaurants = []
        
        # Filter fields
        filtered = []
        for restaurant in restaurants:
            filtered_rest = {"name": restaurant.get("name")}
            if fields.get("map"):
                filtered_rest["map_link"] = restaurant.get("map_link")
            if fields.get("rating"):
                filtered_rest["rating"] = restaurant.get("rating")
            filtered_rest["address"] = restaurant.get("address")
            filtered_rest["source"] = restaurant.get("source")
            filtered.append(filtered_rest)
        
        return jsonify({
            "success": True,
            "location": location,
            "restaurant_count": len(filtered),
            "restaurants": filtered,
            "api_provider": api_provider,
            "fetched_at": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
