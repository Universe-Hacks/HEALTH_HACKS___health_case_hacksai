import type {DescriptionsProps} from 'antd';
import {Button, Descriptions, Layout} from 'antd';
import CityPicker from "../../../modules/pickerCity/components/CityPicker";
import {useEffect, useState} from "react";
import {Area, Data, DataCities} from "../../../modules/pickerCity/types";
import axios from 'axios';
import HomeStatistics from "./inner/HomeStatistics";
import {MapContainer} from "react-leaflet";
import MapLeaflet from "../../../modules/map/components/MapLeaflet";
import AreaPicker from "../../../modules/pickerCity/components/AreaPicker";

const {Header, Footer} = Layout;

function Home() {
  const headerStyle: React.CSSProperties = {
    textAlign: 'left',
    display: 'flex',
    alignItems: 'center',
    color: '#fff',
    height: '100px',
    paddingInline: 50,
    lineHeight: '64px',
    backgroundColor: '#eaeeef',
  };


  const footerStyle: React.CSSProperties = {
    textAlign: 'center',
    color: '#fff',
    backgroundColor: '#eee',
  };

  const itemsDescriptions: DescriptionsProps['items'] = [
    {
      key: '1',
      label: 'XXXXXX',
      children: 'Понизьте количество негативных объектов',
    },
    {
      key: '2',
      label: 'XXXXXX',
      children: 'Повысьте количество положительных объектов',
    },
    {
      key: '3',
      label: 'XXXXXX',
      children: 'Понизьте количество негативных объектов',
    },
    {
      key: '4',
      label: 'XXXXXX',
      children: 'Повысьте количество положительных объектов',
    },
    {
      key: '5',
      label: 'XXXXXX',
      children: 'Понизьте количество негативных объектов',
    },
  ];

  const [cities, setCities] = useState<Data | null>(null);
  const [selectedCities, setSelectedCities] = useState<DataCities[] | null>([]);
  const [selectedArea, setSelectedArea] = useState<Area[] | null>([]);
  const [areas, setAreas] = useState<Area[] | null>(null);

  const items = cities?.items


  console.log(selectedArea, 'selectedArea')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://154.194.53.109:8000/api/v1/cities');
        setCities(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  console.log(areas, 'areas')

  const {Content} = Layout;

  const contentStyle: React.CSSProperties = {
    textAlign: 'center',
    display: 'flex',
    paddingInline: 50,
    color: '#fff',
    width: '550px',
    backgroundColor: '#eaeeef',
  };

  return (
    <Layout>
      <Header style={headerStyle}>
        {
          items ? (
            <CityPicker
              items={items}
              setSelectedCities={setSelectedCities}
              setSelectedArea={setSelectedArea}
            />
          ) : null
        }
        {selectedCities ? (
          <AreaPicker
            areas={areas}
            setAreas={setAreas}
            selectedCities={selectedCities}
            selectedArea={selectedArea}
            setSelectedArea={setSelectedArea}
            setSelectedCities={setSelectedCities}
          />
        ) : null}
        <Button
          style={{
            backgroundColor: '#48773C',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            height: '48px',
            marginLeft: '40px',
            textDecoration: 'none',
            borderRadius: '6px'
          }}
          href="/comparisonCity"
        >
          Сравнение городов
        </Button>
        <Button
          style={{
            backgroundColor: '#48773C',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            height: '48px',
            marginLeft: '40px',
            textDecoration: 'none',
            borderRadius: '6px'
          }}
          href="/comparisonArea"
        >
          Сравнение районов
        </Button>
      </Header>
      {selectedCities ? (
        <>
          <Layout hasSider>
            <Content style={contentStyle}>
              {selectedCities || selectedArea ? (
                <MapContainer center={[56.839104, 60.60825]} zoom={12}>
                  <MapLeaflet
                    selectedCities={selectedCities}
                    selectedArea={selectedArea as Area[]}
                  />
                </MapContainer>
              ) : null}
            </Content>
            <HomeStatistics
              selectedCities={selectedCities}
              selectedArea={selectedArea as Area[]}
            />
          </Layout>
        </>
      ) : null}
      <Footer style={footerStyle}>
        <Descriptions style={{fontSize: '20px'}} title="Рекомендации" items={itemsDescriptions}/>
      </Footer>
    </Layout>
  )
}

export default Home
