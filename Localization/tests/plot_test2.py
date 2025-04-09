import matplotlib.pyplot as plt
import numpy as np
import time

# Number of devices
num_devices = 5

# Initialize distances with random values
distances = np.random.rand(num_devices) * 10

# Store history of distances with timestamps
history_data = []

# Alpha fading parameters (More extreme fading)
min_alpha = 0.05  # More transparent at the lowest
max_alpha = 1.0  # Fully visible for the latest data
history_length = 6  # Reduce stored history for quicker fading

# Simulate updates
for _ in range(20):
    plt.clf()

    # Store current state in history
    timestamp = time.time()
    history_data.append((distances.copy(), timestamp))

    # Keep only the most recent `history_length` updates
    history_data = history_data[-history_length:]

    # Compute alpha values based on recency
    timestamps = np.array([t for _, t in history_data])
    time_diff = timestamps - timestamps[0]  # Normalize to start at 0

    if time_diff.max() > 1:
        fade_factor = 2  # Increase this to make older points fade even faster
        alpha_values = np.clip(max_alpha - fade_factor * (time_diff / time_diff.max()) * (max_alpha - min_alpha), min_alpha, max_alpha)
    else:
        alpha_values = [max_alpha] * len(history_data)

    # Plot historical points with strong fading effect
    for (hist_distances, _), alpha in zip(history_data, alpha_values):
        plt.plot(range(1, len(hist_distances) + 1), hist_distances, 'ro', alpha=alpha)

    # Simulate movement (5% change per step)
    distances += 0.5 * np.random.randn(num_devices)
    distances = np.clip(distances, 0, 10)  # Keep distances in range

    # Labels and display
    plt.ylim(0, 10)  # Max display range
    plt.xlabel("Device Nr.")
    plt.ylabel("Distance (m)")
    plt.pause(0.5)

plt.show()

