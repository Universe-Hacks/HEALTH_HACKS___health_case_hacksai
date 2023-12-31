import {Select} from 'antd';
import {Area, DataCities} from "../types";
import {Dispatch, SetStateAction} from "react";

type CityPickerProps = {
  items: DataCities[],

  setSelectedArea: Dispatch<SetStateAction<Area[] | null>>,

  setSelectedCities: Dispatch<SetStateAction<DataCities[] | null>>,
};

function CityPicker(props: CityPickerProps) {

  const {
    setSelectedArea,
    items,
    setSelectedCities,
  } = props

  const data = items.map((city) => ({
    value: city.id,
    label: city.name
  }))

  const onChange = (value: string) => {
    const selectedCity = items.filter(item => {
      return item.id === value
    })

    setSelectedCities(selectedCity)
    setSelectedArea([])
    alert('Кликни на карту для навигации к выбранному городу')
  };

  const onSearch = (value: string) => {
    console.log('search:', value);
  };

  const filterOption = (input: string, option?: { label: string; value: string }) =>
    (option?.label ?? '').toLowerCase().includes(input.toLowerCase());

  return (
    <Select
      className="custom-select"
      showSearch
      placeholder="Выберите город"
      optionFilterProp="children"
      onChange={onChange}
      onSearch={onSearch}
      filterOption={filterOption}
      options={data}
    />
  );
}

export default CityPicker
