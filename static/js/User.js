function showUser(longitude, latitude)
{
 mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW5weHFjMG5wYzJ6bWF6YzByOW51NSJ9.LwHvv8n_x3PInD9_CbCfZg';
  var current_marker;
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [longitude, latitude],
    zoom: 6,
  });
var marker = new mapboxgl.Marker()
        .setLngLat([longitude, latitude])
        .addTo(map);
        }