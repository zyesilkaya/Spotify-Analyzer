# data_processing.py

import json
import pandas as pd
from datetime import datetime
from collections import defaultdict, Counter

def extract_superlisteners(file_path):
    """
    Extracts the artists categorized as 'Super Listeners' from the Marquee.json file.
    :param file_path: Path to the Marquee.json file.
    :return: A Counter object containing artist names and their counts.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        marquee_data = json.load(file)
    
    superlisteners = [entry["artistName"] for entry in marquee_data if entry["segment"] == "Super Listeners"]
    return Counter(superlisteners)

def load_streaming_data(file_paths):
    """
    Loads and concatenates streaming history JSON files into a single DataFrame.
    :param file_paths: List of file paths to streaming history JSON files.
    :return: A Pandas DataFrame containing all streaming history data.
    """
    dfs = [pd.read_json(fp) for fp in file_paths]
    return pd.concat(dfs, ignore_index=True)

def calculate_total_listening_time(file_paths):
    """
    Calculates the total listening time in minutes from the streaming history files.
    :param file_paths: List of file paths to streaming history JSON files.
    :return: Total listening time in minutes.
    """
    df = load_streaming_data(file_paths)
    return df['msPlayed'].sum() / (1000 * 60)

def calculate_unique_artists(file_paths):
    """
    Counts the number of unique artists listened to.
    :param file_paths: List of file paths to streaming history JSON files.
    :return: Number of unique artists.
    """
    df = load_streaming_data(file_paths)
    return df['artistName'].nunique()

def calculate_unique_tracks(file_paths):
    """
    Counts the number of unique tracks listened to.
    :param file_paths: List of file paths to streaming history JSON files.
    :return: Number of unique tracks.
    """
    df = load_streaming_data(file_paths)
    return df['trackName'].nunique()

def load_streaming_history(file_path):
    """
    Load streaming history data from a JSON file into a DataFrame.
    """
    return pd.read_json(file_path)

def preprocess_streaming_data(df):
    """
    Extract time-based features from the streaming data (hour, month).
    :param df: DataFrame with 'endTime' and 'msPlayed' columns.
    :return: The same DataFrame with new columns (hour, month).
    """
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['hour'] = df['endTime'].dt.hour
    df['month'] = df['endTime'].dt.to_period('M')
    return df

def get_top_artists(df, top_n=10):
    """
    Get the top N artists by total listening time.
    :param df: DataFrame with 'artistName' and 'msPlayed'.
    :param top_n: Number of top artists to get.
    :return: Series of top_n artists with listening time in descending order.
    """
    return df.groupby('artistName')['msPlayed'].sum().sort_values(ascending=False).head(top_n)

def get_monthly_trends(df, top_artists):
    """
    Compute monthly listening trends for top artists.
    :param df: DataFrame with time info.
    :param top_artists: Index of top artists from get_top_artists().
    :return: DataFrame pivoted with months as rows and artists as columns.
    """
    return (
        df[df['artistName'].isin(top_artists.index)]
        .groupby(['month', 'artistName'])['msPlayed']
        .sum()
        .unstack(fill_value=0)
    )

def get_hourly_trends(df):
    """
    Compute total listening time for each hour of the day.
    :param df: DataFrame with 'hour' and 'msPlayed'.
    :return: Series with hour as index and total msPlayed as values.
    """
    return df.groupby('hour')['msPlayed'].sum()

def calculate_most_played_per_month(all_data):
    """
    Calculate the most played artist for each month and total playtime across all months.
    :param all_data: List of dictionaries containing streaming data (endTime, artistName, msPlayed).
    :return: Dictionary with 'most_played_artist_per_month' and 'total_playtime_minutes'.
    """
    df = pd.DataFrame(all_data)
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['month'] = df['endTime'].dt.to_period('M')

    # Group by month and artist, sum the playtime
    monthly_artist_playtime = df.groupby(['month', 'artistName'])['msPlayed'].sum().reset_index()
    # Find the artist with max playtime per month
    idx = monthly_artist_playtime.groupby('month')['msPlayed'].idxmax()
    most_played_artist_per_month = monthly_artist_playtime.loc[idx]

    most_played_artist_per_month_dict = {
        str(row['month']): (row['artistName'], row['msPlayed'])
        for _, row in most_played_artist_per_month.iterrows()
    }

    # Calculate total playtime in minutes
    total_playtime_minutes = df['msPlayed'].sum() / (1000 * 60)

    return {
        "most_played_artist_per_month": most_played_artist_per_month_dict,
        "total_playtime_minutes": total_playtime_minutes
    }

def calculate_top_played(df):
    """
    Get the top 5 artists and tracks per month.
    :param df: DataFrame with 'artistName', 'trackName', 'msPlayed', 'endTime'.
    :return: Dictionary of top 5 artists and top 5 tracks per month.
    """
    monthly_artist_playtime = defaultdict(lambda: defaultdict(int))
    monthly_track_playtime = defaultdict(lambda: defaultdict(int))

    for _, row in df.iterrows():
        artist = row['artistName']
        track = row['trackName']
        playtime = row['msPlayed']
        month = row['endTime'].strftime("%Y-%m")

        monthly_artist_playtime[month][artist] += playtime
        monthly_track_playtime[month][track] += playtime

    return {
        "artists": {
            month: sorted(artists.items(), key=lambda x: x[1], reverse=True)[:5]
            for month, artists in monthly_artist_playtime.items()
        },
        "tracks": {
            month: sorted(tracks.items(), key=lambda x: x[1], reverse=True)[:5]
            for month, tracks in monthly_track_playtime.items()
        }
    }

def load_your_library(file_path):
    """
    Load and process the YourLibrary.json data.
    :param file_path: Path to YourLibrary.json.
    :return: DataFrame of tracks.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data['tracks'])

def get_top_saved_artists(library_df, top_n=10):
    """
    Get the most saved artists in the user's library.
    :param library_df: DataFrame of library data.
    :param top_n: Number of top artists to retrieve.
    :return: List of (artist, count) tuples.
    """
    artist_counts = Counter(library_df['artist'].fillna('Unknown'))
    return artist_counts.most_common(top_n)

