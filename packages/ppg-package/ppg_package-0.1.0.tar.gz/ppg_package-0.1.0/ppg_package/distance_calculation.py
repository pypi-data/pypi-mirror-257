import numpy as np
import matplotlib.pyplot as plt

def calculate_distances_and_plot(signal, troughs, peaks, notches, sampling_rate):
    def calculate_vertical_horizontal_distances(signal, troughs, peaks):
        vertical_distances = []
        horizontal_times = []

        for trough in troughs:
            next_peaks = [peak for peak in peaks if peak > trough]
            if not next_peaks:
                continue
            next_peak = next_peaks[0]

            vertical_distance = signal[next_peak] - signal[trough]
            horizontal_distance = next_peak - trough
            time_duration = horizontal_distance / sampling_rate

            vertical_distances.append(vertical_distance)
            horizontal_times.append(time_duration)

        return vertical_distances, horizontal_times

    def calculate_dicrotic_notch_distances(signal, troughs, notches):
        dicrotic_notch_amplitudes = []
        horizontal_time_differences = []

        for notch in notches:
            next_troughs = [trough for trough in troughs if trough > notch]
            if not next_troughs:
                continue
            next_trough = next_troughs[0]

            dicrotic_notch_amplitude = signal[notch]
            horizontal_distance = next_trough - notch
            time_difference = horizontal_distance / sampling_rate

            dicrotic_notch_amplitudes.append(dicrotic_notch_amplitude)
            horizontal_time_differences.append(time_difference)

        return dicrotic_notch_amplitudes, horizontal_time_differences

    vertical_distances, horizontal_times = calculate_vertical_horizontal_distances(signal, troughs, peaks)
    dicrotic_notch_amplitudes, horizontal_time_differences = calculate_dicrotic_notch_distances(signal, troughs, notches)

    # 绘制PPG波形和标注距离
    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Segment')
    plt.scatter(peaks, signal[peaks], color='green', marker='^', label='Peaks')
    plt.scatter(troughs, signal[troughs], color='orange', marker='v', label='Troughs')
    plt.scatter(notches, signal[notches], color='red', marker='x', label='Dicrotic Notches')
    for i, trough in enumerate(troughs):
        if i < len(peaks) and i < len(vertical_distances):
            peak = peaks[i]
            plt.annotate(f"{vertical_distances[i]:.2f}", (peak, signal[peak]), xytext=(0,10), textcoords='offset points', ha='center')
            plt.annotate(f"{horizontal_times[i]:.2f}s", ((trough+peak)/2, signal[trough]), xytext=(0,-15), textcoords='offset points', ha='center')
            plt.axvline(x=trough, color='grey', linestyle='--', alpha=0.5)
            plt.axvline(x=peak, color='grey', linestyle='--', alpha=0.5)
    plt.title('PPG Segment with Vertical and Horizontal Distances')
    plt.xlabel('Sample Index')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return vertical_distances, horizontal_times, dicrotic_notch_amplitudes, horizontal_time_differences


