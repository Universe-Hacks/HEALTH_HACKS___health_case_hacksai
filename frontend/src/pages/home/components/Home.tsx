import Map from '../../../modules/map/components/Map'
import CityPicker from "../../../modules/pickerCity/components/CityPicker";
import type {DescriptionsProps} from 'antd';
import {Button, Card, Col, Descriptions, Statistic} from "antd";
import {ArrowDownOutlined, ArrowUpOutlined} from '@ant-design/icons';

function Home() {

  const items: DescriptionsProps['items'] = [
    {
      key: '1',
      label: 'XXXXXX',
      children: 'Zhou Maomao',
    },
    {
      key: '2',
      label: 'XXXXXX',
      children: '1810000000',
    },
    {
      key: '3',
      label: 'XXXXXX',
      children: 'Hangzhou, Zhejiang',
    },
    {
      key: '4',
      label: 'XXXXXX',
      children: 'empty',
    },
    {
      key: '5',
      label: 'XXXXXX',
      children: 'No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China',
    },
  ];

  return (
    <div className="home__wrapper">
      <div className="home__city-picker">
        <CityPicker/>
        <div className="home__city-add">
          <Button type="primary" href="/about">Добавить в сравнение</Button>
        </div>
      </div>
      <div className="home__city-map">
        <Map/>
        <div className="home__city-statistics">
          <Col>
            <Col span={12} style={{marginBottom: '40px'}}>
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
            <Col span={12} style={{marginBottom: '40px'}}>
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
            <Col span={12}>
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
          </Col>
        </div>
      </div>
      <div className="home__city-descr">
        <Descriptions title="Рекомендации" items={items}/>
      </div>
    </div>
  )
}

export default Home
