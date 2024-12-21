import os
from data_processing import load_streaming_history, preprocess_streaming_data, get_top_artists, get_monthly_trends, get_hourly_trends
from visualizations import plot_top_artists, plot_monthly_trends, plot_hourly_trends

# Load data
file_path = os.path.join('data', 'StreamingHistory_music_0.json')
streaming_data = load_streaming_history(file_path)

# Process data
streaming_data = preprocess_streaming_data(streaming_data)
top_artists = get_top_artists(streaming_data)
monthly_trends = get_monthly_trends(streaming_data, top_artists)
hourly_trends = get_hourly_trends(streaming_data)

# Visualize data
plot_top_artists(top_artists)
plot_monthly_trends(monthly_trends)
plot_hourly_trends(hourly_trends)
