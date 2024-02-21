import numpy as np
from scipy.signal import butter, filtfilt, freqz
import matplotlib.pyplot as plt

def process_ppg_signal(ppg_data, lowcut=1, highcut=15, fs=500, order=3):
    """
    对PPG信号进行滤波和频谱分析。
    :param ppg_data: 输入的PPG信号数据。
    :param lowcut: 低通滤波器截止频率。
    :param highcut: 高通滤波器截止频率。
    :param fs: 采样率。
    :param order: 滤波器的阶数。
    :return: None
    """
    def butter_bandpass(lowcut, highcut, fs, order=3):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        y = filtfilt(b, a, data)
        return y

    filtered_ppg = butter_bandpass_filter(ppg_data, lowcut, highcut, fs, order)

    # 频谱分析
    ppg_spectrum = np.fft.rfft(filtered_ppg)
    frequencies = np.fft.rfftfreq(len(filtered_ppg), 1/fs)
    magnitude = np.abs(ppg_spectrum)

    # 绘制频谱图
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, magnitude)
    plt.title('PPG Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, 15)
    plt.grid(True)
    plt.show()

    # 分段绘制滤波后的PPG图像
    fig, axs = plt.subplots(6, 1, figsize=(10, 20))
    points_per_segment = len(ppg_data) // 6

    for i in range(6):
        start_index = i * points_per_segment
        end_index = start_index + points_per_segment
        axs[i].plot(filtered_ppg[start_index:end_index])
        axs[i].set_title(f'Filtered PPG Segment {i+1}')
        axs[i].set_xlabel('Sample Number')
        axs[i].set_ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

    return filtered_ppg
