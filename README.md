## Spatial Audio Studio: Free AirPods Replacement

Too broke for $400 AirPods? So was I.  
So I turned my regular wired headphones into a full-on head-tracked spatial audio system using a webcam, Python, and a refusal to overpay for sound tricks.

Turn your head and the audio pans.  
Lean back and it fades out with natural reverb.  
Raise your hand in the air and the volume adjusts.  
It works in real time, no delay, and runs on any standard computer setup.

No custom hardware. No proprietary drivers. Just software doing its job.

---

## What It Does

- Tracks your face through your webcam  
- Moves sound left and right based on head rotation  
- Adds reverb and volume fade when you move away from the camera  
- Adjusts volume by tracking hand height  
- Works on both macOS and Windows  
- Uses Python, Mediapipe, OpenCV, and SoundDevice  

---

## How It Feels

Turn your head to the left and the sound slides to the right ear.  
Turn to the right and it shifts left.  
Lean back and it softens with subtle reverb like you're walking away from the speaker.  
Raise your hand and the volume increases. Lower it and it fades.  
It feels like the sound exists outside your headphones, anchored in space.

---

## Install

Make sure Python is installed. Then run:

```bash
pip install mediapipe opencv-python sounddevice numpy
```

You’ll also need a virtual audio loopback device:

| OS      | Tool                                  |
|---------|----------------------------------------|
| macOS   | [BlackHole (2ch)](https://existential.audio/blackhole/)  
| Windows | [VB-Cable](https://vb-audio.com/Cable/)  

---

## macOS Setup

1. Install BlackHole:
   ```bash
   brew install blackhole-2ch
   ```

2. Open Audio MIDI Setup  
   - Create a Multi-Output Device  
   - Add BlackHole and your headphones  
   - Enable Drift Correction for all devices except your main output  

3. Set your system output to the new Multi-Output Device  
4. Run the following to find your audio device indexes:
   ```bash
   python check.py
   ```

---

## Windows Setup

1. Install VB-Cable  
2. Set VB-Cable Input as your system’s default output  
3. In the app you’re testing (browser, media player, etc.), choose your headphones as the playback device  
4. Run:
   ```bash
   python check.py
   ```

---

## Run the System

Once everything is set up, start the program:

```bash
python main.py
```

Controls:  
- Turn your head left or right to pan the sound  
- Move forward or back to adjust volume and reverb  
- Raise or lower your hand to control the volume in real time  
- Press `q` to quit  

---

## Device Indexes

Use the following command to get your audio device list:

```bash
python check.py
```

Example:

```
0 BlackHole 2ch  
1 External Headphones
```

Update `main.py` with your actual device IDs:

```python
blackhole_input_device = 0  
headphones_output_device = 1
```

---

## How It Works

- Mediapipe tracks your head and hand using Face Mesh and Hand Landmarks  
- OpenCV captures video frames from the webcam  
- SoundDevice plays custom-generated stereo audio with real-time control  
- Volume and panning are computed based on face position and hand height  
- A basic delay buffer creates the reverb effect based on your distance from the camera

No external training, no large models, no GPU requirements. Just efficient, real-time computation that responds as fast as you move.

---

## License

MIT License  
You can use, modify, share, or even build your own version on top of this.

---

## Author

Built by Mehar Khanna  
Just someone who figured if Apple could do it with silicon and sensors, I could do it with Python and a webcam.
