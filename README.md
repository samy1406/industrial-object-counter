# 🏭 Industrial Object Counter

Real-time industrial object counter using background subtraction and blob detection with OpenCV

![Demo](demo/demo.gif)

---

## 📌 Problem Statement

In industrial environments such as warehouses and logistics centers, counting packages on a conveyor belt manually is inefficient and error-prone. This project implements a computer vision pipeline that automatically counts objects crossing a defined line in real-time using background subtraction — no deep learning required. The system processes video frame-by-frame, isolates moving objects from a static background, and increments a count each time an object crosses the detection line.

---

## 🏗️ Architecture

```
Video Input
    │
    ▼
ROI Crop (40%–80% of frame height)
    │
    ▼
Grayscale Conversion
    │
    ▼
Background Subtraction (MOG2)
    │
    ▼
Morphological Opening (noise removal)
    │
    ▼
Contour Detection (largest contour)
    │
    ▼
Centroid Calculation (cx, cy)
    │
    ▼
Line Crossing Detection
    │
    ▼
Count Increment + Annotated Output Video
```

---

## 🎯 Results

| Metric | Value |
|--------|-------|
| Test Video | Conveyor belt with mixed packages |
| Actual Packages | ~9–10 |
| Detected Count | 10 |
| Accuracy | ~95% |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![NumPy](https://img.shields.io/badge/NumPy-latest-orange)

---

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- GitHub Codespaces or local Linux environment

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/samy1406/industrial-object-counter.git
cd industrial-object-counter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your video
# Place your conveyor belt video in the data/ folder
# Rename it to conveyor.mp4

# 4. Run the counter
python src/object_counter.py
```

### Output
- Annotated video saved as `output_mask.avi` in the root directory
- Final count printed in the terminal

---

## 📁 Project Structure

```
industrial-object-counter/
├── src/
│   └── object_counter.py      # Main pipeline
├── data/
│   └── conveyor.mp4           # Input video (not tracked in git)
├── demo/
│   └── demo.gif               # Output demo
├── requirements.txt
├── README.md
└── LEARNING.md
```

---

## 🔍 How It Works

### 1. Region of Interest (ROI)
Only the conveyor belt area (40%–80% of frame height) is processed to eliminate background noise from shelves and surroundings.

### 2. Background Subtraction (MOG2)
`cv2.createBackgroundSubtractorMOG2()` continuously learns the static background over time and outputs a binary mask where white pixels represent moving objects. Unlike simple frame differencing, MOG2 adapts to gradual lighting changes.

### 3. Morphological Opening
Erosion followed by dilation removes small noise blobs while preserving real object shapes.

### 4. Largest Contour Tracking
Instead of tracking all contours (which causes overcounting), only the largest contour per frame is tracked — representing the most prominent object in the scene.

### 5. Line Crossing Detection
A vertical counting line is placed at 50% of frame width. A crossing is detected when:
```
previous_cx >= line_x AND current_cx < line_x
```
This fires exactly once per object crossing.

---

## ⚠️ Limitations

- Background subtraction struggles with sudden lighting changes
- Multiple overlapping packages may be counted as one
- MOG2 requires ~50 frames to stabilize at the start of the video
- Tracks only the largest contour — smaller objects behind a larger one may be missed

---

## 📚 What I Learned

See [LEARNING.md](LEARNING.md)

---

## 🔮 Future Improvements

- Replace background subtraction with YOLOv8 for more robust detection
- Add multi-object tracking (ByteTrack) to handle overlapping packages
- Deploy as a FastAPI endpoint with live camera feed
- Add direction detection (left→right vs right→left)

---

## 👤 Author

**Samy** — [GitHub](https://github.com/samy1406) | [YouTube](#)

