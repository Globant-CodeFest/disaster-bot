import geopandas as gpd
import json

gdf = gpd.read_file('data/comunas.geojson')

def _levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def get_location(location_string):
  distances = []
  for location in list(gdf['Comuna'].dropna().unique()):
    distance = _levenshtein_distance(location.lower(), location_string.lower())
    distances.append((location, distance, 'Comuna'))
  for location in list(gdf['Region'].dropna().unique()):
    distance = _levenshtein_distance(location.lower(), location_string.lower())
    distances.append((location, distance, 'Region'))
  for location in list(gdf['Provincia'].dropna().unique()):
    distance = _levenshtein_distance(location.lower(), location_string.lower())
    distances.append((location, distance, 'Provincia'))
  distances.sort(key=lambda x: x[1], reverse=False)
  return distances[0]

def get_geojson(location_string):
  selected_location = get_location(location_string)
  return gdf[gdf[selected_location[2]] == selected_location[0]]
