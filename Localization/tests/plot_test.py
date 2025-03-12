import matplotlib.pyplot as plt
import numpy as np
import time

# Create figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')  # Initialize an empty line

def update_plot(x_data, y_data):
    """Update the existing plot with new data."""
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    
    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Rescale view
    
    plt.draw()  # Redraw the figure
    plt.pause(0.1)  # Allow GUI events to update

# Show the plot without blocking
plt.ion()  # Turn on interactive mode
plt.show()

# Example loop to update the plot dynamically
for i in range(50):
    x_vals = np.linspace(0, 10, 100)
    y_vals = np.sin(x_vals + i * 0.1)  # Vary the sine wave
    
    update_plot(x_vals, y_vals)  # Update the same plot
    
    print(f"Iteration {i}")
    time.sleep(0.5)  # Simulate other code running

plt.ioff()  # Turn off interactive mode when done
