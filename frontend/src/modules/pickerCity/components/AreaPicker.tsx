import {Select} from 'antd';
import {Area, DataCities} from "../types";
import {Dispatch, SetStateAction, useEffect} from "react";
import axios from "axios";

type AreaPickerProps = {
  selectedArea: Area[] | null,

  areas: Area[] | null,

  setAreas: Dispatch<SetStateAction<Area[] | null>>,

  selectedCities: DataCities[],

  setSelectedArea: Dispatch<SetStateAction<Area[] | null>>,

  setSelectedCities: Dispatch<SetStateAction<DataCities[] | null>>,
}

function AreaPicker(props: AreaPickerProps) {

  const {
    selectedCities,
    setSelectedArea,
    setAreas,
    areas,
  } = props


  useEffect(() => {
    const fetch = async () => {
      if (selectedCities?.[0]?.id) {
        try {
          const response = await axios.get(`http://154.194.53.109:8000/api/v1/districts/${selectedCities?.[0]?.id}`);
          setAreas(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetch();
  }, [selectedCities]);

  const data = areas ? areas.map((area) => ({
    value: area.id,
    label: area.name
  })) : []

  const onChange = (value: string) => {
    const selectedAreas = areas?.filter(item => {
      return item.id === value
    })

    setSelectedArea(selectedAreas as Area[])
    alert('Кликни на карту для навигации к выбранному району')
  };

  const onSearch = (value: string) => {
    console.log('search:', value);
  };

  const filterOption = (input: string, option?: { label: string; value: string }) =>
    (option?.label ?? '').toLowerCase().includes(input.toLowerCase());

  return (
    <Select
      className="custom-select-area"
      showSearch
      disabled={selectedCities.length > 0 || (areas && areas.length > 0) ? false : true}
      placeholder="Выберите район"
      optionFilterProp="children"
      onChange={onChange}
      onSearch={onSearch}
      filterOption={filterOption}
      options={data}
    />
  );
}

export default AreaPicker
