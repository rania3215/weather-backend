# Weather App Backend + React Frontend

A full-stack weather application built with FastAPI and React.

The application allows users to search weather information for different locations, save weather records, view previous searches, export data, view maps, and check air quality.

---

## Features

### Weather
- Search current weather by location
- Temperature information
- Humidity information
- Weather description
- External API integration

### CRUD Operations
- Create weather records
- Read saved records
- Update locations
- Delete records

### Additional Features
- Interactive location map
- Air quality information
- Export data as CSV
- Export data as JSON
- Responsive dashboard UI

---

## Technologies

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- OpenWeather API

### Frontend
- React
- Vite
- JavaScript
- CSS

---

## Project Structure

│
├── app/
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── database.py
│ ├── weather_service.py
│ ├── air_quality_service.py
│ └── map_service.py
│
├── frontend/
│ ├── src/
│ └── package.json
│
├── requirements.txt
└── README.md

---

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


---

## Run Frontend

Go to frontend folder:
cd frontend


Install packages:
npm install

Run:
npm run dev

Frontend URL: http://localhost:5173


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /weather | Create weather record |
| GET | /weather | Get all records |
| GET | /weather/{id} | Get record |
| PUT | /weather/{id} | Update record |
| DELETE | /weather/{id} | Delete record |
| GET | /map/{location} | Get map location |
| GET | /export/csv | Export CSV |

---

## Done by :

Rania Adel Atmeh

