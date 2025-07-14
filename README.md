
# 🎧 Spatial Audio Head-Tracking with Hand Gesture Volume Control

A real-time spatial audio processor that uses your webcam to:
- 🔄 **Pan audio** based on your head position  
- 🎚️ **Adjust master volume** using hand gestures  
- 🎛️ Adds simple reverb and distance-based attenuation  

Built with **Python, Mediapipe, OpenCV, and SoundDevice**.

---

## 📸 Features  

✅ Head rotation left/right → audio panning  
✅ Head distance from camera → volume attenuation  
✅ Index fingertip height → volume control  
✅ Simple reverb (delay buffer)  
✅ Cross-platform: **macOS + Windows**  

---

## 📦 Dependencies  

Install via pip:

```
pip install mediapipe opencv-python sounddevice numpy
```

You also need a **virtual audio loopback device**:

| OS       | Virtual Device                |
|:----------|:--------------------------------|
| **macOS** | [BlackHole (2ch)](https://existential.audio/blackhole/) |
| **Windows** | [VB-Cable](https://vb-audio.com/Cable/) |

---

## 🎛️ macOS Setup  

1. Install BlackHole (via Homebrew or installer)
   ```
   brew install blackhole-2ch
   ```

2. Open **Audio MIDI Setup**
   - Create a **Multi-Output Device**
   - Add `BlackHole 2ch` and `External Headphones`
   - Enable **Drift Correction** on everything except your main output  

3. Set **System Output** to this Multi-Output Device  
4. In the Python code, identify device indices:
   ```
   python check_devices.py
   ```

---

## 🖥️ Windows Setup  

1. Install **VB-Cable**  
2. Set **VB-Cable Input** as default system output  
3. Set **headphones/speakers** as playback device in your app  
4. Identify device indices:
   ```
   python check_devices.py
   ```

---

## 🚀 Run It  

```
python main.py
```

Controls:
- **Move head left/right** → pans audio  
- **Move head closer/farther** → changes volume/distance attenuation  
- **Raise or lower index finger** → controls master volume  

Press `q` to quit.

---

## ⚙️ Device Indices  

Find your audio device indices by running:

```
python check_devices.py
```

Example output:
```
0 BlackHole 2ch
1 External Headphones
...
```

Then set them here in `main.py`:

```python
blackhole_input_device = 0
headphones_output_device = 1
```

---

## 📖 License  

MIT License.  
Feel free to modify, improve, and distribute.

---

## 💡 Credits  

Built by Mehar Khanna  
with ❤️, Python, and way too much curiosity.
