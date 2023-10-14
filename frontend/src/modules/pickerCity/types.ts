export type Data = {
  count: number,
  items: DataCities[]
}

export type DataCities = {
  "id": string,
  "name": string,
  "coordinate": Coords
}

export type Coords = {
  "latitude": number,
  "longitude": number
}
