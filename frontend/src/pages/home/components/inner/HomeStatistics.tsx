import {Card, Col, Layout, Statistic} from "antd";
import {ArrowDownOutlined, ArrowUpOutlined} from "@ant-design/icons";
import {Area, DataCities, Metrics} from "../../../../modules/pickerCity/types";
import {useEffect, useState} from "react";
import axios from "axios";

type HomeStatisticsProps = {
  selectedCities: DataCities[]

  selectedArea: Area[],
};

function HomeStatistics(props: HomeStatisticsProps) {
  const {
    selectedCities,
    selectedArea,
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

  console.log(selectedArea, 'reametr')

  return (
    metrics ? (
      <Sider style={siderStyle}>
        {selectedArea?.[0]?.positivity_rate ? (
          <>
            <Col span={35} style={{marginBottom: '40px'}}>
              <Card bordered={true}>
                <Statistic
                  title="Отношение позитивных точек к негативным"
                  value={selectedArea?.[0]?.positivity_rate}
                  precision={2}
                  valueStyle={selectedArea?.[0]?.positivity_rate >= 1.5 ? {color: '#3f8600'} : {color: '#cf1322'}}
                  prefix={selectedArea?.[0]?.positivity_rate >= 1.5 ? <ArrowUpOutlined/> : <ArrowDownOutlined/>}
                  suffix={<>точек/км<sup>2</sup></>}
                />
              </Card>
            </Col>
            <Col span={35} style={{marginBottom: '40px'}}>
              <Card bordered={true}>
                <Statistic
                  title="Число негативных точек удаленных менее 100м от учебных учреждений"
                  value={selectedArea?.[0]?.negative_points_overflow}
                  precision={0}
                  valueStyle={selectedArea?.[0]?.negative_points_overflow >= 1 ? {color: '#3f8600'} : {color: '#cf1322'}}
                  prefix={selectedArea?.[0]?.negative_points_overflow >= 1 ? <ArrowUpOutlined/> : <ArrowDownOutlined/>}
                  suffix="точек"
                />
              </Card>
            </Col>
          </>
        ) : null}

        <Col span={35} style={{marginBottom: '40px'}}>
          <Card bordered={true}>
            <Statistic
              title="Плотность позитивных объектов"
              value={metrics?.by_type.positive}
              precision={2}
              valueStyle={metrics?.by_type?.positive >= 1.5 ? {color: '#3f8600'} : {color: '#cf1322'}}
              prefix={metrics?.by_type?.positive >= 1.5 ? <ArrowUpOutlined/> : <ArrowDownOutlined/>}
              suffix={<>точек/км<sup>2</sup></>}
            />
          </Card>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Card bordered={true}>
            <Statistic
              title="Плотность негативных объектов"
              value={metrics?.by_type?.negative}
              precision={2}
              valueStyle={{color: '#cf1322'}}
              prefix={<ArrowDownOutlined/>}
              suffix={<>точек/км<sup>2</sup></>}
            />
          </Card>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Card bordered={true}>
            <Statistic
              title="Тенденция районов"
              value={metrics?.positivity_metric >= 1 ? 'Положительная' : metrics?.positivity_metric >= 0 && metrics?.positivity_metric < 1 ? 'Нейтральная' : 'Отрицательная'}
              precision={0}
              valueStyle={metrics?.positivity_metric >= 1 ? {color: '#3f8600'} : metrics?.positivity_metric >= 0 && metrics?.positivity_metric < 1 ? {color: '#80A6FF'} : {color: '#cf1322'}}
              prefix={metrics?.positivity_metric >= 1 ?
                <ArrowUpOutlined/> : metrics?.positivity_metric >= 0 && metrics?.positivity_metric < 1 ?
                  <ArrowUpOutlined/> : <ArrowDownOutlined/>}
              suffix=""
            />
          </Card>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Card bordered={true}>
            <Statistic
              title="Средняя удаленность отрицательных точек от позитивных"
              value={metrics?.avg_negatives_distance}
              precision={0}
              valueStyle={metrics?.avg_negatives_distance > 200 ? {color: '#3f8600'} : {color: '#cf1322'}}
              prefix={metrics?.avg_negatives_distance > 200 ? <ArrowUpOutlined/> : <ArrowDownOutlined/>}
              suffix="м"
            />
          </Card>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Card bordered={true}>
            <Statistic
              title="Минимальное расстояние от негативной точки до учебного учреждения"
              value={metrics?.min_negative_point_distance}
              precision={2}
              valueStyle={metrics?.min_negative_point_distance > 100 ? {color: '#3f8600'} : {color: '#cf1322'}}
              prefix={metrics?.min_negative_point_distance > 100 ? <ArrowUpOutlined/> : <ArrowDownOutlined/>}
              suffix="м"
            />
          </Card>
        </Col>
      </Sider>
    ) : null)
}

export default HomeStatistics
