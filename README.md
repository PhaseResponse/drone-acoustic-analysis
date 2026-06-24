# drone-acoustic-analysis

An acoustic simulation of a 3-blade or 4-blade quadcopter drone is created for a two-microphone observer. 
Signal generation and acoustic propagation concepts are adapted from [1].

## Signal Characteristics

Signal characteristics are calibrated against live drone outdoor recordings.

1. Blade passing frequency (BPF) harmonics (N<sub>b</sub>·f<sub>0</sub>, 2·N<sub>b</sub>·f<sub>0</sub>, ...) are dominant.
   Non-BPF harmonics are suppressed with exponential decay.
2. The four motors are given slight RPM variation to create realistic beating.
3. The phase per motor is given a uniformly random jitter.
4. 1/f² broadband noise is added for motor and aerodynamic noise.

The following is a spectrogram of the drone signal before propagation through the acoustic setup.

<img src="images/spectrogram_raw_3blade.png" width="49%">

## Acoustic Setup

1. Two microphones are positioned 30 cm apart on the x-axis, facing forward (facing the y-axis).
2. Ground reflection is simulated by a mirrored source trajectory below ground (-z), scaled by the reflection coefficient.
3. Wind-induced turbulence noise is simulated by independent 1/f² noise added to each microphone's propagated signal.
4. Three scenarios are simulated.  

a. "flyby": a drone flies laterally parallel to the observer at a constant height.

<p>
  <img src="images/spectrogram_flyby_z20.png" width="49%">
  <img src="images/spectrogram_flyby_z20_brown_rms0.50.png" width="49%">
</p>

b. "approach": a drone approaches the observer orthogonally at a constant height.  
Flight altitude affects the steepness of the Doppler sweep. 

Altitude = 20 m
<p>
  <img src="images/spectrogram_approach_z20.png" width="49%">
  <img src="images/spectrogram_approach_z20_brown_rms0.50.png" width="49%">
</p>

Altitude = 5 m
<p>
  <img src="images/spectrogram_approach_z5.png" width="49%">
  <img src="images/spectrogram_approach_z5_brown_rms0.50.png" width="49%">
</p>

c. "dive": a drone approaches the observer orthogonally and dives to the ground at the observer's location. 

<p>
  <img src="images/spectrogram_dive_z20.png" width="49%">
  <img src="images/spectrogram_dive_z20_brown_rms0.50.png" width="49%">
</p>

<!--  
To view an interactive version with playable audio, open the notebooks on nbviewer:
- [Drone sound simulation](https://nbviewer.org/github/PhaseResponse/drone-acoustic-analysis/blob/main/drone_sound_simulation.ipynb)
- [Microphone turbulence](https://nbviewer.org/github/PhaseResponse/drone-acoustic-analysis/blob/main/mic_turbulence.ipynb)
-->

## Upcoming features

1. Classical detection (drone/no-drone) for edge deployment.
   - private dataset includes: drones, wind noise, voice, birds, dogs.
2. Microphone modeling.
   - Obtain edge microphone recordings w/ and w/o foam windscreen.
   - Tune microphone wind noise model with recordings.
3. Trajectory modeling.
   - Model drone stabilization motion pattern from recordings.
4. ML-based classification (flyby/approach/dive).
   - Augmentation: microphone wind noise, drone physical and trajectory parameters, additional noise sources.

## References
[1] Herold G. Drone auralization example. Acoular Blog. 2024 Sep 21. https://blog.acoular.org/posts/auralization/drone-auralization-example.html

