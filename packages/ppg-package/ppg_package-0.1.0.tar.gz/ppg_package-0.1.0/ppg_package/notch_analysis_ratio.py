import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def find_dicrotic_notches_by_ratio(signal, ratio=0.7):
    peaks, _ = find_peaks(signal, distance=250)
    troughs, _ = find_peaks(-signal, distance=250)
    notches = []
    for i in range(len(troughs)-1):
        start_trough = troughs[i]
        end_trough = troughs[i+1]
        cycle_length = end_trough - start_trough
        expected_notch_position = start_trough + int(cycle_length * ratio)
        if expected_notch_position not in peaks:
            notches.append(expected_notch_position)

    # 可视化
    plt.figure(figsize=(10, 4))
    plt.plot(signal, label='PPG Segment')
    plt.scatter(peaks, signal[peaks], color='green', marker='^', label='Peaks')
    plt.scatter(troughs, signal[troughs], color='orange', marker='v', label='Troughs')
    plt.scatter(notches, signal[notches], color='red', marker='x', label='Dicrotic Notches')
    plt.title('PPG Signal with Dicrotic Notches')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return notches


