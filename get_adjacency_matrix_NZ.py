import pandas as pd
from math import radians, cos, sin, asin, sqrt

# Set Earth's radius.
radius = 6371

# Parse the fixed width texts into structured numerical data.
ColSpecs = [(0, 2), (11, 20), (21, 30)]

# (Optional) To save time, load only small part of the datas that possibly contains "NZ".
RowSpecs = [(40000, 60000)]

stations = pd.read_fwf("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt", colspecs=ColSpecs, rowspecs=RowSpecs, header=None)

# Select the stations in NZ.
stations_NZ = stations.loc[stations[0] == "NZ"]

# Delete the first column.
del stations_NZ[0]

# Compute the geographical distances using the Haversine formula (unit: kilometer).
def get_distance(long_a, lat_a, long_b, lat_b):

  # Transform to radians.
  long_a, lat_a, long_b, lat_b = map(radians, [long_a, lat_a, long_b, lat_b])

  distance = 2 * radius * asin(sqrt(sin((lat_b - lat_a) / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin((long_b - long_a) / 2) ** 2))
  return abs(round(distance, 2))

# Get the adjacency matrix.

# Create an empty matrix.
matrix_dim = list(range(len(stations_NZ.index)))
adjacency_matrix = pd.DataFrame(index=matrix_dim, columns=matrix_dim)
print("The number of rows is " + str(len(stations_NZ.index)) + ".")

# Fill the matrix.
for i in matrix_dim:
    adjacency_matrix.iat[i, i] = 0
    for j in range(i + 1, matrix_dim[-1] + 1):
        distance = get_distance(stations_NZ.iat[i, 1], stations_NZ.iat[i, 0], stations_NZ.iat[j, 1], stations_NZ.iat[j, 0])
        adjacency_matrix.iat[i, j] = distance
        adjacency_matrix.iat[j, i] = distance
    print("Add the %sth row." % i)

print("--------------------")
print("The adjacency matrix:")
print(adjacency_matrix)
print("--------------------")
print("Save the adjacency matrix into a CSV file.")
adjacency_matrix.to_csv("/home/dning/GHCN/GHCN_adjacency_matrix_NZ.csv", index=False, header=False)