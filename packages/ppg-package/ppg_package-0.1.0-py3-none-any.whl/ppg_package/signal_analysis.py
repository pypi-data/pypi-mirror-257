import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import welch, stft
import pywt

def process_and_plot_ppg_signal(ppg_filtered, sampling_rate=500):
    def fft_analysis(signal):
        N = len(signal)
        T = 1.0 / sampling_rate
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal)
        plt.figure(figsize=(12, 6))
        plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
        plt.title("FFT of PPG Signal")
        plt.xlim(0, 15) 
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()

    def psd_analysis(signal):
        f, Pxx_den = welch(signal, fs=sampling_rate, nperseg=1024)
        plt.figure(figsize=(12, 6))
        plt.semilogy(f, Pxx_den)
        plt.title("PSD of PPG Signal")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("PSD")
        plt.grid(True)
        plt.show()

    def stft_analysis(signal):
        f, t, Zxx = stft(signal, fs=sampling_rate, nperseg=256)
        plt.figure(figsize=(12, 6))
        plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
        plt.title("STFT of PPG Signal")
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (sec)")
        plt.ylim(0, 10)
        plt.show()

    def cwt_analysis(signal):
        scales = np.arange(1, 128)
        wavelet = 'morl'
        coefficients, frequencies = pywt.cwt(signal, scales, wavelet, 1.0 / sampling_rate)
        plt.figure(figsize=(10, 6))
        plt.imshow(abs(coefficients), extent=[0, len(signal)/sampling_rate, 1, 128], cmap='jet', aspect='auto', vmax=abs(coefficients).max(), vmin=-abs(coefficients).max())
        plt.title('Continuous Wavelet Transform (CWT) of PPG Signal')
        plt.ylabel('Scale')
        plt.xlabel('Time (sec)')
        plt.show()

    def poincare_plot(signal):
        x = signal[:-1]
        y = signal[1:]
        plt.figure(figsize=(6, 6))
        plt.scatter(x, y, color='blue')
        plt.title('Poincaré Plot')
        plt.xlabel('PPG(n)')
        plt.ylabel('PPG(n+1)')
        plt.grid(True)
        plt.show()

    # 运行各个分析函数
    fft_analysis(ppg_filtered)
    psd_analysis(ppg_filtered)
    stft_analysis(ppg_filtered)
    cwt_analysis(ppg_filtered)
    poincare_plot(ppg_filtered)

# 示例数据用于测试函数
sampling_rate = 500
t = np.linspace(0, 10, 5000)
ppg_filtered = np.sin(2 * np.pi * 1.2 * t) + 0.5 * np.sin(2 * np.pi * 2.4 * t)

# 调用函数
process_and_plot_ppg_signal(ppg_filtered, sampling_rate)
