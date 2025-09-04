const map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap'
}).addTo(map);

const info = document.getElementById('info')
document.getElementById('load').onclick = async () => {
  const resp = await fetch('/api/trees', { method: 'POST' });
  const data = await resp.json();
  info.textContent = JSON.stringify(data.features.slice(0,5), null, 2)
  const layer = L.geoJSON(data, {
    onEachFeature: (feature, layer) => {
      layer.bindPopup(`Tree ${feature.properties.label}<br/>Height: ${feature.properties.height.toFixed(2)} m`)
    }
  }).addTo(map);
  map.fitBounds(layer.getBounds());
}


