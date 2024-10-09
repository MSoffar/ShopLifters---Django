from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os

# Load your model
model = load_model(r"C:\Users\Lenovo\OneDrive - Alexandria University\Desktop\Projects\ShopLifting - Django\ShopliftingDetection\video_analysis\best_model_LSTM_MOBILE.keras")  # Update the path to your .keras model

def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save()

            # Process the video with your pre-trained model
            video_path = video_instance.video_file.path
            result = process_video(video_path)

            # Pass the result to the template
            return render(request, 'video_analysis/result.html', {'result': result})
    else:
        form = VideoForm()
    return render(request, 'video_analysis/upload.html', {'form': form})
def adjust_frame_count(frames, target_frame_count=100):
    frame_count = len(frames)
    
    if frame_count == target_frame_count:
        return frames
    elif frame_count > target_frame_count:
        # Use uniform sampling to preserve overall structure
        indices = np.linspace(0, frame_count - 1, target_frame_count, dtype=int)
        return [frames[i] for i in indices]
    else:
        # Interpolate missing frames
        repeats = np.ceil(target_frame_count / frame_count).astype(int)
        indices = np.arange(frame_count).repeat(repeats)[:target_frame_count]
        return [frames[i] for i in indices]
def process_video(video_path):
    print("Starting video processing...")  # Initial message

    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    # Step 1: Video Frame Extraction
    print("Extracting and resizing frames...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (128, 128))
        frames.append(resized_frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames.")

    # Step 2: Adjust Frame Count
    print("Adjusting frame count to match model input requirements...")
    frames = adjust_frame_count(frames, target_frame_count=100)
    print(f"Adjusted frame count to {len(frames)} frames.")

    # Step 3: Normalize and Prepare for Prediction
    print("Normalizing frames and preparing for model input...")
    frames = np.array(frames) / 255.0  # Normalize frames
    frames = np.expand_dims(frames, axis=0)  # Add batch dimension
    print("Finished preparing frames for model input.")

    # Step 4: Model Prediction
    print("Starting model prediction...")
    try:
        prediction = model.predict(frames)
        predicted_label = np.argmax(prediction, axis=1)[0]
        print("Model prediction complete.")
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Prediction Error"

    # Step 5: Return Prediction Result
    result = "Shoplifting Detected" if predicted_label == 1 else "No Shoplifting Detected"
    print(f"Prediction result: {result}")
    return result


