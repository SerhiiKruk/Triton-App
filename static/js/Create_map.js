
mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW51ZDVkMGg2dzJyb2Y2Y2lrenp2NCJ9.suxwFu99fm3uh2F-EdNcxw';
var current_marker;

var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [30.50, 50.40],
zoom: 5
});

var geocoder = new MapboxGeocoder({
accessToken: mapboxgl.accessToken,
marker: {
color: 'orange'
},
mapboxgl: mapboxgl
});

map.on('click', function(e) {

if (current_marker!=null)
current_marker.remove()

console.log('A click event has occurred at ' + e.lngLat);
var marker = new mapboxgl.Marker()
.setLngLat(e.lngLat)
.addTo(map);

console.log(e.lngLat)

current_marker = marker;

document.getElementById('id_latitude').value = JSON.stringify(e.lngLat['lat']);
document.getElementById('id_longitude').value = JSON.stringify(e.lngLat['lng']);


});
