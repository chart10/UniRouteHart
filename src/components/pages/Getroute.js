import React from 'react'
import Map from '../Map'
// Component: Route Finder
// Contains the forms needed to run a route query
/*global google*/

function Getroute() { 
 return(
    <div class="panel">
     <div>
      <input type="text" id="from" placeholder="origin"></input>
     </div>
     <div>
      <input type="text" id="dest" placeholder="destination"></input>
     </div>
     <b>Select type of Commute</b>
     <select id="mode">
      <option value="DRIVING">Driving</option>
      <option value="WALKING">Walking</option>
      <option value="BICYCLING">Bicycling</option>
      <option value="TRANSIT">Transit</option>
     </select>
    </div>
 ) 
 function initMap(){
  //create a DirectionsService object to use the route method and get a result for our request
  const directionsService = new google.maps.DirectionsService();
  //create a DirectionsRenderer object which we will use to display the route
  const directionsRenderer = new google.maps.DirectionsRenderer();
  const map = new google.maps.Map(document.getElementById("map"), Map);

  //bind the DirectionsRenderer to the map
directionsRenderer.setMap(map);

calculateAndDisplayRoute(directionsService, directionsRenderer);
//Allow the user to select what type of method of commute
document.getElementById("mode").addEventListener("change", ()=>{
  calculateAndDisplayRoute(directionsService, directionsRenderer);
})
}

function calculateAndDisplayRoute(directionsService, directionsRenderer){
  //This will allow the user to select the mode of traveling
  const selectedMode = document.getElementById("mode").value;

  directionsService.route({
    origin: document.getElementById("from").value,
    destination: document.getElementById("dest").value,

    travelMode: google.maps.TravelMode[selectedMode],
  })
  .then((response)=>{
    directionsRenderer.setDirections(response);
  })
  .catch((e) => window.alert("Directions request failed due to " ));
}
window.initMap = initMap;
}

export default Getroute
