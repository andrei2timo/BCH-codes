import sys, os
import time
import psutil
import matplotlib.pyplot as plt

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import BCH

# Test data for encoding
encoding_input = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1],
    [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2],
    [8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3],
    [9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4],
    [10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5],
    [11, 12, 13, 14, 15, 16, 1, 2, 3, 4, 5, 6],
    [12, 13, 14, 15, 16, 1, 2, 3, 4, 5, 6, 7],
    [13, 14, 15, 16, 1, 2, 3, 4, 5, 6, 7, 8],
    [14, 15, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [15, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    [1, 3, 5, 7, 9, 11, 13, 15, 2, 4, 6, 8],
    [2, 4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7],
    [3, 5, 7, 9, 11, 13, 15, 2, 4, 6, 8, 10],
    [4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9],
    [5, 7, 9, 11, 13, 15, 2, 4, 6, 8, 10, 12],
    [6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9, 11],
    [7, 9, 11, 13, 15, 2, 4, 6, 8, 10, 12, 14],
    [8, 10, 12, 14, 16, 1, 3, 5, 7, 9, 11, 13],
    [9, 11, 13, 15, 2, 4, 6, 8, 10, 12, 14, 16],
    [10, 12, 14, 16, 1, 3, 5, 7, 9, 11, 13, 15],
    [11, 13, 15, 2, 4, 6, 8, 10, 12, 14, 16, 1],
    [12, 14, 16, 1, 3, 5, 7, 9, 11, 13, 15, 2],
]

# Test data for error correction
error_correction_input = [
    [5, 3, 2, 8, 6, 9, 1, 1, 2, 6, 7, 4, 15, 1, 14, 9],
    [6, 4, 3, 9, 7, 10, 2, 2, 3, 7, 8, 5, 16, 2, 15, 10],
    [7, 5, 4, 10, 8, 11, 3, 3, 4, 8, 9, 6, 1, 3, 16, 11],
    [8, 6, 5, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [9, 7, 6, 12, 10, 13, 5, 5, 6, 10, 11, 8, 3, 5, 2, 13],
    [10, 8, 7, 13, 11, 14, 6, 6, 7, 11, 12, 9, 4, 6, 3, 14],
    [11, 9, 8, 14, 12, 15, 7, 7, 8, 12, 13, 10, 5, 7, 4, 15],
    [12, 10, 9, 15, 13, 16, 8, 8, 9, 13, 14, 11, 6, 8, 5, 16],
    [13, 11, 10, 16, 14, 1, 9, 9, 10, 14, 15, 12, 7, 9, 6, 1],
    [14, 12, 11, 1, 15, 2, 10, 10, 11, 15, 16, 13, 8, 10, 7, 2],
    [7, 6, 5, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [1, 1, 1, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [8, 6, 2, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [8, 5, 3, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [12, 6, 5, 11, 9, 12, 4, 4, 5, 9, 10, 7, 2, 4, 1, 12],
    [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [1, 3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 14],
    [2, 4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9, 11, 13, 15],
    [3, 5, 7, 9, 11, 13, 15, 1, 2, 4, 6, 8, 10, 12, 14, 16],
    [4, 6, 8, 10, 12, 14, 16, 2, 3, 5, 7, 9, 11, 13, 15, 1],
    [5, 7, 9, 11, 13, 15, 1, 3, 4, 6, 8, 10, 12, 14, 16, 2],
    [6, 8, 10, 12, 14, 16, 2, 4, 5, 7, 9, 11, 13, 15, 1, 3],
    [7, 9, 11, 13, 15, 1, 3, 5, 6, 8, 10, 12, 14, 16, 2, 4],
    [8, 10, 12, 14, 16, 2, 4, 6, 7, 9, 11, 13, 15, 1, 3, 5],
    [9, 11, 13, 15, 1, 3, 5, 7, 8, 10, 12, 14, 16, 2, 4, 6],
    [10, 12, 14, 16, 2, 4, 6, 8, 9, 11, 13, 15, 1, 3, 5, 7],
    [11, 13, 15, 1, 3, 5, 7, 9, 10, 12, 14, 16, 2, 4, 6, 8],
    [12, 14, 16, 2, 4, 6, 8, 10, 11, 13, 15, 1, 3, 5, 7, 9],
    [13, 15, 1, 3, 5, 7, 9, 11, 12, 14, 16, 2, 4, 6, 8, 10],
    [14, 16, 2, 4, 6, 8, 10, 12, 13, 15, 1, 3, 5, 7, 9, 11],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1],
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2],
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3],
    [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2, 3, 4],
]

def test_error_correction_performance(ax):
    original_data = [input_data[:12] for input_data in error_correction_input]
    encoded_data = [BCH.BCHGenerator(input_data) for input_data in original_data]

    # Introduce errors
    error_data = [data[:] for data in encoded_data]
    error_count = []
    for i, data in enumerate(error_data):
        errors_introduced = 0
        data[5] = (data[5] + 1) % 16
        data[10] = (data[10] + 2) % 16
        errors_introduced += 2
        error_count.append(errors_introduced)

    corrected_data = [BCH.bch_syndrome_generator(input_data) for input_data in error_data]

    # Check for errors corrected vs introduced
    errors_corrected = []
    for i, original in enumerate(original_data):
        corrected = corrected_data[i][:len(original)]
        errors_fixed = sum(1 for j in range(min(len(original), len(corrected))) if corrected[j] != error_data[i][j])
        errors_corrected.append(errors_fixed)

    # Plot theoretical vs actual correction performance
    ax.plot(range(len(error_count)), error_count, label="Errors Introduced", marker='o')
    ax.plot(range(len(errors_corrected)), errors_corrected, label="Errors Corrected", marker='x')
    ax.set_title('Error Correction Performance')
    ax.set_xlabel('Test Index')
    ax.set_ylabel('Errors')
    ax.legend()
    ax.grid(True)

    # Display metrics on the right side of the subplot
    performance_text = (
        f"Errors Introduced: {sum(error_count)}\n"
        f"Errors Corrected: {sum(errors_corrected)}\n"
        f"Correction Rate: {sum(errors_corrected) / sum(error_count) * 100:.2f}%"
    )
    ax.text(1.05, 0.5, performance_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

def test_speed_and_efficiency(ax):
    original_data = [input_data[:12] for input_data in encoding_input]

    # Measure encoding and decoding time
    encoding_times = []
    decoding_times = []

    for data in original_data:
        start_time = time.time()
        encoded = BCH.BCHGenerator(data)
        encoding_time = time.time() - start_time
        encoding_times.append(encoding_time)

        # Measure decoding time (syndrome calculation)
        start_time = time.time()
        corrected = BCH.bch_syndrome_generator(encoded)
        decoding_time = time.time() - start_time
        decoding_times.append(decoding_time)

    # Plot the encoding/decoding times
    ax.plot(range(len(encoding_times)), encoding_times, label="Encoding Time", marker='o')
    ax.plot(range(len(decoding_times)), decoding_times, label="Decoding Time", marker='x')
    ax.set_title('Encoding/Decoding Speed')
    ax.set_xlabel('Test Index')
    ax.set_ylabel('Time (seconds)')
    ax.legend()
    ax.grid(True)

    # Display metrics on the right side of the subplot
    performance_text = (
        f"Avg Encoding Time: {sum(encoding_times) / len(encoding_times):.5f} s\n"
        f"Avg Decoding Time: {sum(decoding_times) / len(decoding_times):.5f} s\n"
        f"Total Processing Time: {sum(encoding_times) + sum(decoding_times):.5f} s"
    )
    ax.text(1.05, 0.5, performance_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

def test_resource_utilization(ax):
    original_data = [input_data[:12] for input_data in encoding_input]

    process = psutil.Process(os.getpid())
    memory_usage = []
    cpu_usage = []

    for data in original_data:
        # Measure memory and CPU usage during encoding
        initial_mem = process.memory_info().rss
        initial_cpu = process.cpu_percent(interval=None)

        encoded = BCH.BCHGenerator(data)

        mem_usage = process.memory_info().rss - initial_mem
        cpu_load = process.cpu_percent(interval=None) - initial_cpu

        memory_usage.append(mem_usage)
        cpu_usage.append(cpu_load)

    # Plot memory and CPU usage
    ax.plot(range(len(memory_usage)), memory_usage, label="Memory Usage (bytes)", marker='o')
    ax.plot(range(len(cpu_usage)), cpu_usage, label="CPU Usage (%)", marker='x')
    ax.set_title('Resource Utilization')
    ax.set_xlabel('Test Index')
    ax.set_ylabel('Usage')
    ax.legend()
    ax.grid(True)

   # Display metrics on the right side of the subplot
    performance_text = (
        f"Avg Memory Usage: {sum(memory_usage) / len(memory_usage):.2f} bytes\n"
        f"Avg CPU Usage: {sum(cpu_usage) / len(cpu_usage):.2f} %"
    )
    ax.text(1.05, 0.5, performance_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5))

# Create subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 10))  

# Call test functions
test_error_correction_performance(axs[0, 0])
test_speed_and_efficiency(axs[1, 0])
test_resource_utilization(axs[2, 0])

# Hide any unused subplots
for i in range(3):
    for j in range(1, 2):  # You only want to use the left column (axs[i, 0])
        fig.delaxes(axs[i, j])

# Final plot adjustments
plt.tight_layout()
plt.show()