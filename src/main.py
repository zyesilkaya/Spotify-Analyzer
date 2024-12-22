# main.py

import os
import pandas as pd

# Import data processing functions
from data_processing import (
    load_streaming_history, preprocess_streaming_data, get_top_artists,
    get_monthly_trends, get_hourly_trends, calculate_most_played_per_month,
    calculate_top_played, load_your_library, get_top_saved_artists,
    extract_superlisteners, calculate_total_listening_time,
    calculate_unique_artists, calculate_unique_tracks
)

# Import visualization functions
from visualizations import (
    plot_top_artists, plot_monthly_trends, plot_hourly_trends,
    plot_top_10_tracks, plot_superlisteners, plot_artist_playtime_histograms,
    plot_top_saved_artists, plot_most_played_artist_per_month,
    plot_monthly_listening_time, plot_total_listening_time,
    plot_unique_artists_and_tracks, show_metrics_table
)

# --------------------------
# FILE PATHS / SETUP
# --------------------------
marquee_file_path = os.path.join('data', 'Marquee.json')

# Automatically get all StreamingHistory_music_*.json files
streaming_files = [
    f for f in os.listdir('data') 
    if f.startswith('StreamingHistory_music_') and f.endswith('.json')
]
streaming_file_paths = [os.path.join('data', file) for file in streaming_files]

# --------------------------
# SUPERLISTENERS
# --------------------------
superlisteners_counter = extract_superlisteners(marquee_file_path)

# --------------------------
# CALCULATE TOTAL MINUTES, UNIQUE ARTISTS/TRACKS
# --------------------------
total_minutes = calculate_total_listening_time(streaming_file_paths)
unique_artists = calculate_unique_artists(streaming_file_paths)
unique_tracks = calculate_unique_tracks(streaming_file_paths)

# --------------------------
# LOAD SPECIFIC STREAMING DATA
# (Example: we pick the first file to demonstrate loading a single dataset)
# --------------------------
file_path = os.path.join('data', 'StreamingHistory_music_0.json')
streaming_data = load_streaming_history(file_path)

# Re-extract superlisteners (if needed) from the same file or alternate
file_path = os.path.join('data', 'Marquee.json')  
superlisteners_counter = extract_superlisteners(file_path)

# --------------------------
# LOAD YOUR LIBRARY
# --------------------------
library_path = os.path.join('data', 'YourLibrary.json')
library_data = load_your_library(library_path)

# --------------------------
# ANALYZE & VISUALIZE SAVED ARTISTS
# --------------------------
top_saved_artists = get_top_saved_artists(library_data)
plot_top_saved_artists(top_saved_artists)

# --------------------------
# LOAD & COMBINE ALL STREAMING FILES
# --------------------------
# Instead of hardcoding multiple filenames, we reuse the streaming_files list:
all_data = []
for file_name in streaming_files:
    with open(os.path.join('data', file_name), 'r') as file:
        all_data.extend(pd.read_json(file).to_dict(orient='records'))

# --------------------------
# MOST PLAYED PER MONTH STATS
# --------------------------
most_played_stats = calculate_most_played_per_month(all_data)
most_played_artist_per_month = most_played_stats['most_played_artist_per_month']
total_playtime_minutes = most_played_stats['total_playtime_minutes']

# --------------------------
# VISUALIZE MOST PLAYED PER MONTH
# --------------------------
plot_most_played_artist_per_month(most_played_artist_per_month)
# If desired, you could also plot total_playtime_minutes here:
# plot_total_listening_time(total_playtime_minutes)

# --------------------------
# PROCESS & ANALYZE STREAMING DATA
# --------------------------
streaming_data = preprocess_streaming_data(streaming_data)
top_artists = get_top_artists(streaming_data)
monthly_trends = get_monthly_trends(streaming_data, top_artists)
hourly_trends = get_hourly_trends(streaming_data)
most_played_per_month = calculate_most_played_per_month(streaming_data)
top_played = calculate_top_played(streaming_data)

# --------------------------
# PLOTS USING THE COMBINED DATA
# --------------------------
plot_monthly_listening_time(all_data)
plot_top_10_tracks(all_data)

# --------------------------
# PLOTS USING PROCESSED single-file DATA
# --------------------------
plot_top_artists(top_artists)
plot_hourly_trends(hourly_trends)

# --------------------------
# ADDITIONAL PLOTS
# --------------------------
plot_superlisteners(superlisteners_counter)
# plot_total_listening_time(total_minutes)
# plot_unique_artists_and_tracks(unique_artists, unique_tracks)
show_metrics_table(total_minutes, unique_artists, unique_tracks)
