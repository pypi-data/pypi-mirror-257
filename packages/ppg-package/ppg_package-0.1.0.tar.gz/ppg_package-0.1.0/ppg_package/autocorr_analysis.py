from scipy.signal import correlate, find_peaks
import matplotlib.pyplot as plt

def analyze_autocorrelation(peak_to_trough_amplitudes):
    """
    对峰到谷幅度的自相关分析。
    :param peak_to_trough_amplitudes: 峰到谷的幅度数组。
    :return: 周期的真实值
    """
    auto_corr = correlate(peak_to_trough_amplitudes, peak_to_trough_amplitudes, mode='full')
    center = len(auto_corr) // 2
    auto_corr_peaks, _ = find_peaks(auto_corr[center:])

    if len(auto_corr_peaks) > 10:
        period = auto_corr_peaks[0]
    else:
        period = 0

    period_true = period * 0.57

    # 绘制自相关结果
    plt.figure(figsize=(12, 6))
    plt.plot(auto_corr[center:center + 2 * period] if period > 0 else auto_corr[center:])
    plt.title('Autocorrelation of Peak-to-Trough Amplitudes')
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.grid()
    plt.show()

    # 绘制原始数据
    plt.figure(figsize=(12, 6))
    plt.plot(peak_to_trough_amplitudes)
    plt.title('Peak-to-Trough Amplitudes Over Time')
    plt.xlabel('Data Point Index')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

    return period_true
