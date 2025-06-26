# SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-CONVERSION-USING-HAND-LAND-MARKS
A real-time system that converts ASL hand gestures into text and speech using MediaPipe and OpenCV. It detects static gestures via webcam, processes hand landmarks, and outputs recognized letters through an interactive GUI with optional speech via pyttsx3. Lightweight and accessible.
# 🤟 Sign Language to Text and Speech Conversion Using Hand Landmarks

A real-time AI-based application that converts American Sign Language (ASL) hand gestures into text and speech using computer vision and hand landmark detection — designed to empower the speech and hearing impaired.
## 📌 Problem Statement

Communication barriers between hearing/speech-impaired individuals and the general population often limit social interaction and accessibility. This project aims to bridge that gap using technology that can understand ASL gestures and output spoken or written communication.
## 🧠 Project Overview

The system uses **MediaPipe** for real-time hand landmark tracking and **OpenCV** to capture video from a webcam. Each gesture is interpreted using predefined rules and mapped to corresponding ASL alphabets. The output is then displayed and optionally spoken using a TTS engine.
## 🚀 Key Features

- 🎥 Real-time gesture detection using a webcam  
- 🖐️ Static ASL alphabet recognition using hand landmarks  
- 💬 Text-to-speech conversion via `pyttsx3`  
- 🖱️ Intuitive GUI with buttons to predict, delete, clear, and speak  
- 💻 No external sensors — only a webcam required  
## 🛠️ Technologies Used

| Component       | Technology       |
|------------------|------------------|
| Programming      | Python            |
| CV Library       | OpenCV            |
| Hand Tracking    | MediaPipe         |
| Speech Engine    | pyttsx3           |
| GUI Framework    | Tkinter           |
## 🗂️ File Structure

- `main.py` – Main logic and GUI  
- `gesture_logic.py` – Hand landmark classification  
- `tts_output.py` – Text-to-speech handler  
- `assets/` – Image or icon files (if any)
## 🔁 Workflow

1. Webcam feed is captured using OpenCV  
2. MediaPipe detects and tracks hand landmarks  
3. Logic maps gesture shape to ASL alphabet  
4. Output is appended to a sentence  
5. Sentence is optionally converted to speech  
## 🧪 Installation & Run

### Install dependencies:

```bash
pip install opencv-python mediapipe pyttsx3

## 🏃‍♀️ **How to Run the Program:

Make sure all dependencies are installed.

```bash
python main.py

