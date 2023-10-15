export type Data = {
  count: number,
  items: DataCities[]
}

export type Gis = {
  count: number,
  items: DataGis[]
}

export type Area = {
  "id": string,
  "name": string,
  "polygon_coordinates": Coords[],
  "by_type": {
    "negative": number,
    "positive": number,
    "study": number,
  },
  "by_object": {
    "park": number,
    "footway": number,
    "pitch": number,
    "sports_centre": number,
    "stadium": number,
    "track": number,
    "market": number,
    "greengrocer": number,
    "farm": number,
    "tobacco": number,
    "smoke_shop": number,
    "bar": number,
    "pub": number,
    "wine": number,
    "alcohol": number,
    "fast_food": number,
    "food_court": number,
    "university": number,
    "college": number,
    "school": number,
    "kindergarten": number,
    "language_school": number,
    "music_school": number,
  },
  "positivity_rate": number,
  "negative_points_overflow": number,
  "min_negative_point_distance": number,
}

export type Metrics = {
  "by_type": {
    "negative": number,
    "positive": number,
    "study": number
  },
  "by_object": {
    "park": number,
    "footway": number,
    "pitch": number,
    "sports_centre": number,
    "stadium": number,
    "track": number,
    "market": number,
    "greengrocer": number,
    "farm": number,
    "tobacco": number,
    "smoke_shop": number,
    "bar": number,
    "pub": number,
    "wine": number,
    "alcohol": number,
    "fast_food": number,
    "food_court": number,
    "university": number,
    "college": number,
    "school": number,
    "kindergarten": number,
    "language_school": number,
    "music_school": number
  },
  "positivity_metric": number,
  "avg_negatives_distance": number,
  "min_negative_point_distance": number
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
