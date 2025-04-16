import pandas as pd
import matplotlib.pyplot as plt
from IPython import display
import datetime

def convert_time_to_seconds(time_str):
    """
    Convert a time string in the format HH:MM:SS.millis to seconds.
    Example: "00:00:05.802" -> 5.802 seconds.
    """
    dt = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6
    return seconds

def plot_attempts_score_time(csv_file):
    """
    Reads a CSV file with columns attempt, score, and time.
    It converts the time column to seconds and plots:
      - Attempts vs. Score
      - Attempts vs. Time (seconds)
    
    Both series are plotted as lines with markers in a separate plot window.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert "time" column from "HH:MM:SS.millis" format to seconds
    df["time_seconds"] = df["time"].apply(convert_time_to_seconds)
    
    # Create a new figure for the plot
    plt.figure(figsize=(10, 6))
    
    # Plot the score data (line with markers)
    plt.plot(df["attempt"], df["score"], marker='o', label="Score")
    
    # Plot the time (in seconds) data (line with markers)
    plt.plot(df["attempt"], df["time_seconds"], marker='o', label="Time (s)")
    
    # Set labels and title
    plt.xlabel("Attempt")
    plt.ylabel("Value")
    plt.title("Attempts vs. Score and Time")
    
    # Add a legend to differentiate the lines.
    plt.legend()
    
    # Optionally, add a grid to improve readability.
    plt.grid(True)
    
    # Display the plot in a separate window.
    plt.show()

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)