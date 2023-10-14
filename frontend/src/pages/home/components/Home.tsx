import type {DescriptionsProps} from 'antd';
import {Button, Card, Col, Descriptions, Layout, Statistic} from 'antd';
import {ArrowDownOutlined, ArrowUpOutlined} from '@ant-design/icons';
import CityPicker from "../../../modules/pickerCity/components/CityPicker";
import {useEffect, useState} from "react";
import {Data, DataCities} from "../../../modules/pickerCity/types";
import axios from 'axios';
import {MapContainer} from "react-leaflet";
import MapLeaflet from "../../../modules/map/components/MapLeaflet";

function Home() {

  const {Header, Footer, Sider, Content} = Layout;

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

  const siderStyle: React.CSSProperties = {
    lineHeight: '120px',
    color: '#fff',
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
      <Layout hasSider>
        <Content style={contentStyle}>
          {selectedCities ? (
            <MapContainer center={[56.839104, 60.60825]} zoom={10}>
              <MapLeaflet selectedCities={selectedCities}/>
            </MapContainer>
          ) : null}
        </Content>
        <Sider style={siderStyle}>
          <Col span={35} style={{marginBottom: '40px'}}>
            <Card bordered={true}>
              <Statistic
                title="Равномерность распределения"
                value={11.28}
                precision={2}
                valueStyle={{color: '#3f8600'}}
                prefix={<ArrowUpOutlined/>}
                suffix="%"
              />
            </Card>
          </Col>
          <Col span={35} style={{marginBottom: '40px'}}>
            <Card bordered={true}>
              <Statistic
                title="Плотность объектов"
                value={9.3}
                precision={2}
                valueStyle={{color: '#cf1322'}}
                prefix={<ArrowDownOutlined/>}
                suffix="%"
              />
            </Card>
          </Col>
          <Col span={35}>
            <Card bordered={true}>
              <Statistic
                title="Минимальное расстояние"
                value={11.28}
                precision={2}
                valueStyle={{color: '#3f8600'}}
                prefix={<ArrowUpOutlined/>}
                suffix="%"
              />
            </Card>
          </Col>
        </Sider>
      </Layout>
      <Footer style={footerStyle}>
        <Descriptions style={{fontSize: '20px'}} title="Рекомендации" items={itemsDescriptions}/>
      </Footer>
    </Layout>
  )
}

export default Home
