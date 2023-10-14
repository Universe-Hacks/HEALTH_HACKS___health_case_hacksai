import "leaflet/dist/leaflet.css";
import {TileLayer, useMapEvent} from "react-leaflet";
import {useEffect, useState} from "react";
import {DataCities} from "../../pickerCity/types";

type MapLeafletProps = {
  selectedCities: DataCities[]
};

function MapLeaflet(props: MapLeafletProps) {
  const {
    selectedCities,
  } = props

  const [position, setPosition] = useState(null);

  const map = useMapEvent('click', () => {
    map.setView(position, map.getZoom())
  })

  useEffect(() => {
    const newCoords = selectedCities.map(item => {
      return [item.coordinate.latitude, item.coordinate.longitude]
    });

    const newCoordsNotEmpty = newCoords.length > 0 ? newCoords[0] : null;
    setPosition(newCoordsNotEmpty)


  }, [selectedCities]);


  return (
    <>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {/* {cities.map((city, idx) => (
        <Marker
          position={[city.lat, city.lng]}
          icon={markerIcon}
          key={idx}
        >
          <Popup>
            <b>
              {city.city}, {city.country}
            </b>
          </Popup>
        </Marker>
      ))}*/}
    </>
  )
}

export default MapLeaflet

