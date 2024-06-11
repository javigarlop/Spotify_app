## Documentation for the Music Data Analysis Script

This script is designed to automate the process of retrieving, processing, and visualizing music data from the Spotify API. It is particularly useful for music analysts, data scientists, and enthusiasts who want to explore and visualize various musical attributes of an artist's work.

### Purpose

The primary purpose of this script is to:
1. **Authenticate** with the Spotify API using provided credentials.
2. **Search** for a specific artist on Spotify.
3. **Retrieve** detailed information about the artist's albums and tracks.
4. **Fetch** audio features for each track, such as valence (happiness) and energy levels.
5. **Visualize** the data using a scatter plot to show the relationship between valence and energy across different tracks and albums.

### Key Features

1. **Logging**: The script logs its progress and any issues encountered, providing helpful messages to track the process.
2. **Data Saving**: Retrieved data is saved as JSON files for later use or analysis.
3. **Visualization**: The script generates a scatter plot to visualize the valence and energy of tracks, offering insights into the emotional and energetic properties of the music.

### Step-by-Step Breakdown

#### 1. **Authentication**
- The script starts by loading Spotify API credentials (client ID and client secret) from a `secrets.json` file.
- It then requests a bearer token from the Spotify API, which is required for subsequent API calls.

#### 2. **Artist Search**
- The script searches for the specified artist on Spotify.
- It retrieves basic information about up to 10 matching artists, including their IDs and names.
- The results are saved as a JSON file and converted into a Pandas DataFrame for further processing.

#### 3. **Album Data Retrieval**
- Using the artist's ID, the script fetches information about their albums.
- It collects up to 35 albums, saving details like album names and IDs.
- This data is saved as a JSON file and also converted into a DataFrame.

#### 4. **Track Data Retrieval**
- For each album, the script retrieves information about all tracks.
- It compiles data including track names and IDs, along with the corresponding album information.
- This data is saved as a JSON file and converted into a DataFrame.

#### 5. **Audio Features Fetching**
- The script fetches audio features (valence and energy) for each track.
- These features are added to the DataFrame for tracks.

#### 6. **Data Visualization**
- The script generates a scatter plot with valence on the x-axis and energy on the y-axis.
- Different albums are represented by different colors.
- The plot helps visualize the emotional and energetic landscape of the artist's music.
- The plot is saved as a PNG file.

### Usage

To run the script, execute it with the desired artist's name and specify a directory to save the results. For example:

```bash
python script_name.py
```

Ensure that the secrets.json file is in the same directory as the script and contains your Spotify API credentials.

### Example Output

The script produces several JSON files containing the retrieved data and a PNG file of the scatter plot, all saved in the specified results directory.
