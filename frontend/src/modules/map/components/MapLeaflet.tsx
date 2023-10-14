import "leaflet/dist/leaflet.css";
import {Marker, Popup, TileLayer, useMapEvent} from "react-leaflet";
import {useEffect, useState} from "react";
import {DataCities, Gis} from "../../pickerCity/types";
import axios from "axios";
import L, {LatLngExpression} from "leaflet";

type MapLeafletProps = {
  selectedCities: DataCities[]
};

function MapLeaflet(props: MapLeafletProps) {
  const {
    selectedCities,
  } = props

  const redIcon = new L.Icon({
    iconUrl: '../../../../red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });

  const blueIcon = new L.Icon({
    iconUrl: '../../../../blue.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });

  const greenIcon = new L.Icon({
    iconUrl: '../../../../green.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });

  const [position, setPosition] = useState<LatLngExpression>();
  const [gis, setGis] = useState<Gis | null>(null);

  const map = useMapEvent('click', () => {
    map.setView(position as LatLngExpression, map.getZoom())
  })

  useEffect(() => {
    const newCoords = selectedCities.map(item => {
      return [item.coordinate.latitude, item.coordinate.longitude]
    });

    const newCoordsNotEmpty = newCoords.length > 0 ? newCoords[0] : null;
    setPosition(newCoordsNotEmpty as LatLngExpression)

  }, [selectedCities]);

  useEffect(() => {
    const fetch = async () => {
      if (selectedCities?.[0]?.id) {
        try {
          const response = await axios.get(`http://154.194.53.109:8000/api/v1/cities/${selectedCities?.[0]?.id}/gis`);
          setGis(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetch();
  }, [selectedCities]);

  const items = gis?.items


  console.log(items, 'gis22')

  return (
    <>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {items ? (
        items.map((city) => (
          city.object_type === 'positive' ? (
            <Marker
              key={`map-leaflet-${city.id}`}
              position={[city.coordinate.latitude, city.coordinate.longitude]}
              icon={greenIcon}
            >
              {city.object_type}
            </Marker>
          ) : (
            city.object_type === 'study' ? (
              <Marker
                key={`map-leaflet-${city.id}`}
                position={[city.coordinate.latitude, city.coordinate.longitude]}
                icon={blueIcon}
              >
                <Popup>
                  {city.object_type}
                </Popup>
              </Marker>
            ) : (
              <Marker
                key={`map-leaflet-${city.id}`}
                position={[city.coordinate.latitude, city.coordinate.longitude]}
                icon={redIcon}
              >
                <Popup>
                  {city.object_type}
                </Popup>
              </Marker>
            )
          )
        ))
      ) : null}
    </>
  )
}

export default MapLeaflet

