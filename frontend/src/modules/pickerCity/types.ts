export type Data = {
  count: number,
  items: DataCities[]
}

export type Gis = {
  count: number,
  items: DataGis[]
}

export type DataGis = {
  "id": string,
  "object_type": string,
  "coordinate": Coords,
  "tags": Tags[],
}

export type Tags = {
  "name": string,
  "value": string
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
