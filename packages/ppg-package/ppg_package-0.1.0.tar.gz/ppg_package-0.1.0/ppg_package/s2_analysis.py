import numpy as np
import matplotlib.pyplot as plt

def calculate_s2_and_plot(signal, troughs, notches, cycle_rectangles):
    s2_areas = []
    s2_rectangles = []

    for rect in cycle_rectangles:
        cycle_start, cycle_end, _, _ = rect
        notches_in_cycle = [notch for notch in notches if cycle_start <= notch <= cycle_end]
        if not notches_in_cycle:
            continue
        notch = notches_in_cycle[0]
        troughs_in_cycle = [trough for trough in troughs if cycle_start <= trough <= cycle_end]
        if not troughs_in_cycle:
            continue
        farthest_trough = max(troughs_in_cycle, key=lambda trough: abs(trough - notch))
        start = min(notch, farthest_trough)
        end = max(notch, farthest_trough)
        trough_level = signal[farthest_trough]
        area = np.trapz(signal[start:end] - trough_level, dx=1)
        s2_areas.append(area)
        s2_rectangles.append((start, end, trough_level, signal[notch]))

    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Segment')
    for rect in s2_rectangles:
        plt.fill_between(x=range(rect[0], rect[1]), y1=signal[rect[0]:rect[1]], y2=rect[2], color='lightgreen', alpha=0.3)
    plt.title('PPG Segment with S2 Areas')
    plt.xlabel('Sample Index')
    plt.ylabel('PPG Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return s2_areas
