# spotify-network

This was created for Dr. Matta's CS490 Social and Biological Networks class.

It is a program for generating a network off of your Spotify extended listening history where a node is a song and an edge exists if two songs were listened to each other consecutively. The main portion of the code exists in the "spotify_network" folder.

This repository also contains scripts in the "scripts" folder for scraping large amounts of data for different songs off of the Spotify API. The scraping is rate limited and the purpose of it is so that you can pull down Spotify song data in batches and save it so you don't need to constantly hit the API.

## Instructions on Running

### Setup
```bash
pip install -r requirements.txt
```

Add a folder to this repository titled "MyData" that contains all of your endsong_*.json files.

### Running
```bash
python spotify_network/network.py
```
Generates a .gexf and .gml file containing your graph data
