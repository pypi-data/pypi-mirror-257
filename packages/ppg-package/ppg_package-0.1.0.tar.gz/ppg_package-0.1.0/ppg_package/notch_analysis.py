import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, argrelextrema

def find_dicrotic_notches(signal, distance=200):
    """
    在PPG信号中找到二尖瓣波值，并进行可视化。
    :param signal: PPG信号数组。
    :param distance: 寻找峰值和谷值时考虑的最小间隔。
    :return: 包含峰值、谷值和二尖瓣波值索引的元组。
    """
    # 找到所有的峰值和谷值
    peaks, _ = find_peaks(signal, distance=distance)
    troughs, _ = find_peaks(-signal, distance=distance)

    # 初始化二尖瓣波值列表
    dicrotic_notches = []

    # 遍历每个峰值，寻找它和下一个峰值之间的所有局部最小值点
    for i in range(len(peaks) - 1):
        if i + 1 < len(troughs):
            # 在当前峰值和下一个峰值之间找到所有的局部最小值点
            local_minima = argrelextrema(signal[peaks[i]:peaks[i+1]], np.less)[0] + peaks[i]
            local_minima = [index for index in local_minima if index not in troughs]

            # 初始化用于比较的二阶导数最大值
            max_second_derivative = -np.inf
            best_notch = None

            for local_minimum in local_minima:
                if local_minimum < len(signal) - 1:
                    amplitude_condition = True  # 可以添加振幅条件
                    second_derivative = signal[local_minimum + 1] - 2 * signal[local_minimum] + signal[local_minimum - 1]

                    if second_derivative > max_second_derivative and amplitude_condition:
                        max_second_derivative = second_derivative
                        best_notch = local_minimum

            if best_notch is not None:
                dicrotic_notches.append(best_notch)

    # 可视化
    plt.figure(figsize=(12, 6))
    plt.plot(signal, label='PPG Signal')
    plt.scatter(peaks, signal[peaks], color='green', marker='^', label='Peaks')
    plt.scatter(troughs, signal[troughs], color='orange', marker='v', label='Troughs')
    plt.scatter(dicrotic_notches, signal[dicrotic_notches], color='red', marker='x', label='Dicrotic Notches')
    plt.title('PPG Signal with Dicrotic Notches')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()
    plt.show()

    return peaks, troughs, dicrotic_notches
