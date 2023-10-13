import {Select} from 'antd';

function CityPicker() {

  const onChange = (value: string) => {
    console.log(`selected ${value}`);
  };

  const onSearch = (value: string) => {
    console.log('search:', value);
  };

  const filterOption = (input: string, option?: { label: string; value: string }) =>
    (option?.label ?? '').toLowerCase().includes(input.toLowerCase());

  const data = [
    {
      value: 'Екатеринбург',
      label: 'Екатеринбург',
    },
    {
      value: 'Тула',
      label: 'Тула',
    },
    {
      value: 'Тамбов',
      label: 'Тамбов',
    },
  ]

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
