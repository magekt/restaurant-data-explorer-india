# Restaurant Data Explorer - India

A Python-based web application to explore and fetch restaurant data across India using multiple APIs (Geoapify, Zomato, Google Maps). Features filtering, GMB detection, and social media integration.

## Features

✅ **Multiple API Support**: Geoapify, Zomato, Google Maps  
✅ **Hybrid Mode**: Combine results from multiple sources  
✅ **Selective Fields**: Choose which data to fetch (reduces API costs)  
✅ **GMB Detection**: Extract Google My Business profiles  
✅ **Social Links**: Fetch Instagram, Facebook, Twitter  
✅ **Established Year**: Track restaurant opening dates  
✅ **Map Integration**: Direct Google Maps links  
✅ **India-Optimized**: Specific support for Indian cities  
✅ **Responsive UI**: Mobile-friendly restaurant cards  
✅ **Easy Deployment**: Deploy on Render, Railway, or Heroku

## Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **APIs**: Geoapify, Zomato, Google Maps Places
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: Optional (can be integrated)
- **Deployment**: Render, Railway, Heroku

## Setup Instructions

### 1. Get API Keys

- **Geoapify** (Recommended): [https://myprojects.geoapify.com/](https://myprojects.geoapify.com/) → Free tier: 3,000 credits/day
- **Zomato** (Optional): [https://developers.zomato.com/](https://developers.zomato.com/) → May require approval
- **Google Maps** (Optional): [Google Cloud Console](https://console.cloud.google.com/) → Places API

### 2. Clone Repository

```bash
git clone https://github.com/magekt/restaurant-data-explorer-india.git
cd restaurant-data-explorer-india
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create `.env` File

Create a `.env` file in the project root:

```text
GEOAPIFY_API_KEY=your_geoapify_api_key
ZOMATI_API_KEY=your_zomato_api_key
GOOGLE_API_KEY=your_google_api_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### 6. Run Locally

```bash
python restaurant_api_backend.py
```

Visit `http://localhost:5000` in your browser.

## Deployment

### Deploy on Render (Recommended)

1. Push your code to GitHub
2. Go to [Render.com](https://render.com/)
3. Connect your GitHub account
4. Create a new Web Service
5. Select your repository
6. Set Build Command: `pip install -r requirements.txt`
7. Set Start Command: `gunicorn app:app`
8. Add environment variables from `.env`
9. Deploy!

### Deploy on Railway

1. Push to GitHub
2. Go to [Railway.app](https://railway.app/)
3. New Project → GitHub Repo
4. Select your repository
5. Add environment variables
6. Deploy automatically

### Deploy on Heroku

```bash
heroku login
heroku create your-app-name
heroku config:set GEOAPIFY_API_KEY=your_key
heroku config:set ZOMATO_API_KEY=your_key
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

## Project Structure

```
restaurant-data-explorer-india/
├── restaurant_api_backend.py    # Main Flask backend
├── index.html                    # Frontend UI
├── requirements.txt              # Python dependencies
├── Procfile                      # Heroku deployment config
├── runtime.txt                   # Python version
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── docs/                         # Documentation
    ├── API_USAGE.md
    └── DEPLOYMENT_GUIDE.md
```

## API Endpoints

### POST `/api/restaurants`

Fetch restaurant data from specified API provider.

**Request Body:**
```json
{
  "location": "Pune",
  "api_provider": "geoapify",
  "radius": 5000,
  "fields": {
    "name": true,
    "map": true,
    "rating": true,
    "established": false,
    "social": true,
    "gmb": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "location": "Pune",
  "restaurant_count": 42,
  "restaurants": [
    {
      "name": "Restaurant Name",
      "address": "Address",
      "map_link": "https://...",
      "rating": 4.5,
      "source": "Geoapify"
    }
  ],
  "api_provider": "geoapify",
  "fetched_at": "2024-01-05T21:00:00"
}
```

### GET `/api/health`

Health check endpoint.

## Cost Optimization Tips

1. **Use Geoapify free tier** (3k credits/day = ~300 searches/day)
2. **Implement caching** to reduce redundant API calls
3. **Batch requests** when possible
4. **Use field selection** to skip expensive enrichment
5. **Set appropriate search radius** to limit results

## Usage Examples

### Search restaurants in Pune with Geoapify

```python
from restaurant_api_backend import RestaurantDataFetcher

fetcher = RestaurantDataFetcher()
result = fetcher.fetch_restaurants(
    location="Pune",
    api_provider="geoapify",
    radius=5000,
    fields={
        "name": True,
        "map": True,
        "rating": True,
        "established": False,
        "social": True,
        "gmb": True
    }
)

print(f"Found {result['restaurant_count']} restaurants")
for restaurant in result['restaurants']:
    print(f"- {restaurant['name']} (Rating: {restaurant['rating']})")
```

## Troubleshooting

### "Failed to fetch restaurants"

- Check API key validity
- Verify internet connection
- Check rate limits on API
- Review API documentation for specific parameters

### "Location not found"

- Ensure location name is correct
- Try full city name (e.g., "Pune, Maharashtra, India")
- Check Geoapify location support

### CORS errors

- Flask-CORS is configured to allow all origins
- If using custom domain, update CORS settings in `restaurant_api_backend.py`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GEOAPIFY_API_KEY | API key from Geoapify | Yes |
| ZOMATO_API_KEY | API key from Zomato | No |
| GOOGLE_API_KEY | API key from Google Cloud | No |
| FLASK_ENV | Environment (development/production) | No |
| FLASK_DEBUG | Enable debug mode | No |

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open-source and available under the MIT License.

## Support

For issues, questions, or suggestions:

- Open an [issue](https://github.com/magekt/restaurant-data-explorer-india/issues)
- Check existing issues for solutions
- Review API documentation

## Roadmap

- [ ] Add Redis caching
- [ ] Implement CSV/Excel export
- [ ] Add database integration (PostgreSQL)
- [ ] Create admin dashboard
- [ ] Add more restaurant APIs
- [ ] Implement advanced filtering
- [ ] Add mobile app
- [ ] Multi-language support

## Changelog

### v1.0.0 (2024-01-05)

- Initial release
- Geoapify integration
- Zomato integration (basic)
- Google Maps integration (basic)
- Flask backend with CORS
- Responsive HTML UI
- Deployment guides
