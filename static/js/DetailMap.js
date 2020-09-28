mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW51ZDVkMGg2dzJyb2Y2Y2lrenp2NCJ9.suxwFu99fm3uh2F-EdNcxw';

function showUser(longitude, latitude)
{
var map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [longitude, latitude], // starting position [lng, lat]
zoom: 5 // starting zoom
});

var lng = parseFloat(longitude)
var lat = parseFloat(latitude)

var ll = new mapboxgl.LngLat(lng,lat);

var marker = new mapboxgl.Marker()
.setLngLat(ll)
.addTo(map);
}


