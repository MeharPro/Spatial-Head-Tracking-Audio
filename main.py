import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd

# Audio settings
BLOCKSIZE = 1024
SAMPLERATE = 44100
CHANNELS = 2

# Device indices from query_devices()
blackhole_input_device = 0
headphones_output_device = 1

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(1)

# Shared panning, distance values, and master volume
pan = 0.0
distance_factor = 1.0
master_volume = 0.8

# Reverb buffer (simple delay line)
reverb_buffer = np.zeros((BLOCKSIZE * 2, 2))
reverb_index = 0
REVERB_DECAY = 0.35

# Audio callback
def audio_callback(indata, outdata, frames, time, status):
    global pan, distance_factor, reverb_buffer, reverb_index, master_volume
    if status:
        print(status)

    left = indata[:, 0] * (1 - pan)
    right = indata[:, 1] * (1 + pan)
    stereo = np.column_stack((left, right))
    stereo *= distance_factor

    for i in range(len(stereo)):
        delayed = reverb_buffer[reverb_index]
        stereo[i] += delayed * REVERB_DECAY
        reverb_buffer[reverb_index] = stereo[i]
        reverb_index = (reverb_index + 1) % len(reverb_buffer)

    stereo *= master_volume
    outdata[:] = stereo

# Start audio stream
stream = sd.Stream(
    samplerate=SAMPLERATE,
    blocksize=BLOCKSIZE,
    device=(blackhole_input_device, headphones_output_device),
    channels=CHANNELS,
    callback=audio_callback
)
stream.start()

# Head and hand tracking loop
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_result = face_mesh.process(frame_rgb)
    hand_result = hands.process(frame_rgb)

    if face_result.multi_face_landmarks:
        landmarks = face_result.multi_face_landmarks[0]
        left_ear = landmarks.landmark[234]
        right_ear = landmarks.landmark[454]

        dx = right_ear.x - left_ear.x
        dy = right_ear.y - left_ear.y
        yaw = np.arctan2(dy, dx) * (180.0 / np.pi)

        alpha = 0.15
        pan = alpha * np.clip(yaw / 30.0, -0.8, 0.8) + (1 - alpha) * pan

        ear_distance = np.sqrt(dx**2 + dy**2)
        distance_factor = np.clip((ear_distance - 0.05) * 8.0, 0.4, 1.0)

    if hand_result.multi_hand_landmarks:
        hand_landmarks = hand_result.multi_hand_landmarks[0]
        index_finger_tip = hand_landmarks.landmark[8]  # index fingertip

        # Map Y-position to volume: lower Y (hand up) = higher volume
        hand_y = index_finger_tip.y
        volume_alpha = 0.2
        new_volume = np.clip(1.2 - hand_y * 2, 0.2, 1.0)
        master_volume = volume_alpha * new_volume + (1 - volume_alpha) * master_volume

        # Draw hand landmarks
        mp.solutions.drawing_utils.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Head & Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
stream.stop()
stream.close()
