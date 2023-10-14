import "leaflet/dist/leaflet.css";
import {MapContainer, TileLayer} from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import {DataCities} from "../../pickerCity/types";

type MapProps = {
  selectedCities: DataCities[]
};

function Map(props: MapProps) {

  const {
    selectedCities,
  } = props

  console.log(selectedCities, '227')

  const coord = selectedCities.map(item => {
    return [item.coordinate.latitude, item.coordinate.longitude]
  })

  console.log(...coord, 'coord')

  return (
    <MapContainer center={[56.8389, 60.6057]} zoom={10}>
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
