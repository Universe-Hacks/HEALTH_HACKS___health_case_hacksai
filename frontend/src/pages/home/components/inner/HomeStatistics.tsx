import {Card, Col, Layout, Statistic} from "antd";
import {ArrowDownOutlined, ArrowUpOutlined} from "@ant-design/icons";
import {DataCities, Metrics} from "../../../../modules/pickerCity/types";
import {useEffect, useState} from "react";
import axios from "axios";

type HomeStatisticsProps = {
  selectedCities: DataCities[]
};

function HomeStatistics(props: HomeStatisticsProps) {
  const {
    selectedCities,
  } = props

  const [metrics, setMetrics] = useState<Metrics | null>(null);

  const {Sider} = Layout;


  const siderStyle: React.CSSProperties = {
    lineHeight: '120px',
    color: '#fff',
    backgroundColor: '#eaeeef',
  };

  useEffect(() => {
    const fetch = async () => {
      if (selectedCities?.[0]?.id) {
        try {
          const response = await axios.get(`http://154.194.53.109:8000/api/v1/cities/${selectedCities?.[0]?.id}/metrics`);
          setMetrics(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetch();
  }, [selectedCities]);

  console.log(metrics, 'metr')

  return (
    metrics ? (
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
              title="Плотность позитивных объектов"
              value={metrics?.by_type.positive}
              precision={2}
              valueStyle={metrics?.by_type?.positive >= 1.5 ? {color: '#3f8600'} : {color: '#cf1322'}}
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
    ) : null)
}

export default HomeStatistics
