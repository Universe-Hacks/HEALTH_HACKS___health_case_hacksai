import "leaflet/dist/leaflet.css";
import {Marker, Polygon, TileLayer, useMapEvent} from "react-leaflet";
import {useEffect, useState} from "react";
import {Area, DataCities, Gis} from "../../pickerCity/types";
import axios from "axios";
import L, {LatLngExpression} from "leaflet";

type MapLeafletProps = {
  selectedCities: DataCities[]

  selectedArea: Area[]
};

function MapLeaflet(props: MapLeafletProps) {
  const {
    selectedCities,
    selectedArea,
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
  const [positionArea, setPositionArea] = useState<LatLngExpression>();
  const [gis, setGis] = useState<Gis | null>(null);
  const [, setAreaGis] = useState<Gis | null>(null);

  const items = gis?.items

  const map = useMapEvent('click', () => {
    map.setView(position as LatLngExpression, map.getZoom())
  })

  const mapArea = useMapEvent('click', () => {
    mapArea.setView(positionArea as LatLngExpression, mapArea.getZoom())
  })

  const polygon = selectedArea.map(item => {
    return item.polygon_coordinates
  })

  const polyg = polygon[0]?.map(item => [item.latitude, item.longitude]);

  useEffect(() => {
    const newCoords = selectedCities.map(item => {
      return [item.coordinate.latitude, item.coordinate.longitude]
    });

    const newCoordsNotEmpty = newCoords.length > 0 ? newCoords[0] : null;
    setPosition(newCoordsNotEmpty as LatLngExpression)
  }, [selectedCities]);

  useEffect(() => {
    const newCoords = selectedArea.map(item => {
      return [item.polygon_coordinates[0].latitude, item.polygon_coordinates[0].longitude]
    });

    const newCoordsNotEmpty = newCoords.length > 0 ? newCoords[0] : null;
    setPositionArea(newCoordsNotEmpty as LatLngExpression)
  }, [selectedArea]);


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

  useEffect(() => {
    const fetch = async () => {
      if (selectedArea?.[0]?.id) {
        try {
          const response = await axios.get(`http://154.194.53.109:8000/api/v1/cities/${selectedCities?.[0]?.id}/${selectedArea?.[0]?.id}/gis`);
          setAreaGis(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetch();
  }, [selectedArea]);

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
            </Marker>
          ) : (
            city.object_type === 'study' ? (
              <Marker
                key={`map-leaflet-${city.id}`}
                position={[city.coordinate.latitude, city.coordinate.longitude]}
                icon={blueIcon}
              >
              </Marker>
            ) : (
              <Marker
                key={`map-leaflet-${city.id}`}
                position={[city.coordinate.latitude, city.coordinate.longitude]}
                icon={redIcon}
              >
              </Marker>
            )
          )
        ))
      ) : null}

      {polygon.length > 0 ? (
        <Polygon positions={polyg as LatLngExpression[]} color="blue"/>
      ) : null}
    </>
  )
}

export default MapLeaflet

