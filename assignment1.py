# Import necessary libraries
import pandas as pd
from geopy.distance import geodesic
import folium
import branca

# Load the shark sightings data
df_sharks = pd.read_csv('sharks.csv')

# Function to calculate the total distance traveled by a shark
def calculate_distance(df):
    total_distance = 0
    for i in range(1, len(df)):
        current_coords = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])
        previous_coords = (df.iloc[i-1]['latitude'], df.iloc[i-1]['longitude'])
        total_distance += geodesic(previous_coords, current_coords).kilometers
    return total_distance

# Get the unique shark IDs
shark_ids = df_sharks['id'].unique()

# Create a color dictionary for each shark
colors = ['blue', 'green', 'red', 'purple', 'orange']
color_dict = {shark_id: color for shark_id, color in zip(shark_ids[:5], colors)}

# Create a folium Map object
m = folium.Map(location=[0, 0], zoom_start=2)

# Create a legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 100px; height: 90px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            ">&nbsp; <b>Shark ID</b> <br>
              &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i> &nbsp; {} <br>
              &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i> &nbsp; {} <br>
              &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i> &nbsp; {} <br>
              &nbsp; <i class="fa fa-map-marker fa-2x" style="color:purple"></i> &nbsp; {} <br>
              &nbsp; <i class="fa fa-map-marker fa-2x" style="color:orange"></i> &nbsp; {}
</div>
'''.format(*shark_ids[:5])

m.get_root().html.add_child(folium.Element(legend_html))

# Calculate the total distance traveled by the first 5 sharks and plot their paths
for i, shark_id in enumerate(shark_ids[:5]):
    df_shark = df_sharks[df_sharks['id'] == shark_id].sort_values('datetime')
    total_distance = calculate_distance(df_shark)

    # Create a folium PolyLine object for the shark's path
    path = folium.PolyLine(locations=df_shark[['latitude', 'longitude']].values,
                           color=color_dict[shark_id], weight=5)

    # Add a tooltip to the path
    path.add_child(folium.Tooltip(f'Shark ID: {shark_id}\nSpecies: {df_shark["species"].iloc[0]}'))

    # Add the path to the map
    m.add_child(path)

# Display the map
m.save('shark_paths.html')

import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Load the shark sightings data
df_sharks = pd.read_csv('sharks.csv')

# Function to calculate the total distance traveled by a shark
def calculate_distance(df):
    total_distance = 0
    for i in range(1, len(df)):
        current_coords = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])
        previous_coords = (df.iloc[i-1]['latitude'], df.iloc[i-1]['longitude'])
        total_distance += geodesic(previous_coords, current_coords).kilometers
    return total_distance

# Create a new dataframe to store the total distance traveled by each shark
df_distances = pd.DataFrame(columns=['id', 'species', 'distance'])

# Calculate the total distance traveled by each shark and add it to the dataframe
for shark_id in df_sharks['id'].unique():
    df_shark = df_sharks[df_sharks['id'] == shark_id].sort_values('datetime')
    total_distance = calculate_distance(df_shark)
    df_distances.loc[len(df_distances)] = [shark_id, df_shark['species'].iloc[0], total_distance]

# Calculate the average distance traveled by each species
df_average_distances = df_distances.groupby('species')['distance'].mean().reset_index()

# Plot the average distances
plt.bar(df_average_distances['species'], df_average_distances['distance'], color='blue')
plt.title('Average Distance Traveled by Each Species')
plt.xlabel('Species')
plt.ylabel('Average Distance (km)')
plt.show()

# Find the shark that covered the most distance for each species
df_max_distance = df_distances.groupby('species')['distance'].idxmax()
df_sharks_max_distance = df_distances.loc[df_max_distance]

# Print the shark that covered the most distance for each species
print(df_sharks_max_distance)
