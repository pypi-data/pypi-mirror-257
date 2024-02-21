import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def analyze_breathing(ppg_breathing, sampling_rate, points_per_segment):
    """
    分析PPG信号的呼吸周期并进行可视化。
    :param ppg_breathing: 经过滤波的PPG信号。
    :param sampling_rate: 采样率。
    :param points_per_segment: 每个子图的样本数。
    :return: 分析结果字典
    """
    min_distance_between_peaks = int(sampling_rate * 2)

    peaks_breathing, _ = find_peaks(ppg_breathing, distance=min_distance_between_peaks)
    troughs_breathing, _ = find_peaks(-ppg_breathing, distance=min_distance_between_peaks)
    breathing_intervals = np.diff(peaks_breathing)
    average_breathing_interval = np.mean(breathing_intervals) / sampling_rate
    breathing_periods = np.diff(peaks_breathing) / sampling_rate  
    breathing_period_variability = np.std(breathing_periods) / np.mean(breathing_periods)

    # 可视化呼吸信号和峰谷
    fig, axs = plt.subplots(6, 1, figsize=(12, 18))
    for i in range(6):
        start_index = i * points_per_segment
        end_index = start_index + points_per_segment
        segment_breathing = ppg_breathing[start_index:end_index]
        segment_peaks = [peak - start_index for peak in peaks_breathing if start_index <= peak < end_index]
        segment_troughs = [trough - start_index for trough in troughs_breathing if start_index <= trough < end_index]
        axs[i].plot(segment_breathing, label='Breathing Signal')
        axs[i].plot(segment_peaks, segment_breathing[segment_peaks], 'x', label='Peaks')
        axs[i].plot(segment_troughs, segment_breathing[segment_troughs], 'o', label='Troughs')
        axs[i].set_title(f'PPG Breathing Segment {i+1}')
        axs[i].legend()
    plt.tight_layout()
    plt.show()

    return {
        "average_breathing_interval": average_breathing_interval,
        "breathing_period_variability": breathing_period_variability,
        "breathing_periods": breathing_periods,
        "breathing_intervals": breathing_intervals
    }
