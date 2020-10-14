let map
function init(){
mapboxgl.accessToken = 'pk.eyJ1IjoiamltbXk4OTgiLCJhIjoiY2tmOW51ZDVkMGg2dzJyb2Y2Y2lrenp2NCJ9.suxwFu99fm3uh2F-EdNcxw';
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [0, 0],
        zoom: 3
    });
}

function addcoordinates(lng,lat, fullname){
      var popup = new mapboxgl.Popup({ offset: 25 }).setText(
        fullname
      );
      var marker = new mapboxgl.Marker({'color':getColor()})
        .setLngLat([lng,lat])
        .setPopup(popup)
        .addTo(map);
}

function getColor()
{
randomNumber = getRandomInt(1118481);
hexString = randomNumber.toString(16);

let i = 0;
while(i<6-hexString.length)
{
hexString += '0'
i++;
}

random_color = "#" + hexString
return random_color
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

