/*!***************************************************
 * OpenStreetMap with Leaflet
 *****************************************************/
function map() {
  var mapElement = document.getElementById("map");
  
  if (mapElement != null) {
    var latitude = parseFloat(mapElement.getAttribute("data-latitude"));
    var longitude = parseFloat(mapElement.getAttribute("data-longitude"));
    var mapMarker = mapElement.getAttribute("data-marker");
    var mapMarkerName = mapElement.getAttribute("data-marker-name");
    
    // Initialize the map
    var map = L.map('map').setView([latitude, longitude], 15);
    
    // Add OpenStreetMap tiles with grayscale style
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);
    
    // Create custom icon if marker image is provided
    var markerIcon = L.icon({
      iconUrl: mapMarker,
      iconSize: [30, 40],
      iconAnchor: [15, 40],
      popupAnchor: [0, -40]
    });
    
    // Add marker
    var marker = L.marker([latitude, longitude], {
      icon: markerIcon,
      title: mapMarkerName
    }).addTo(map);
    
    // Optionally add a popup
    if (mapMarkerName) {
      marker.bindPopup(mapMarkerName);
    }
  }
}

// Initialize map when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', map);
} else {
  map();
}
