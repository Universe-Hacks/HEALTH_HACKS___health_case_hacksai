import type {DescriptionsProps} from 'antd';
import {Button, Descriptions, Layout} from 'antd';
import CityPicker from "../../../modules/pickerCity/components/CityPicker";
import {useEffect, useState} from "react";
import {Data, DataCities} from "../../../modules/pickerCity/types";
import axios from 'axios';
import HomeStatistics from "./inner/HomeStatistics";
import {MapContainer} from "react-leaflet";
import MapLeaflet from "../../../modules/map/components/MapLeaflet";

const {Header, Footer} = Layout;

function Home() {
  const headerStyle: React.CSSProperties = {
    textAlign: 'left',
    display: 'flex',
    alignItems: 'center',
    color: '#fff',
    height: 100,
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

  const items = cities?.items

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

  const {Content} = Layout;

  const contentStyle: React.CSSProperties = {
    textAlign: 'center',
    display: 'flex',
    alignItems: 'center',
    lineHeight: '120px',
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
            />
          ) : null
        }
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
              {selectedCities ? (
                <MapContainer center={[56.839104, 60.60825]} zoom={10}>
                  <MapLeaflet selectedCities={selectedCities}/>
                </MapContainer>
              ) : null}
            </Content>
            <HomeStatistics selectedCities={selectedCities}/>
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
