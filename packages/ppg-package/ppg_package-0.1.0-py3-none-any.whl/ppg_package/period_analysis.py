import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def analyze_ppg_period(ppg_filtered, sampling_rate, points_per_segment):
    """
    分析PPG信号的周期并进行可视化。
    :param ppg_filtered: 经过滤波的PPG信号。
    :param sampling_rate: 采样率。
    :param points_per_segment: 每个子图的样本数。
    :return: 分析结果字典
    """
    min_distance_between_peaks = int(sampling_rate * 0.35)

    peaks_filtered, _ = find_peaks(ppg_filtered, distance=min_distance_between_peaks)
    troughs_filtered, _ = find_peaks(-ppg_filtered, distance=min_distance_between_peaks)
    filtered_intervals = np.diff(peaks_filtered)
    average_filtered_interval = np.mean(filtered_intervals) / sampling_rate
    filtered_periods = np.diff(peaks_filtered) / sampling_rate  
    filtered_period_variability = np.std(filtered_periods) / np.mean(filtered_periods)

    # 可视化PPG周期信号
    fig, axs = plt.subplots(6, 1, figsize=(12, 18))
    for i in range(6):
        start_index = i * points_per_segment
        end_index = start_index + points_per_segment
        segment_filtered = ppg_filtered[start_index:end_index]
        segment_peaks = [peak - start_index for peak in peaks_filtered if start_index <= peak < end_index]
        segment_troughs = [trough - start_index for trough in troughs_filtered if start_index <= trough < end_index]
        axs[i].plot(segment_filtered, label='Filtered Signal')
        axs[i].plot(segment_peaks, segment_filtered[segment_peaks], 'x', label='Peaks')
        axs[i].plot(segment_troughs, segment_filtered[segment_troughs], 'o', label='Troughs')
        axs[i].set_title(f'PPG Filtered Segment {i+1}')
        axs[i].legend()
    plt.tight_layout()
    plt.show()

    return {
        "average_filtered_interval": average_filtered_interval,
        "filtered_period_variability": filtered_period_variability,
        "filtered_periods": filtered_periods,
        "filtered_intervals": filtered_intervals
    }
