import {Card, Col, Layout, Statistic, Tooltip} from "antd";
import {ArrowDownOutlined, ArrowUpOutlined} from "@ant-design/icons";
import {Area, DataCities, Metrics} from "../../../../modules/pickerCity/types";
import {useEffect, useMemo, useState} from "react";
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
    width: "1550px",
    display: 'inline-flex',
    maxWidth: "1550px",
    minWidth: "1550px",
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

  const [arrow,] = useState('Show');

  const mergedArrow = useMemo(() => {
    if (arrow === 'Hide') {
      return false;
    }

    if (arrow === 'Show') {
      return true;
    }

    return {
      pointAtCenter: true,
    };
  }, [arrow]);

  console.log(selectedArea, 'reametr')

  return (
    metrics ? (
      <Sider style={siderStyle}>
        {selectedArea?.[0]?.positivity_rate ? (
          <>
            <Col span={35} style={{marginBottom: '40px'}}>
              <Tooltip placement="top"
                       title='Сумма положительных точек в районе города превышает отрицательные на 50%. Если значение больше 1.5, то отображается зеленым, и значит сумма положительных точек превышает отрицательные. (метрика для районов)'
                       arrow={mergedArrow}>
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
              </Tooltip>
            </Col>
            <Col span={35} style={{marginBottom: '40px'}}>
              <Tooltip placement="top"
                       title='Число точек продажи алкоголя или табака или фастфуда удаленных от образовательных учреждений менее чем на 100м. Значение указывается красным, если количество точек больше или равно 1. (метрика для районов)'
                       arrow={mergedArrow}>
                <Card bordered={true}>
                  <Statistic
                    title="Число негативных точек удаленных менее 100м от учебных учреждений"
                    value={selectedArea?.[0]?.negative_points_overflow}
                    precision={0}
                    valueStyle={selectedArea?.[0]?.negative_points_overflow >= 1 ? {color: '#cf1322'} : {color: '#3f8600'}}
                    prefix={selectedArea?.[0]?.negative_points_overflow >= 1 ? <ArrowDownOutlined/> :
                      <ArrowUpOutlined/>}
                    suffix="точек"
                  />
                </Card>
              </Tooltip>
            </Col>
          </>
        ) : null}

        <Col span={35} style={{marginBottom: '40px'}}>
          <Tooltip placement="top"
                   title='Разница числа районов, в которых сумма положительных точек превышает отрицательные на 50% от числа районов, в которых сумма положительных точек не превышает отрицательные на 50%. Если значение больше или равно 1 (Положительная), от 0 до 1 (Нейтральная), меньше 0 (Отрицательная). (метрика для города)'
                   arrow={mergedArrow}>
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
          </Tooltip>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Tooltip placement="top"
                   title='Средняя удаленность отрицательных точек в городе от положительных точек менее 200 метров. Если значение зеленое значит отрицательная точка расположена более чем на 200м от положительной (метрика для города)'
                   arrow={mergedArrow}>
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
          </Tooltip>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Tooltip placement="top"
                   title='Плотность позитивных точек. Если значение больше 1.5 (зеленое).'
                   arrow={mergedArrow}>
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
          </Tooltip>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Tooltip placement="top"
                   title='Плотность негативных точек.'
                   arrow={mergedArrow}>
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
          </Tooltip>
        </Col>
        <Col span={35} style={{marginBottom: '40px'}}>
          <Tooltip placement="top"
                   title='Минимальное расстояние от негативной точки до учебного учреждения. Если значение больше 100м, значение (зеленое).'
                   arrow={mergedArrow}>
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
          </Tooltip>
        </Col>
      </Sider>
    ) : null)
}

export default HomeStatistics
