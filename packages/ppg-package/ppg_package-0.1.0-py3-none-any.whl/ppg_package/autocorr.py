import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def analyze_ppg_autocorr(ppg_filtered, distance=250):
    """
    分析PPG信号的自相关，并评估波形质量。
    :param ppg_filtered: 经过滤波的PPG信号。
    :param distance: find_peaks的distance参数。
    :return: (ppg_filtered_new, quality_peak)
    """
    # 计算自相关
    autocorr = np.correlate(ppg_filtered, ppg_filtered, mode='full')
    autocorr = autocorr[autocorr.size // 2:]

    # 寻找峰值
    peaks, _ = find_peaks(autocorr, distance=distance)
    if len(peaks) > 1:
        quality_peak = peaks[1]
        ppg_filtered_new = ppg_filtered[quality_peak:]
    else:
        print("未找到合适的峰值，保留原始数据。")
        ppg_filtered_new = ppg_filtered
        quality_peak = 0

    # 可视化自相关图
    plt.figure(figsize=(10, 4))
    plt.plot(autocorr)
    plt.title('PPG Self Correlation')
    plt.xlabel('Lag')
    plt.ylabel('Correlation')
    plt.show()

    # 可视化PPG信号
    subplots = 6
    samples_per_subplot = len(ppg_filtered) // subplots

    fig, axes = plt.subplots(subplots, 1, figsize=(10, 12))
    for i in range(subplots):
        start_index = i * samples_per_subplot
        end_index = start_index + samples_per_subplot
        axes[i].plot(ppg_filtered[start_index:end_index])
        axes[i].set_title(f'PPG Segment {i+1}')
        axes[i].set_xlabel('Sample Number')
        axes[i].set_ylabel('Amplitude')
    plt.tight_layout()
    plt.show()

    return ppg_filtered_new, quality_peak
