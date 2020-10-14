 mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW5weHFjMG5wYzJ6bWF6YzByOW51NSJ9.LwHvv8n_x3PInD9_CbCfZg';
  var current_marker;
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [30.50, 50.40],
    zoom: 6,
  });

  var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    marker: false,
    placeholder: 'Search',
  });

  map.addControl(geocoder);

  geocoder.on('result', function(ev) {
    document.getElementById('id_address').value = ev.result.place_name;
    document.getElementById('id_latitude').value = ev.result.geometry.coordinates[0];
    document.getElementById('id_longitude').value = ev.result.geometry.coordinates[1];

    if (current_marker!=null)
        current_marker.remove()
      current_marker = new mapboxgl.Marker()
      .setLngLat([ev.result.geometry.coordinates[0],ev.result.geometry.coordinates[1]])
      .addTo(map);
  });

map.on('click', function(e) {
    if (current_marker!=null)
        current_marker.remove()

    var marker = new mapboxgl.Marker()
    .setLngLat(e.lngLat)
    .addTo(map);

    current_marker = marker;

    document.getElementById('id_latitude').value = JSON.stringify(e.lngLat['lat']);
    document.getElementById('id_longitude').value = JSON.stringify(e.lngLat['lng']);
});
