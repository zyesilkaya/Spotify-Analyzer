# visualizations.py

import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
import pandas as pd
def plot_top_artists(top_artists):
    """Plot a bar chart of the top artists."""
    plt.figure(figsize=(10, 6))
    top_artists.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Artists by Listening Time')
    plt.xlabel('Artist')
    plt.ylabel('Total Listening Time (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_monthly_trends(monthly_trends):
    """Plot a line chart of monthly trends for top artists."""
    plt.figure(figsize=(2, 6))
    monthly_trends.plot(marker='o')
    plt.title('Monthly Listening Trends for Top Artists')
    plt.xlabel('Month')
    plt.ylabel('Total Listening Time (ms)')
    plt.grid(True)
    plt.legend(title='Artist', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_hourly_trends(hourly_trends):
    """Plot an interactive heatmap of hourly listening trends."""
    fig = px.bar(
        x=hourly_trends.index,
        y=hourly_trends.values,
        labels={'x': 'Hour of Day', 'y': 'Total Listening Time (ms)'},
        title='Listening Activity by Hour of Day',
        color=hourly_trends.values,
    )
    fig.show()

def plot_top_tracks(top_tracks):
    """Plot the top tracks in a bar chart."""
    for month, tracks in top_tracks.items():
        track_names, playtimes = zip(*tracks)
        plt.figure(figsize=(10, 6))
        plt.barh(track_names, playtimes, color="orange")
        plt.title(f"Top 5 Tracks for {month}")
        plt.xlabel("Playtime (ms)")
        plt.tight_layout()
        plt.show()

def plot_top_artists_bar(top_artists):
    """Plot the top artists in a horizontal bar chart."""
    for month, artists in top_artists.items():
        artist_names, playtimes = zip(*artists)
        plt.figure(figsize=(10, 6))
        plt.barh(artist_names, playtimes, color="purple")
        plt.title(f"Top 5 Artists for {month}")
        plt.xlabel("Playtime (ms)")
        plt.tight_layout()
        plt.show()

def plot_artist_playtime_histograms(df):
    """Plot histograms for artist playtime distribution."""
    artist_playtime = df.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)

    # Single histogram
    plt.figure(figsize=(12, 6))
    plt.hist(artist_playtime, bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Listening Time by Artist')
    plt.xlabel('Hours Played')
    plt.ylabel('Number of Artists')
    plt.tight_layout()
    plt.show()

    # Histograms with different bin sizes
    plt.figure(figsize=(15, 10))
    for i, bins in enumerate([10, 30, 50], start=1):
        plt.subplot(3, 1, i)
        plt.hist(artist_playtime, bins=bins, color=['skyblue', 'lightgreen', 'lightcoral'][i-1], edgecolor='black')
        plt.title(f'Histogram with {bins} Bins')
        plt.xlabel('Hours Played')
        plt.ylabel('Number of Artists')
    plt.tight_layout()
    plt.show()

def plot_top_saved_artists(top_artists):
    """Plot the top saved artists in a horizontal bar chart."""
    artists, counts = zip(*top_artists)
    plt.figure(figsize=(12, 6))
    plt.barh(artists, counts, color='lightblue')
    plt.xlabel('Number of Tracks Saved')
    plt.title('Top Saved Artists in Your Library')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def plot_genre_diversity(genre_counts):
    """Plot genre diversity as a pie chart."""
    labels, sizes = zip(*genre_counts.items())
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Genre Diversity in Your Library')
    plt.axis('equal')  # Equal aspect ratio ensures a perfect circle
    plt.tight_layout()
    plt.show()

def plot_most_played_artist_per_month(most_played_artist_per_month):
    """Plot the most played artist per month."""
    months = list(most_played_artist_per_month.keys())
    artists = [artist for artist, _ in most_played_artist_per_month.values()]
    playtimes = [playtime / (1000 * 60) for _, playtime in most_played_artist_per_month.values()]

    plt.figure(figsize=(12, 6))
    plt.bar(months, playtimes, color="skyblue")
    plt.title("Most Played Artist Per Month", fontsize=16)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Listening Time (Minutes)", fontsize=14)
    plt.xticks(rotation=45)
    for i, artist in enumerate(artists):
        plt.text(months[i], playtimes[i], artist, ha='center', va='bottom', fontsize=10, rotation=45)
    plt.tight_layout()
    plt.show()

def plot_total_listening_time(total_playtime_minutes):
    """Plot the total listening time as a single bar."""
    plt.figure(figsize=(6, 6))
    plt.bar(["Total Listening Time"], [total_playtime_minutes], color="lightgreen")
    plt.title("Total Listening Time", fontsize=16)
    plt.ylabel("Time (Minutes)", fontsize=14)
    for i, val in enumerate([total_playtime_minutes]):
        plt.text(i, val, f"{val:.2f} minutes", ha='center', va='bottom', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_monthly_listening_time(all_data):
    """Plot total listening time per month."""
    # Convert the data to a DataFrame
    df = pd.DataFrame(all_data)
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['month'] = df['endTime'].dt.to_period('M')

    # Group by month and calculate total playtime in minutes
    monthly_playtime = df.groupby('month')['msPlayed'].sum() / (1000 * 60)

    # Plot
    plt.figure(figsize=(12, 6))
    monthly_playtime.plot(kind='bar', color='lightblue', width=0.8)
    plt.title("Total Listening Time Per Month", fontsize=16)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Minutes Played", fontsize=14)
    plt.xticks(rotation=45)
    for index, value in enumerate(monthly_playtime):
        plt.text(index, value, f"{value:.0f}", ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.show()

def plot_top_10_tracks(all_data):
    """Plot the top 10 most played tracks."""
    # Convert the data to a DataFrame
    df = pd.DataFrame(all_data)

    # Group by track name and sum the playtime
    track_playtime = df.groupby('trackName')['msPlayed'].sum()

    # Convert playtime to minutes and get the top 10 tracks
    track_playtime_minutes = track_playtime / (1000 * 60)
    top_10_tracks = track_playtime_minutes.nlargest(10)

    # Plot
    plt.figure(figsize=(12, 6))
    top_10_tracks.plot(kind='barh', color='lightcoral')
    plt.title("Top 10 Most Played Tracks", fontsize=16)
    plt.xlabel("Minutes Played", fontsize=14)
    plt.ylabel("Track Name", fontsize=14)
    plt.gca().invert_yaxis()  # Invert the y-axis to have the most played track on top
    for index, value in enumerate(top_10_tracks):
        plt.text(value, index, f"{value:.1f} min", va='center', fontsize=10)
    plt.tight_layout()
    plt.show()

def plot_superlisteners(counter_data):
    """
    Plots the superlisteners using a horizontal bar chart.
    :param counter_data: Counter object with artist names and their frequencies.
    """
    # Sort data by frequency
    artists, counts = zip(*counter_data.most_common())
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(artists, counts, color='skyblue')
    plt.title("Super Listeners - Most Frequent Artists", fontsize=16)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Artist Name", fontsize=14)
    plt.gca().invert_yaxis()  # Have the most frequent artist on top
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt

def plot_superlisteners(counter_data):
    """
    Plots the superlisteners using a horizontal bar chart.
    :param counter_data: Counter object with artist names and their frequencies.
    """
    # Sort data by frequency
    artists, counts = zip(*counter_data.most_common())
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(artists, counts, color='skyblue')
    plt.title("Super Listeners - Most Frequent Artists", fontsize=16)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Artist Name", fontsize=14)
    plt.gca().invert_yaxis()  # Have the most frequent artist on top
    plt.tight_layout()
    plt.show()

def plot_total_listening_time(total_minutes):
    """
    Visualizes total listening time as a single bar.
    :param total_minutes: Total listening time in minutes.
    """
    plt.figure(figsize=(6, 6))
    plt.bar(["Total Listening Time"], [total_minutes], color='lightgreen')
    plt.title("Total Listening Time", fontsize=16)
    plt.ylabel("Time (Minutes)", fontsize=14)
    plt.text(0, total_minutes, f"{total_minutes:.2f} min", ha='center', va='bottom', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_unique_artists_and_tracks(unique_artists, unique_tracks):
    """
    Visualizes the number of unique artists and tracks as a grouped bar chart.
    :param unique_artists: Number of unique artists.
    :param unique_tracks: Number of unique tracks.
    """
    categories = ["Unique Artists", "Unique Tracks"]
    values = [unique_artists, unique_tracks]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['skyblue', 'lightcoral'])
    plt.title("Unique Artists and Tracks", fontsize=16)
    plt.ylabel("Count", fontsize=14)
    for i, value in enumerate(values):
        plt.text(i, value, str(value), ha='center', va='bottom', fontsize=12)
    plt.tight_layout()
    plt.show()
