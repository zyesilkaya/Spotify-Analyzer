# visualizations.py

import os
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from collections import Counter

def plot_top_artists(top_artists, output_dir="results"):
    """
    Plot a bar chart of the top artists, both show and save to file.
    :param top_artists: A Pandas Series with artist names as index 
                        and total listening time (ms) as values.
    :param output_dir: Directory where the plot image will be saved.
    """
    # Make sure output_dir exists
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    top_artists.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Artists by Listening Time')
    plt.xlabel('Artist')
    plt.ylabel('Total Listening Time (ms)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save figure
    plt.savefig(os.path.join(output_dir, "top_artists.png"), bbox_inches='tight')
    plt.show()


def plot_monthly_trends(monthly_trends, output_dir="results"):
    """
    Plot a line chart of monthly trends for top artists.
    :param monthly_trends: DataFrame with months as index 
                           and top artists as columns.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    monthly_trends.plot(marker='o')
    plt.title('Monthly Listening Trends for Top Artists')
    plt.xlabel('Month')
    plt.ylabel('Total Listening Time (ms)')
    plt.grid(True)
    plt.legend(title='Artist', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, "monthly_trends.png"), bbox_inches='tight')
    plt.show()


def plot_hourly_trends(hourly_trends, output_dir="results"):
    """
    Plot an interactive bar chart of hourly listening trends.
    :param hourly_trends: A Pandas Series with hours as index 
                          and total listening time (ms) as values.
    :param output_dir: Directory where the plot image will be saved.
    """
    # For Plotly figures, we can save as HTML if you like, or screenshot.
    # Example below saves as HTML, but feel free to skip or adapt as needed.

    os.makedirs(output_dir, exist_ok=True)

    fig = px.bar(
        x=hourly_trends.index,
        y=hourly_trends.values,
        labels={'x': 'Hour of Day', 'y': 'Total Listening Time (ms)'},
        title='Listening Activity by Hour of Day',
        color=hourly_trends.values,
    )
    # Save to HTML if desired
    fig.write_html(os.path.join(output_dir, "hourly_trends.html"))

    # Also show in an interactive window
    fig.show()


def plot_top_tracks(top_tracks, output_dir="results"):
    """
    Plot the top tracks in a bar chart for each month.
    :param top_tracks: Dictionary with month as keys and 
                       a list of (track, playtime) tuples as values.
    :param output_dir: Directory where the plot image(s) will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    for month, tracks in top_tracks.items():
        track_names, playtimes = zip(*tracks)
        plt.figure(figsize=(10, 6))
        plt.barh(track_names, playtimes, color="orange")
        plt.title(f"Top 5 Tracks for {month}")
        plt.xlabel("Playtime (ms)")
        plt.tight_layout()

        # Generate a unique filename per month
        safe_month = str(month).replace("/", "-")
        plt.savefig(os.path.join(output_dir, f"top_tracks_{safe_month}.png"), bbox_inches='tight')
        plt.show()


def plot_top_artists_bar(top_artists, output_dir="results"):
    """
    Plot the top artists in a horizontal bar chart for each month.
    :param top_artists: Dictionary with month as keys and 
                        a list of (artist, playtime) tuples as values.
    :param output_dir: Directory where the plot image(s) will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    for month, artists in top_artists.items():
        artist_names, playtimes = zip(*artists)
        plt.figure(figsize=(10, 6))
        plt.barh(artist_names, playtimes, color="purple")
        plt.title(f"Top 5 Artists for {month}")
        plt.xlabel("Playtime (ms)")
        plt.tight_layout()

        safe_month = str(month).replace("/", "-")
        plt.savefig(os.path.join(output_dir, f"top_artists_{safe_month}.png"), bbox_inches='tight')
        plt.show()


def plot_artist_playtime_histograms(df, output_dir="results"):
    """
    Plot histograms for artist playtime distribution.
    :param df: DataFrame containing 'artistName' and 'msPlayed'.
    :param output_dir: Directory where the plots will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    artist_playtime = df.groupby('artistName')['msPlayed'].sum() / (1000 * 60 * 60)

    # Single histogram
    plt.figure(figsize=(12, 6))
    plt.hist(artist_playtime, bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Listening Time by Artist')
    plt.xlabel('Hours Played')
    plt.ylabel('Number of Artists')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "artist_playtime_histogram_30bins.png"), bbox_inches='tight')
    plt.show()

    # Histograms with different bin sizes
    plt.figure(figsize=(15, 10))
    for i, bins in enumerate([10, 30, 50], start=1):
        plt.subplot(3, 1, i)
        plt.hist(
            artist_playtime,
            bins=bins,
            color=['skyblue', 'lightgreen', 'lightcoral'][i-1],
            edgecolor='black'
        )
        plt.title(f'Histogram with {bins} Bins')
        plt.xlabel('Hours Played')
        plt.ylabel('Number of Artists')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "artist_playtime_histograms_various_bins.png"), bbox_inches='tight')
    plt.show()


