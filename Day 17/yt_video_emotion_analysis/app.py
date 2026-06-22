import cv2
import json
import numpy as np
from fer.fer import FER

# 1. Custom JSON Encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

input_video_path = "input_video.mp4"  # Replace with your video file name
cap = cv2.VideoCapture(input_video_path)

fps = cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 30
detector = FER(mtcnn=False)

# Dictionaries to keep track of running totals for averaging
emotion_totals = {
    "angry": 0.0, "disgust": 0.0, "fear": 0.0, 
    "happy": 0.0, "sad": 0.0, "surprise": 0.0, "neutral": 0.0
}
total_faces_detected = 0

print("Analyzing video to compute overall emotion trends...")

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    
    # Analyze 1 frame per second to keep processing fast
    if frame_count % int(fps) != 0:
        continue

    try:
        analysis = detector.detect_emotions(frame)
        
        # Accumulate scores for every face found in this frame
        for face in analysis:
            emotions = face['emotions']
            for emotion_name, score in emotions.items():
                # FER returns values from 0.0 to 1.0, scale it to 100% here
                emotion_totals[emotion_name] += score * 100
            total_faces_detected += 1

    except Exception as e:
        continue

cap.release()

# 2. Compute the final global averages
if total_faces_detected > 0:
    overall_percentages = {
        emotion: round(total_score / total_faces_detected, 2)
        for emotion, total_score in emotion_totals.items()
    }
    # Determine the absolute dominant emotion across the entire video
    overall_dominant = max(overall_percentages, key=overall_percentages.get)
else:
    overall_percentages = {emotion: 0.0 for emotion in emotion_totals}
    overall_dominant = "unknown"

# 3. Structure the final overall summary JSON
overall_summary = {
    "video_source": input_video_path,
    "total_faces_analyzed": total_faces_detected,
    "overall_dominant_emotion": overall_dominant,
    "overall_emotion_percentages": overall_percentages
}

# Serialize and print
output_json = json.dumps(overall_summary, indent=4, cls=NumpyEncoder)

print("\n--- OVERALL VIDEO EMOTION SUMMARY ---")
print(output_json)

# Save to a single file
with open("overall_video_emotion.json", "w") as f:
    f.write(output_json)

print("\nSuccessfully saved summary to 'overall_video_emotion.json'")