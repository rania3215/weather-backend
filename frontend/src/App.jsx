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
  const [forecast, setForecast] = useState([]);
  const [locationLoading, setLocationLoading] = useState(false);
  const [coordinates, setCoordinates] = useState(null);
  const [videos, setVideos] = useState([]);
  
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
          location: location
        
        })
      }
    );


    if (!response.ok) {

      const errorData = await response.json();

      throw new Error(
        errorData.detail || "Location not found"
      );

    }


    const data = await response.json();


    setWeather(data);
    setLocation(data.location);
    

    // Get searched location coordinates
    const locationResponse = await fetch(
      `http://127.0.0.1:8000/location/${data.location}`
    );


    const locationData = await locationResponse.json();


    setCoordinates({
      latitude: locationData.latitude,
      longitude: locationData.longitude
    });


    setMap(null);
    setAirQuality(null);
    setForecast([]);


    getYoutubeVideos(data.location);


  } catch (err) {

    setError(err.message);

  } finally {

    setLoading(false);

  }

};

const getForecast = async () => {

  try {

    const response = await fetch(
      `http://127.0.0.1:8000/forecast/${location}`
    );


    const data = await response.json();


    setForecast(data.forecast);


  } catch (error) {

    console.log(error);

  }

};
const getYoutubeVideos = async (place) => {

  try {

    const response = await fetch(
      `http://127.0.0.1:8000/youtube/${place}`
    );

    const data = await response.json();

    console.log("YOUTUBE DATA:", data);

    setVideos(data.videos);

  } catch(error) {

    console.log("YOUTUBE ERROR:", error);

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
const exportXML = () => {

  window.open(
    "http://127.0.0.1:8000/export/xml",
    "_blank"
  );

};
const getMap = async () => {

  try {

    let response;

   
    if (coordinates) {

      response = await fetch(
        `http://127.0.0.1:8000/map-coordinates/${coordinates.latitude}/${coordinates.longitude}`
      );

    } else {

      response = await fetch(
        `http://127.0.0.1:8000/map/${location}`
      );

    }

    const data = await response.json();

    setMap(data);

  } catch (err) {

    console.log(err);

  }

};


const getAirQuality = async () => {

  try {

    let response;

    if (coordinates) {

      response = await fetch(
        `http://127.0.0.1:8000/air-quality-coordinates/${coordinates.latitude}/${coordinates.longitude}`
      );

    } else {

      response = await fetch(
        `http://127.0.0.1:8000/air-quality/${location}`
      );

    }

    if (!response.ok) {
      throw new Error("Air quality not found");
    }

    const data = await response.json();

    setAirQuality(data);

  } catch (err) {

    console.log(err);

  }

};

const getAQIStatus = (aqi) => {

  if (aqi === 1) return "Good 🟢";
  if (aqi === 2) return "Fair 🟡";
  if (aqi === 3) return "Moderate 🟠";
  if (aqi === 4) return "Poor 🔴";
  if (aqi === 5) return "Very Poor 🟣";

  return "Unknown";

};
const getCurrentLocation = () => {


setLocationLoading(true);


navigator.geolocation.getCurrentPosition(

async(position)=>{


const lat = position.coords.latitude;
const lon = position.coords.longitude;

setCoordinates({
  latitude: lat,
  longitude: lon
});

const response = await fetch(

`http://127.0.0.1:8000/weather/location/${lat}/${lon}`

);


const data = await response.json();


setWeather(data);
setLocation(data.location);
setMap(null);
setAirQuality(null);
setForecast([]);
setLocationLoading(false);
getYoutubeVideos(data.location);

},


(error)=>{


alert("Location permission denied");


setLocationLoading(false);


}


);


};

  return (
    <div className="container">

      <h1>Weather </h1>


       <input
  placeholder="Enter location"
  value={location}
  onChange={(e) => setLocation(e.target.value)}
/>




      <button onClick={getWeather}>
        Get Weather
      </button>
      <button onClick={getCurrentLocation}>

       📍 Use My Location

      </button>
 {locationLoading && (

<p>
Getting your location... 
</p>

)}
      {loading && (

<p>
Loading weather data... ⏳
</p>

)}
{error && (

<p className="error">
 {error}
</p>

)}
      <button onClick={getMap}>
        Map
      </button>


      <button onClick={getAirQuality}>
        Air Quality
      </button>


{weather && (

<div className="card">

<h2>
📍 {weather.location}
</h2>


<div className="temperature">

{weather?.description?.includes("clear")
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

<div className="card">

<h2>
🌿 Air Quality
</h2>
  <p>
📍 Location: {location}
  </p>







<p>
AQI: {airQuality.air_quality?.aqi ?? "-"} (
{getAQIStatus(airQuality.air_quality?.aqi)}
)
</p>


<p>
CO: {airQuality.air_quality?.co ?? "-"}
</p>


<p>
NO₂: {airQuality.air_quality?.no2 ?? "-"}
</p>


<p>
PM2.5: {airQuality.air_quality?.pm2_5 ?? "-"}
</p>


<p>
O₃: {airQuality.air_quality?.o3 ?? "-"}
</p>


</div>

)}

{forecast.length > 0 && (

<div className="card">

<h2>
📅 5 Day Forecast
</h2>


<div className="forecast-container">


{forecast.map((item, index) => (

<div className="card" key={index}>


<h3>
{item.date}
</h3>


<p>
🌡️ {item.temperature} °C
</p>


<p>
🌤️ {item.description}
</p>


</div>

))}


</div>

</div>

)}

      <button onClick={getForecast}>
        5 Day Forecast
      </button>
      <button onClick={getRecords}>
        Show Previous Searches
      </button>
      <button onClick={exportCSV}>
        Download CSV
      </button>
      <button onClick={exportJSON}>
        Download JSON
      </button>
      <button onClick={exportXML}>
       Download XML
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
            <th>      </th>
            <th>      </th>
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
{videos.length > 0 && (

<div className="card">
<h2>
 you may also like these videos about {location}
</h2>

<div className="videos-container">

{videos.map((video,index)=>(

<div key={index} className="video-card">

<img
src={video.thumbnail}
alt={video.title}
/>

<h3>
{video.title}
</h3>

<a
href={video.url}
target="_blank"
rel="noreferrer"
>
Watch Video
</a>

</div>

))}

</div>

</div>

)}

<footer className="footer">

<h3>
Developed by Rania Atmeh
</h3>

<p>
Weather App built for PM Accelerator Technical Assessment.
</p>

<p>
PM Accelerator helps professionals build product management skills
through training, mentorship, and career opportunities.
</p>

</footer>
    </div>
  );
}


export default App;