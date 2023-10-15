import {Area, DataCities} from "../../../../modules/pickerCity/types";
import {useEffect, useState} from "react";
import axios from "axios";

type FootetWrapperProps = {
  selectedCities: DataCities[]

  selectedArea: Area[]
};

function FooterWrapper(props: FootetWrapperProps) {

  const {
    selectedCities,
    selectedArea,
  } = props

  const [recs, setRecs] = useState<Record<string, string>[]>();

  useEffect(() => {
    const fetchData = async () => {
      if (selectedCities?.[0]?.id) {
        try {
          const response = await axios.get(`http://154.194.53.109:8000/api/v1/cities/${selectedCities?.[0]?.id}/recs`);
          setRecs(response.data);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    };

    fetchData();
  }, [selectedCities]);

  return (
    <div>
      <div className="footer-wrapper">Рекомендации</div>
      {recs ? (
        recs?.map((item: Record<string, string>) => (
            <div key={item.key} className="footer-descr">
              <div>{item.key}: {item.value}</div>
            </div>
          )
        )
      ) : <span className="footer-text">Выберите город, чтобы получить рекомендации</span>}

      {selectedArea ? (
        selectedArea?.[0]?.recs?.map((item: Record<string, string>) => (
            <div key={item.key} className="footer-descr">
              <div>{item.key}: {item.value}</div>
            </div>
          )
        )
      ) : <span className="footer-text">Выберите район, чтобы получить рекомендации</span>}
    </div>
  );
}

export default FooterWrapper
