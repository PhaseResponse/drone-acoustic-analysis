"""
audio batch processing utils
"""
from scipy.io import wavfile
from scipy.signal import spectrogram as sg
import numpy as np
import os
from sklearn.metrics import precision_recall_curve, f1_score
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# --- spectrogram params  ---
N_FFT     = 1024
HOP       = 512
F_MAX     = 8000
DURATION  = 1.0   # seconds per segment
SR        = 16000
# --- segment params  ---
N_FRAMES          = 16                  # frames per segment
N_SEGMENT_OVERLAP = 8                   # frames overlapping previous segment, for EMA initial conditions
SEG_SAMPLES       = N_FFT * N_FRAMES    # number of samples per segment

# --- segment wav file ---
def segment_wav(wav_path, label, seg_samples=SEG_SAMPLES, sr=SR, n_overlap=N_SEGMENT_OVERLAP):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fs, audio = wavfile.read(wav_path)
    if audio.ndim > 1:
        audio = audio[:, 0]
    if audio.dtype == np.int32:
        audio = audio.astype(np.float32) / 2147483648.0
    elif audio.dtype == np.int16:
        audio = audio.astype(np.float32) / 32768.0
    if fs != sr:
        from scipy.signal import resample_poly
        from math import gcd
        g = gcd(sr, fs)
        audio = resample_poly(audio, sr // g, fs // g)
    overlap_samples = n_overlap * HOP
    total_samples = seg_samples + overlap_samples
    segments = []
    for start in range(0, len(audio) - total_samples + 1, seg_samples):
        seg = audio[start:start + total_samples]
        segments.append((seg, label))
    return segments

def save_segments_as_wav(segments, out_dir, sr=SR):
    os.makedirs(out_dir, exist_ok=True)
    for i, (audio, label) in enumerate(segments):
        fname = f"seg_{i:05d}_label{label}.wav"
        path = os.path.join(out_dir, fname)
        audio_int16 = (audio * 32768).clip(-32768, 32767).astype(np.int16)
        wavfile.write(path, sr, audio_int16)

def load_segments_from_wav(out_dir, sr=SR):
    segments = []
    for fname in sorted(os.listdir(out_dir)):
        if not fname.endswith(".wav"):
            continue
        label = int(fname.split("_label")[1].replace(".wav", ""))
        _, audio = wavfile.read(os.path.join(out_dir, fname))
        audio = audio.astype(np.float32) / 32768.0
        segments.append((audio, label))
    return segments


def scores_from_segments(segments, score_fn, fs=None):
    """Run on all segments, return scores and labels."""
    scores = []
    labels = []
    for audio, label in segments:
        score = score_fn(audio, fs) if fs else score_fn(audio)
        scores.append(score)
        labels.append(label)
    return np.array(scores), np.array(labels)

def plot_pr_curve(scores, labels, title=None, threshold_label=None, op_threshold=None):    
    precision, recall, thresholds = precision_recall_curve(labels, scores)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)
    best_idx = np.argmax(f1)
    best_f1 = f1[best_idx]
    best_thresh = thresholds[best_idx] if best_idx < len(thresholds) else 1.0
    fig, ax = plt.subplots(figsize=(7, 5))
    precision_smooth = savgol_filter(precision, window_length=51, polyorder=2)
    ax.plot(recall, precision_smooth, color='steelblue', linewidth=1.5)
    conf_on_idx = np.argmin(np.abs(thresholds - op_threshold))
    ax.scatter(recall[conf_on_idx], precision[conf_on_idx], 
               color='green', zorder=5,
               label=f'{threshold_label}={op_threshold}   f1-score={f1[conf_on_idx]:.2f}')    
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig
