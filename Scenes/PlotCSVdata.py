import pandas as pd
import matplotlib.pyplot as plt
import sys


def plot_csv_data(file_path):
    df = pd.read_csv(file_path)

    # Check if the CSV file contains the required columns
    required_columns = {"attempt", "time", "score"}
    if not required_columns.issubset(df.columns):
        print("Error: CSV file must contain attempt, time, and score columns.")
        return

    # Convert attempt numbers and scores to integers
    df['attempt'] = df['attempt'].astype(int)
    df['score'] = df['score'].astype(int)
    
    # Find the last occurrence of attempt 0 (most recent game start)
    last_start = df[df['attempt'] == 0].index[-1]
    
    # Get only the data from the most recent game
    recent_df = df.iloc[last_start:]
    
    # Convert time strings to seconds
    def time_to_seconds(time_str):
        h, m, s = time_str.split(':')
        return float(h) * 3600 + float(m) * 60 + float(s)
    
    recent_df['time_seconds'] = recent_df['time'].apply(time_to_seconds)
    
    # Sort by attempt number to ensure correct line connections
    recent_df = recent_df.sort_values('attempt')

    # Create figure with single subplot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot time on left y-axis
    color1 = 'tab:blue'
    ax1.set_xlabel('Attempt Number')
    ax1.set_ylabel('Time (seconds)', color=color1)
    line1 = ax1.plot(recent_df["attempt"], recent_df["time_seconds"], color=color1, marker='o', 
                     linestyle='-', label='Time')
    ax1.tick_params(axis='y', labelcolor=color1)

    # Create second y-axis for score
    color2 = 'tab:red'
    ax2 = ax1.twinx()
    ax2.set_ylabel('Score', color=color2)
    line2 = ax2.plot(recent_df["attempt"], recent_df["score"], color=color2, marker='s', 
                     linestyle='-', label='Score')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Ensure y-axis for score shows whole numbers
    ax2.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # Ensure x-axis shows whole numbers
    ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Add title and legend
    plt.title("Snake Game Performance (Current Session)")
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
    else:
        plot_csv_data(sys.argv[1])