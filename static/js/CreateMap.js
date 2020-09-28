//
//mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW51ZDVkMGg2dzJyb2Y2Y2lrenp2NCJ9.suxwFu99fm3uh2F-EdNcxw';
//var current_marker;
//
//var map = new mapboxgl.Map({
//container: 'map',
//style: 'mapbox://styles/mapbox/streets-v11',
//center: [30.50, 50.40],
//zoom: 5
//});
//
//var geocoder = new MapboxGeocoder({ // Initialize the geocoder
//  accessToken: mapboxgl.accessToken, // Set the access token
//  mapboxgl: mapboxgl, // Set the mapbox-gl instance
//  marker: false, // Do not use the default marker style
//});
//
//map.addControl(geocoder);
//console.log(geocoder)
//
//map.on('click', function(e) {
//
//if (current_marker!=null)
//current_marker.remove()
//
//console.log('A click event has occurred at ' + e.lngLat);
//var marker = new mapboxgl.Marker()
//.setLngLat(e.lngLat)
//.addTo(map);
//
//console.log(e.lngLat)
//
//current_marker = marker;
//
//document.getElementById('id_latitude').value = JSON.stringify(e.lngLat['lat']);
//document.getElementById('id_longitude').value = JSON.stringify(e.lngLat['lng']);
//
//
//});
 mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW5weHFjMG5wYzJ6bWF6YzByOW51NSJ9.LwHvv8n_x3PInD9_CbCfZg';
  var map = new mapboxgl.Map({
    container: 'map', // Container ID
    style: 'mapbox://styles/mapbox/streets-v11', // Map style to use
    center: [30.50, 50.40], // Starting position [lng, lat]
    zoom: 6, // Starting zoom level
  });

//  var marker = new mapboxgl.Marker() // Initialize a new marker
//    .setLngLat([-122.25948, 37.87221]) // Marker [lng, lat] coordinates
//    .addTo(map); // Add the marker to the map

  var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    marker: false,
    placeholder: 'Search',
  });

  map.addControl(geocoder);

  map.on('load', function() {
    map.addSource('single-point', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: []
      }
    });

    map.addLayer({
      id: 'point',
      source: 'single-point',
      type: 'circle',
      paint: {
        'circle-radius': 10,
        'circle-color': '#448ee4'
      }
    });

    geocoder.on('result', function(ev) {
      document.getElementById('id_address').value = ev.result.place_name;
      document.getElementById('id_latitude').value = ev.result.geometry.coordinates[0];
      document.getElementById('id_longitude').value = ev.result.geometry.coordinates[1];
      map.getSource('single-point').setData(ev.result.geometry);
    });
  });