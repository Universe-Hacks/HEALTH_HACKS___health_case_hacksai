import "leaflet/dist/leaflet.css";
import {MapContainer, TileLayer} from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";

function Map() {

  return (
    <MapContainer center={[55.7558, 37.6176]} zoom={4}>
      {/* Установите координаты центра и масштаб так, чтобы охватить Россию */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MarkerClusterGroup chunkedLoading>
        {/* Здесь можно добавить маркеры для различных точек в России */}
      </MarkerClusterGroup>
    </MapContainer>
  );
}

export default Map
