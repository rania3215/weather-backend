# Weather Backend API

A FastAPI weather application with CRUD operations,
database persistence, external API integration,
and data export functionality.

a- Technologies

 FastAPI ,Python ,SQLite ,SQLAlchemy ,OpenWeather API

b- Features

1. Get current weather by location
2. Store weather records in SQLite
3. CRUD operations:
4. Create weather records
5. Read weather history
6. Update records
7. Delete records
8. Location validation and geocoding
9. Map integration
10. Export data:
11. CSV
12. JSON

c- Run Project
step 1 Install dependencies:

pip install -r requirements.txt

step2 Run :

uvicorn app.main:app --reload

step3 API Documentation:

in your browser paste the link below :
http://127.0.0.1:8000/docs