import os
import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


def calculate_ema(data, span):
    return data.ewm(span=span, adjust=False).mean()

def plot_data(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert 'snapped_at' to datetime
    df["snapped_at"] = pd.to_datetime(df["snapped_at"])

    # Calculate the ratio of total_volume to market_cap
    df["ratio"] = df["total_volume"] / df["market_cap"]

    # Calculate 20-day and 50-day Simple Moving Averages
    df["SMA20"] = df["price"].rolling(window=20).mean()
    df["SMA50"] = df["price"].rolling(window=50).mean()

    # Calculate 21-day EMA
    df["EMA21"] = calculate_ema(df["price"], 21)

    # Create the figure and axis objects
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20), sharex=True)

    # Plot ratio on the first subplot
    color = "tab:blue"
    ax1.set_ylabel("Total Volume / Market Cap Ratio", color=color)
    ax1.plot(df["snapped_at"], df["ratio"], color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True)
    ax1.set_title("Total Volume / Market Cap Ratio Over Time")

    # Plot price and moving averages on the second subplot
    ax2.set_ylabel("Price")
    ax2.plot(df["snapped_at"], df["price"], color="tab:orange", label="Price")
    ax2.plot(df["snapped_at"], df["SMA20"], color="tab:red", label="20-day SMA")
    ax2.plot(df["snapped_at"], df["SMA50"], color="tab:green", label="50-day SMA")
    ax2.plot(df["snapped_at"], df["EMA21"], color="purple", label="21-day EMA", linestyle="--")
    ax2.tick_params(axis="y")
    ax2.grid(True)
    ax2.legend()
    ax2.set_title("Price and Moving Averages Over Time")

    # Plot volume on the third subplot
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Volume")
    ax3.bar(df["snapped_at"], df["total_volume"], color="tab:purple", alpha=0.7)
    ax3.tick_params(axis="y")
    ax3.grid(True)
    ax3.set_title("Trading Volume Over Time")

    # Set x-axis format
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax3.xaxis.set_major_locator(mdates.AutoDateLocator())

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

    # Generate output file name
    output_file = f"{os.path.splitext(input_file)[0]}_advanced_chart.png"

    # Save the figure
    plt.savefig(output_file, dpi=300)
    print(f"Advanced chart saved as {output_file}")

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
