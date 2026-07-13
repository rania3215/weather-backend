import { useState } from "react";
import "./App.css";

function App() {

  const [location, setLocation] = useState("");
  const [weather, setWeather] = useState(null);
  const [records, setRecords] = useState([]);
  const [map, setMap] = useState(null);
  const [airQuality, setAirQuality] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  // CREATE
  const getWeather = async () => {

  setLoading(true);
  setError("");

  try {

    const response = await fetch(
      "http://127.0.0.1:8000/weather",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          location: location,
          start_date: "2026-07-13",
          end_date: "2026-07-13"
        })
      }
    );


    if (!response.ok) {
      throw new Error("Location not found");
    }


    const data = await response.json();

    setWeather(data);


  } catch (err) {

    setError(err.message);

  }
  finally {

    setLoading(false);

  }

};


  // READ
  const getRecords = async () => {

    const response = await fetch(
      "http://127.0.0.1:8000/weather"
    );

    const data = await response.json();

    setRecords(data);
  };
const deleteRecord = async (id) => {

  await fetch(
    `http://127.0.0.1:8000/weather/${id}`,
    {
      method: "DELETE"
    }
  );

  getRecords();

};
const updateRecord = async (id) => {

  const newLocation = prompt(
    "Enter new location:"
  );


  if (!newLocation) return;


  await fetch(
    `http://127.0.0.1:8000/weather/${id}?location=${newLocation}`,
    {
      method: "PUT"
    }
  );


  getRecords();

};

const exportCSV = () => {

  window.open(
    "http://127.0.0.1:8000/export/csv",
    "_blank"
  );

};
const exportJSON = () => {

  const file = new Blob(
    [
      JSON.stringify(records, null, 2)
    ],
    {
      type: "application/json"
    }
  );


  const url = URL.createObjectURL(file);


  const link = document.createElement("a");

  link.href = url;

  link.download = "weather_data.json";

  link.click();

};

const getMap = async () => {

  const response = await fetch(
    `http://127.0.0.1:8000/map/${location}`
  );

  const data = await response.json();

  setMap(data);

};

const getAirQuality = async () => {

  const response = await fetch(
    `http://127.0.0.1:8000/air-quality/${location}`
  );

  const data = await response.json();

  setAirQuality(data);

};

const getAQIStatus = (aqi) => {

  if (aqi === 1) return "Good 🟢";
  if (aqi === 2) return "Fair 🟡";
  if (aqi === 3) return "Moderate 🟠";
  if (aqi === 4) return "Poor 🔴";
  if (aqi === 5) return "Very Poor 🟣";

  return "Unknown";

};
  return (
    <div className="container">

      <h1>Weather </h1>


      <input
        placeholder="Enter location"
        value={location}
        onChange={(e)=>setLocation(e.target.value)}
      />


      <button onClick={getWeather}>
        Get Weather
      </button>
      {loading && (

<p>
Loading weather data... ⏳
</p>

)}
{error && (

<p className="error">
❌ {error}
</p>

)}
      <button onClick={getMap}>
        Show Map
      </button>


      <button onClick={getAirQuality}>
        Air Quality
      </button>

{weather && (

<div className="card weather-info">

<h2>
📍 {weather.location}
</h2>


<div className="temperature">

{weather.description.includes("clear")
?
"☀️"
:
"☁️"
}

<h1>
{weather.temperature} °C
</h1>

</div>


<p>
💧 Humidity:
{weather.humidity} %
</p>


<p>
🌤️ {weather.description}
</p>


</div>

)}



      <hr/>
{map && (

<div className="card">

<h2>
📍 {map.location} Map
</h2>


<iframe

title="location-map"

width="100%"

height="350"

style={{
  border: "0",
  borderRadius: "15px"
}}

loading="lazy"

src={`https://www.openstreetmap.org/export/embed.html?bbox=${map.longitude-0.05}%2C${map.latitude-0.05}%2C${map.longitude+0.05}%2C${map.latitude+0.05}&layer=mapnik&marker=${map.latitude}%2C${map.longitude}`}

>

</iframe>


<br/>


<a
href={map.map_url}
target="_blank"
rel="noreferrer"
>
Open Full Map
</a>


</div>

)}

{airQuality && (

<div className="card air-card">

<h2>
🌿 Air Quality
</h2>

<p>
📍 Location: {airQuality.location}
</p>

<p>
🌎 Country: {airQuality.country}
</p>


<h3>
Air Quality Data
</h3>


<p>
AQI: {getAQIStatus(airQuality.air_quality.aqi)}
</p>

<p>
CO: {airQuality.air_quality.co}
</p>

<p>
NO₂: {airQuality.air_quality.no2}
</p>

<p>
PM2.5: {airQuality.air_quality.pm2_5}
</p>

<p>
O₃: {airQuality.air_quality.o3}
</p>


</div>

)}
      <button onClick={exportCSV}>
        Download CSV
      </button>


      <button onClick={exportJSON}>
        Download JSON
      </button>

      <button onClick={getRecords}>
        Show Previous Searches
      </button>

         <div className="container">
      <h2>
        Previous Searches
      </h2>
         </div>

      <table border="1">

        <thead>
          <tr>
            <th>ID</th>
            <th>Location</th>
            <th>Temperature</th>
            <th>Humidity</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>


        <tbody>

        {
          records.map((record)=>(
            <tr key={record.id}>

              <td>{record.id}</td>

              <td>{record.location}</td>

              <td>
                {record.temperature}
              </td>

              <td>
                {record.humidity}
              </td>

              <td>
                {record.description}
              </td>
             <td>
              <button
                onClick={() => updateRecord(record.id)}
              >
                Update
              </button>
            </td>

              <td>
                <button
                  onClick={() => deleteRecord(record.id)}
                >
                  Delete
                </button>
              </td>

            </tr>
          ))
        }

        </tbody>

      </table>


    </div>
  );
}


export default App;