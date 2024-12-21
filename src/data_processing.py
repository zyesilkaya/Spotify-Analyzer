import pandas as pd

def load_streaming_history(file_path):
    """Load streaming history data from a JSON file."""
    return pd.read_json(file_path)

def preprocess_streaming_data(df):
    """Extract useful time-based features from the data."""
    df['endTime'] = pd.to_datetime(df['endTime'])
    df['hour'] = df['endTime'].dt.hour
    df['month'] = df['endTime'].dt.to_period('M')
    return df

def get_top_artists(df, top_n=10):
    """Get the top N artists by listening time."""
    return df.groupby('artistName')['msPlayed'].sum().sort_values(ascending=False).head(top_n)

def get_monthly_trends(df, top_artists):
    """Compute monthly listening trends for top artists."""
    return (
        df[df['artistName'].isin(top_artists.index)]
        .groupby(['month', 'artistName'])['msPlayed']
        .sum()
        .unstack(fill_value=0)
    )

def get_hourly_trends(df):
    """Compute total listening time for each hour of the day."""
    return df.groupby('hour')['msPlayed'].sum()
