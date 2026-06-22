# utils.py
import os

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from IPython.display import display
from IPython.display import Audio
from IPython.display import HTML


# Spectrogram parameters
FS           = 44100      # Hz
NFFT         = 4096       # fft window size [samples]
NOVERLAP     = 4096-256   # fft window overlap [samples]
VMIN         = -100       # minimum depth [dB]
VMAX         = -50        # maximum depth [dB]
YMAX         = 8000       # max frequency [Hz]

def plot_spectrogram(audio, Fs=FS, vmin=VMIN, vmax=VMAX, title='', fn=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.specgram(audio, Fs=Fs, NFFT=NFFT, noverlap=NOVERLAP, vmin=vmin, vmax=vmax)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title(title)
    fig.colorbar(ax.images[-1], ax=ax, label='dB')
    ax.set_ylim(0, YMAX)
    if fn:
        fig.savefig(fn, dpi=150, bbox_inches='tight')
    display(fig)
    plt.close(fig)
    return None

def plot_spectrogram_channels(audio, Fs=FS, vmin=VMIN, vmax=VMAX, title='', fn=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(title)
    
    ax1.specgram(audio[:,0], Fs=Fs, NFFT=NFFT, noverlap=NOVERLAP, vmin=vmin, vmax=vmax)
    ax1.set_title('Channel 0')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_ylim(0, YMAX)
    
    ax2.specgram(audio[:,1], Fs=Fs, NFFT=NFFT, noverlap=NOVERLAP, vmin=vmin, vmax=vmax)
    ax2.set_title('Channel 1')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(0, YMAX)
    fig.colorbar(ax2.images[-1], ax=[ax1, ax2], label='dB', fraction=0.046, pad=0.04)
    if fn:
        fig.savefig(fn, dpi=150, bbox_inches='tight')
    display(fig)
    plt.close(fig)
    return None