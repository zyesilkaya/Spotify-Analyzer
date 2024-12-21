# main.py

import os
import pandas as pd
from data_processing import (
    load_streaming_history, preprocess_streaming_data,
    get_top_artists, get_monthly_trends, get_hourly_trends,
    calculate_most_played_per_month, calculate_top_played, load_your_library,
    get_top_saved_artists, get_genre_diversity, extract_superlisteners
)
from visualizations import (
    plot_top_artists, plot_monthly_trends, plot_hourly_trends,
    plot_top_10_tracks, plot_superlisteners, plot_artist_playtime_histograms,
    plot_top_saved_artists, plot_genre_diversity, plot_most_played_artist_per_month,
    plot_monthly_listening_time
)

import os
from data_processing import (
    extract_superlisteners, calculate_total_listening_time, 
    calculate_unique_artists, calculate_unique_tracks
)
from visualizations import (
    plot_superlisteners, plot_total_listening_time, 
    plot_unique_artists_and_tracks
)

# File path to Marquee.json
marquee_file_path = os.path.join('data', 'Marquee.json')  # Update as needed
streaming_files = [
    'StreamingHistory_music_0.json',
    'StreamingHistory_music_1.json',
    'StreamingHistory_music_2.json',
    'StreamingHistory_music_3.json',
    'StreamingHistory_music_4.json'
]
streaming_file_paths = [os.path.join('data', file) for file in streaming_files]

# Extract superlisteners data
superlisteners_counter = extract_superlisteners(marquee_file_path)

# Calculate total listening time, unique artists, and unique tracks
total_minutes = calculate_total_listening_time(streaming_file_paths)
unique_artists = calculate_unique_artists(streaming_file_paths)
unique_tracks = calculate_unique_tracks(streaming_file_paths)

# Load data
file_path = os.path.join('data', 'StreamingHistory_music_0.json')
streaming_data = load_streaming_history(file_path)

file_path = os.path.join('data', 'Marquee.json')  # Update as needed
superlisteners_counter = extract_superlisteners(file_path)

# Load YourLibrary.json data
library_path = os.path.join('data', 'YourLibrary.json')
library_data = load_your_library(library_path)

# Analyze and visualize saved artists and genre diversity
top_saved_artists = get_top_saved_artists(library_data)
plot_top_saved_artists(top_saved_artists)

genre_counts = get_genre_diversity(library_data)
if genre_counts:
    plot_genre_diversity(genre_counts)

file_list = [
    'StreamingHistory_music_0.json', 'StreamingHistory_music_1.json', 
    'StreamingHistory_music_2.json', 'StreamingHistory_music_3.json', 
    'StreamingHistory_music_4.json'
]
all_data = []
for file_name in file_list:
    with open(os.path.join('data', file_name), 'r') as file:
        all_data.extend(pd.read_json(file).to_dict(orient='records'))

most_played_stats = calculate_most_played_per_month(all_data)
most_played_artist_per_month = most_played_stats['most_played_artist_per_month']
total_playtime_minutes = most_played_stats['total_playtime_minutes']

# Visualize most played artist per month and total listening time
plot_most_played_artist_per_month(most_played_artist_per_month)
# plot_total_listening_time(total_playtime_minutes)

# Process data
streaming_data = preprocess_streaming_data(streaming_data)
top_artists = get_top_artists(streaming_data)
monthly_trends = get_monthly_trends(streaming_data, top_artists)
hourly_trends = get_hourly_trends(streaming_data)
most_played_per_month = calculate_most_played_per_month(streaming_data)
top_played = calculate_top_played(streaming_data)

plot_monthly_listening_time(all_data)

# Plot top 10 tracks
plot_top_10_tracks(all_data)

plot_top_artists(top_artists)
plot_hourly_trends(hourly_trends)
plot_superlisteners(superlisteners_counter)
plot_total_listening_time(total_minutes)
plot_unique_artists_and_tracks(unique_artists, unique_tracks)
