import numpy as np
import matplotlib.pyplot as plt

def calculate_rising_slope_area(signal, troughs, peaks):
    corrected_rising_slope_areas = []
    corrected_rising_slope_rectangles = []

    for i in range(len(troughs)):
        trough = troughs[i]
        next_peaks = [peak for peak in peaks if peak > trough]
        if not next_peaks:
            continue
        next_peak = next_peaks[0]
        
        horizontal_distance = next_peak - trough
        trough_level = signal[trough]
        area = np.trapz(signal[trough:next_peak] - trough_level, dx=1)
        corrected_rising_slope_areas.append(area)
        corrected_rising_slope_rectangles.append((trough, next_peak, trough_level, signal[next_peak]))

    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Segment')
    for rect in corrected_rising_slope_rectangles:
        plt.fill_between(x=range(rect[0], rect[1]), y1=signal[rect[0]:rect[1]], y2=rect[2], color='lightgray', alpha=0.3)
    plt.scatter(peaks, signal[peaks], color='green', marker='^', label='Peaks')
    plt.scatter(troughs, signal[troughs], color='orange', marker='v', label='Troughs')
    plt.title('PPG Segment with Corrected Rising Slope Areas')
    plt.xlabel('Sample Index')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return corrected_rising_slope_areas


