import matplotlib.pyplot as plt
import plotly.express as px

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
    plt.figure(figsize=(12, 6))
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
