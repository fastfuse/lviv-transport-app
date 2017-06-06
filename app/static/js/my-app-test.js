
var osm = L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png"),

    mapboxLight = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFzdGZ1c2UiLCJhIjoiY2l1ZnN3cm0yMDAyczJ2dXZyYWZnaWVjciJ9.411LJ8YHIUYLmTGrfvfkLg"),

    mapboxStreets = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFzdGZ1c2UiLCJhIjoiY2l1ZnN3cm0yMDAyczJ2dXZyYWZnaWVjciJ9.411LJ8YHIUYLmTGrfvfkLg"),

    mapboxDark = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFzdGZ1c2UiLCJhIjoiY2l1ZnN3cm0yMDAyczJ2dXZyYWZnaWVjciJ9.411LJ8YHIUYLmTGrfvfkLg");


var baseMapLayers = {
    "Open Street Maps": osm,
    "Mapbox Streets": mapboxStreets,
    "Mapbox Light": mapboxLight,
    "Mapbox Dark": mapboxDark
};


var map = L.map('map', {
  center: [49.84104, 24.03164],
  zoom: 13,
  zoomControl: false,
  layers: [osm]
});

// ====================

var myLocation = L.layerGroup().addTo(map);

var myLocationIcon = L.icon({
    iconUrl: 'static/img/me.svg',
    iconSize:     [40, 40],
    iconAnchor:   [20, 40],
    popupAnchor:  [0, -35]
});


function onLocationFound(e) {
    myLocation.clearLayers();
    L.marker(e.latlng, {icon: myLocationIcon}).addTo(myLocation)
        .bindPopup("Ви тут").openPopup();
}

function onLocationError(e) {
    alert(e.message);
}


map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);
map.locate({setView: true, maxZoom: 16});


// =======================================

L.control.layers(baseMapLayers).addTo(map);


L.control.zoom({
  position: 'bottomright'
}).addTo(map);


var locateControl = L.control.locate({
  position: "bottomright",
  flyTo: true,
  drawCircle: true,
  follow: true,
  setView: true,
  keepCurrentZoomLevel: true,
  markerStyle: {
    weight: 1,
    opacity: 0.8,
    fillOpacity: 0.8
  },
  circleStyle: {
    weight: 1,
    clickable: false
  },
  metric: true,
  strings: {
    title: "My location (where am I?)",
    popup: "You are within {distance} {unit} from this point",
    outsideMapBoundsMsg: "You seem located outside the boundaries of the map"
  },
  locateOptions: {
    maxZoom: 18,
    watch: true,
    enableHighAccuracy: true,
    maximumAge: 10000,
    timeout: 10000
  }
}).addTo(map);


// ==================   Stops   ==========================

$.ajax({
    type: "GET",
    url: "static/data/city_stops.geojson",
    dataType: "json",
    success: function (response) {
      stops_layer = L.geoJSON(response,{
        onEachFeature: function(feature, layer){
          layer.bindPopup(feature.properties.code);
          layer.bindPopup('<a href="/info/'+feature.properties.code+'">'+feature.properties.name+' (табло)'+'</a> <br><br><button onclick=showVehicles("'+feature.properties.code+'")>Показати транспорт</button>');
        }
      })

      stops_clustered = L.markerClusterGroup();
      stops_clustered.addLayer(stops_layer);
      map.addLayer(stops_clustered);
    }
});


// ==================   Vehicles   ==========================

var vehicles = L.layerGroup().addTo(map);

var baseUrl = "https://lviv-transport-info.herokuapp.com/api/info/"

var vehicleIcon = L.icon({
    iconUrl: 'static/img/right-arrow.svg',
    iconSize:     [32, 32],
    iconAnchor:   [16, 16],
    popupAnchor:  [0, 0]
});



var refresh = null;

function showVehicles(stop_id){

  showTransport();
  if(refresh){
    clearInterval(refresh);
  }

  refresh = setInterval(showTransport, 8000);

  function showTransport(){
    var stopUrl = baseUrl + stop_id;

    $.get(stopUrl, function(data) {
      var answer = data;
      
      if(answer){
        vehicles.clearLayers();
        // map.setView(myLocation, 15);
        for(i=0; i<answer.length; i++){
          L.marker([answer[i].Y, answer[i].X],
                   {icon: vehicleIcon,
                    rotationAngle: answer[i].Angle})
                      .bindPopup(answer[i].RouteName + ' (' + 
                    + answer[i].VehicleName + ')<br> До: "' +
                    answer[i].IterationEnd + '"<br> Через: ' +
                    Math.floor(answer[i].TimeToPoint/60) + ' хв').addTo(vehicles);
        };
      }
      else{
        return;
      }
    }, "json");
  };
};
