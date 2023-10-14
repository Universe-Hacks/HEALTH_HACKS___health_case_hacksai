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

  console.log(selectedCities, 'selectedCities')


  /*  if (selectedCities) {
      const coords: LatLngTuple = selectedCities.map(item => {
        return [item.coordinate.latitude, item.coordinate.longitude]
      })

      console.log(coords, 'coords')

      setCoord(coords as LatLngTuple)
    }*/


  return (
    <MapContainer center={[3213, 321]} zoom={10}>
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