def plot_top_saved_artists(top_artists, output_dir="results"):
    """
    Plot the top saved artists in a horizontal bar chart.
    :param top_artists: List of (artist, count) tuples.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    artists, counts = zip(*top_artists)
    plt.figure(figsize=(12, 6))
    plt.barh(artists, counts, color='lightblue')
    plt.xlabel('Number of Tracks Saved')
    plt.title('Top Saved Artists in Your Library')
    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig(os.path.join(output_dir, "top_saved_artists.png"), bbox_inches='tight')
    plt.show()


def plot_most_played_artist_per_month(most_played_artist_per_month, output_dir="results"):
    """
    Plot the most played artist per month.
    :param most_played_artist_per_month: Dict with month as key and (artist, playtime) as value.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

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
    plt.savefig(os.path.join(output_dir, "most_played_artist_per_month.png"), bbox_inches='tight')
    plt.show()


def plot_monthly_listening_time(all_data, output_dir="results"):
    """
    Plot total listening time per month from a combined list of streaming dictionaries.
    :param all_data: List of dictionaries from JSON streaming files.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(all_data)
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['month'] = df['endTime'].dt.to_period('M')

    monthly_playtime = df.groupby('month')['msPlayed'].sum() / (1000 * 60)

    plt.figure(figsize=(12, 6))
    monthly_playtime.plot(kind='bar', color='lightblue', width=0.8)
    plt.title("Total Listening Time Per Month", fontsize=16)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Minutes Played", fontsize=14)
    plt.xticks(rotation=45)

    for index, value in enumerate(monthly_playtime):
        plt.text(index, value, f"{value:.0f}", ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_listening_time.png"), bbox_inches='tight')
    plt.show()


def plot_top_10_tracks(all_data, output_dir="results"):
    """
    Plot the top 10 most played tracks (in minutes).
    :param all_data: List of dictionaries from JSON streaming files.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(all_data)
    track_playtime = df.groupby('trackName')['msPlayed'].sum()
    track_playtime_minutes = track_playtime / (1000 * 60)
    top_10_tracks = track_playtime_minutes.nlargest(10)

    plt.figure(figsize=(12, 6))
    top_10_tracks.plot(kind='barh', color='lightcoral')
    plt.title("Top 10 Most Played Tracks", fontsize=16)
    plt.xlabel("Minutes Played", fontsize=14)
    plt.ylabel("Track Name", fontsize=14)
    plt.gca().invert_yaxis()  # Most played track on top

    for index, value in enumerate(top_10_tracks):
        plt.text(value, index, f"{value:.1f} min", va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_10_tracks.png"), bbox_inches='tight')
    plt.show()


def plot_superlisteners(counter_data, output_dir="results"):
    """
    Plots the superlisteners using a horizontal bar chart.
    :param counter_data: Counter object with artist names and their frequencies.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    artists, counts = zip(*counter_data.most_common())
    plt.figure(figsize=(10, 6))
    plt.barh(artists, counts, color='skyblue')
    plt.title("Super Listeners - Most Frequent Artists", fontsize=16)
    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Artist Name", fontsize=14)
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "superlisteners.png"), bbox_inches='tight')
    plt.show()


def plot_total_listening_time(total_minutes, output_dir="results"):
    """
    Visualize total listening time as a single bar.
    :param total_minutes: Total listening time in minutes.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(6, 6))
    plt.bar(["Total Listening Time"], [total_minutes], color='lightgreen')
    plt.title("Total Listening Time", fontsize=16)
    plt.ylabel("Time (Minutes)", fontsize=14)
    plt.text(0, total_minutes, f"{total_minutes:.2f} min", ha='center', va='bottom', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "total_listening_time.png"), bbox_inches='tight')
    plt.show()


def plot_unique_artists_and_tracks(unique_artists, unique_tracks, output_dir="results"):
    """
    Visualize the number of unique artists and tracks as a grouped bar chart.
    :param unique_artists: Number of unique artists.
    :param unique_tracks: Number of unique tracks.
    :param output_dir: Directory where the plot image will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    categories = ["Unique Artists", "Unique Tracks"]
    values = [unique_artists, unique_tracks]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['skyblue', 'lightcoral'])
    plt.title("Unique Artists and Tracks", fontsize=16)
    plt.ylabel("Count", fontsize=14)

    for i, value in enumerate(values):
        plt.text(i, value, str(value), ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "unique_artists_and_tracks.png"), bbox_inches='tight')
    plt.show()

def show_metrics_table(total_minutes, unique_artists, unique_tracks, output_dir="results"):
    """
    Display total listening time, unique artists, and unique tracks 
    in a simple table.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Prepare data in a Pandas DataFrame
    data = [
        ["Total Listening Time (min)", f"{total_minutes:.2f}"],
        ["Unique Artists", str(unique_artists)],
        ["Unique Tracks", str(unique_tracks)]
    ]
    df = pd.DataFrame(data, columns=["Metric", "Value"])

    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('tight')
    ax.axis('off')  # Hide x- and y-axis

    # Create a table in the center of the axes
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )

    # Optionally adjust font size & scaling
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)  # Make the table larger if needed

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "overall_metrics_table.png"), bbox_inches='tight')
    plt.show()
