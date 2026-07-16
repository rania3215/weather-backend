# Weather Application

## Features

 Current Weather by city name
 Weather using user's current location.
 5-Day Weather Forecast.
 Air Quality Index (AQI).
 Interactive Map Integration.
 YouTube Travel Recommendations.
 Weather Search History.
 CRUD Operations.
 Export Weather Data (CSV / JSON).
 Responsive Glassmorphism UI.
 Error Handling.

## Technologies

Frontend:
React.

Backend:
FastAPI.

Database:
SQLite.

APIs:
OpenWeather.
YouTube.
OpenStreetMap.


## Project Structure


 app/
  main.py
  models.py
  schemas.py
  crud.py
  database.py
  weather_service.py
  air_quality_service.py
  map_service.py

 frontend/
   src/
    package.json
  requirements.txt
  README.md

## Environment Variables

Create a config.py file:
OPENWEATHER_API_KEY="your_api_key"
YOUTUBE_API_KEY="your_api_key"

## Run Backend

Create virtual environment:
  python -m venv venv
  
  Activate:
  Windows:
  venv\Scripts\activate

Install dependencies:
 pip install -r requirements.txt

Run:
uvicorn app.main:app --reload
Backend URL:http://127.0.0.1:8000
API Documentation:http://127.0.0.1:8000/docs




## Run Frontend

Go to frontend folder:
cd frontend


Install packages:
npm install

Run:
npm run dev

Frontend URL: http://localhost:5173

## API Endpoints

 Method , Endpoint , Description :

 POST , /weather , Create weather record 
 GET , /weather , Get all weather records 
 GET , /weather/{id} , Get weather record by id 
 PUT , /weather/{id} , Update weather record 
 DELETE  /weather/{id} , Delete weather record 
 GET , /forecast/{location} , Get 5-day forecast 
 GET , /map/{location} , Get map coordinates 
 GET , /map-coordinates/{lat}/{lon} , Map using coordinates :
 GET , /air-quality/{location} , Get air quality 
 GET , /air-quality-coordinates/{lat}/{lon} , Air quality by coordinates :
 GET , /youtube/{location} , Get YouTube videos 
 GET , /export/csv , Export CSV file 
 GET  /export/json , Export JSON data 

## Database

The application uses SQLite with SQLAlchemy ORM.

Stored data includes:
Location.
Temperature.
Humidity.
Weather description.
Search history.

## Future Improvements

User authentication.
Weather alerts.
More weather providers.
Interactive weather charts.
Deployment using Docker and cloud services.

## Author

Developed by **Rania Adel Atmeh**

Weather App built for PM Accelerator Technical Assessment.

