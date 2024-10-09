import os
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def plot_data(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert 'snapped_at' to datetime
    df["snapped_at"] = pd.to_datetime(df["snapped_at"])

    # Calculate the ratio of total_volume to market_cap
    df["ratio"] = df["total_volume"] / df["market_cap"]

    # Create the figure and axis objects
    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Plot ratio on the left y-axis
    color = "tab:blue"
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Total Volume / Market Cap Ratio", color=color)
    ax1.plot(df["snapped_at"], df["ratio"], color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    # Create a second y-axis for price
    ax2 = ax1.twinx()
    color = "tab:orange"
    ax2.set_ylabel("Price", color=color)
    ax2.plot(df["snapped_at"], df["price"], color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    # Set x-axis format
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # Add title
    plt.title("Total Volume / Market Cap Ratio and Price Over Time")

    # Add grid
    ax1.grid(True)

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

    # Generate output file name
    output_file = f"{os.path.splitext(input_file)[0]}_chart.png"

    # Save the figure
    plt.savefig(output_file, dpi=300)
    print(f"Chart saved as {output_file}")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <input_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    plot_data(input_file)
