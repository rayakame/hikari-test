import numpy as np
import base64
from pydub import AudioSegment


def calculate_waveform(audio_file_path: str) -> tuple[str, float]:

    audio = AudioSegment.from_file(audio_file_path)
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)


    samples /= np.iinfo(audio.array_type).max

    # Determine number of bins
    duration = len(audio) / 1000.0
    num_bins = np.clip(int(duration * 10), min(32, len(samples)), 256)
    samples_per_bin = len(samples) // num_bins

    # Compute root-mean-square for each bin
    bins = np.zeros(num_bins, dtype=np.uint8)
    for i in range(num_bins):
        start = i * samples_per_bin
        end = start + samples_per_bin
        rms = np.sqrt(np.mean(np.square(samples[start:end])))
        bins[i] = int(rms * 255)

    # Normalize bins
    max_bin = np.max(bins)
    if max_bin > 0:
        ratio = 1 + (255 / max_bin - 1) * min(1, 100 * (max_bin / 255) ** 3)
        bins = np.minimum(255, (bins * ratio).astype(np.uint8))

    waveform_encoded = base64.b64encode(bins.tobytes()).decode('utf-8')

    return waveform_encoded, duration

