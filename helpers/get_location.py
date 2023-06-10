import pandas as pd

df = pd.read_csv('data/1900_2021_DISASTERS.xlsx - emdat data.csv')

df_chile = df[df['Country'] == 'Chile']

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
  for location in list(df_chile['Location'].dropna().unique()):
    distance = _levenshtein_distance(location.lower(), location_string.lower())
    distances.append((location, distance))
  distances.sort(key=lambda x: x[1], reverse=False)
  return distances[0][0]

