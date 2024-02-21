import matplotlib.pyplot as plt
import pandas as pd

def plot_ppg_segments(file_path, cycles_per_segment=20, total_cycles=6, sampling_rate=500):
    try:
        data = pd.read_csv(file_path, sep='\t', header=None, usecols=[0], skiprows=2)
        original_ppg = data[0].tolist()
        points_per_cycle = sampling_rate

        segments = [original_ppg[i * points_per_cycle * cycles_per_segment:(i + 1) * points_per_cycle * cycles_per_segment] for i in range(total_cycles)]

        fig, axs = plt.subplots(total_cycles, 1, figsize=(10, 20))
        for i, segment in enumerate(segments):
            axs[i].plot(segment)
            axs[i].set_title(f'PPG data {i+1} with {cycles_per_segment} Cycles')
            axs[i].set_xlabel('Sample Number')
            axs[i].set_ylabel('PPG Amplitude')

        plt.tight_layout()
        plt.show()

        return True
    except Exception as e:
        print("Error in plotting PPG segments:", str(e))
        return False
