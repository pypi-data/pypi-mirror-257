import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def calculate_ppg_areas(signal, peaks, troughs):
    def calculate_s1(signal, peaks, troughs):
        s1_areas = []
        cycle_rectangles = []

        for i in range(len(troughs) - 1):
            cycle_start = troughs[i]
            cycle_end = troughs[i + 1]
            peaks_in_cycle = [peak for peak in peaks if cycle_start <= peak < cycle_end]

            if peaks_in_cycle:
                max_peak = max(peaks_in_cycle, key=lambda peak: signal[peak])
                amplitude = signal[max_peak] - signal[cycle_start]
                area = (cycle_end - cycle_start) * amplitude
                s1_areas.append(area)
                cycle_rectangles.append((cycle_start, cycle_end, signal[cycle_start], signal[max_peak]))

        return s1_areas, cycle_rectangles

    def calculate_area_under_curve(signal, cycle_rectangles):
        areas_under_curve = []

        for rect in cycle_rectangles:
            cycle_start, cycle_end, baseline, _ = rect
            area_under_curve = np.trapz(signal[cycle_start:cycle_end] - baseline, dx=1)
            areas_under_curve.append(area_under_curve)

        return areas_under_curve

    s1_areas, cycle_rectangles = calculate_s1(signal, peaks, troughs)
    areas_under_curve = calculate_area_under_curve(signal, cycle_rectangles)

    # 绘制PPG波形和周期矩形
    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Segment')
    for rect in cycle_rectangles:
        plt.fill_betweenx(y=[rect[2], rect[3]], x1=rect[0], x2=rect[1], color='grey', alpha=0.2)
    plt.title('PPG Segment with Filled Rectangles Covering Each Cycle')
    plt.xlabel('Sample Index')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 绘制PPG波形和线下面积
    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Segment')
    for rect in cycle_rectangles:
        cycle_start, cycle_end, baseline, _ = rect
        plt.fill_between(x=range(cycle_start, cycle_end), y1=signal[cycle_start:cycle_end], y2=baseline, color='blue', alpha=0.2)
    plt.title('PPG Segment with Areas Under Curve Filled')
    plt.xlabel('Sample Index')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return s1_areas, areas_under_curve
