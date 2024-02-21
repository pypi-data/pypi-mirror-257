import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def extract_breathing_component(ppg_data, lowcut=0.5, fs=500, order=5):
    """
    对PPG数据进行低通滤波以提取呼吸成分。
    :param ppg_data: 输入的PPG信号数据。
    :param lowcut: 低通滤波器截止频率。
    :param fs: 采样率。
    :param order: 滤波器的阶数。
    :return: None
    """
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data)
        return y

    ppg_breathing = butter_lowpass_filter(ppg_data, lowcut, fs, order)

    # 绘制滤波后的PPG呼吸成分图像
    plt.figure(figsize=(10, 6))
    plt.plot(ppg_breathing)
    plt.title('PPG Breathing Component (0-0.5 Hz)')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
    plt.show()

    return ppg_breathing
