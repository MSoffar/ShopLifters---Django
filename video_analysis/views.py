from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
from django.views.decorators.csrf import csrf_exempt
# Load your model (make sure the path is correct)
model = load_model(r"G:/Python/Cellula_Final_cv/ShopLifters---Django/video_analysis/best_model_LSTM_MOBILE.keras") 
@csrf_exempt
def video_upload(request):
    if request.method == 'POST':
        print('Received POST request')  # Log when a request is received

        # Check if a file is included in the request
        if 'video_file' in request.FILES:
            video_file = request.FILES['video_file']
            video_path = save_temp_video(video_file)
            print(f'Temporary video saved at: {video_path}')  # Log the path of the saved video

            # Process the video with your pre-trained model
            result = process_video(video_path)
            print(f'Processing result: {result}')  # Log the processing result

            # Clean up the temporary video file after processing
            os.remove(video_path)
            print(f'Temporary video file removed: {video_path}')  # Log removal of the temp file

            # Prepare the response with prediction class and percentages
            return JsonResponse(result)
        else:
            print('No video file provided in the request')
            return JsonResponse({'error': 'No video file provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def save_temp_video(video_file):
    """ Save the uploaded video file temporarily. """
    temp_video_path = os.path.join("temp_videos", video_file.name)
    with open(temp_video_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    return temp_video_path

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
        predictions = model.predict(frames)
        predicted_label = np.argmax(predictions, axis=1)[0]
        prediction_percentages = predictions[0].tolist()  # Convert to list for JSON response
        print("Model prediction complete.")
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"predicted_class": "Prediction Error", "prediction_percentages": []}

    # Step 5: Return Prediction Result
    result = {
        "predicted_class": "Shoplifting Detected" if predicted_label == 1 else "No Shoplifting Detected",
        "prediction_percentages": prediction_percentages
    }
    print(f"Prediction result: {result}")
    return result

def adjust_frame_count(frames, target_frame_count):
    """ Adjusts the number of frames to the target frame count. """
    if len(frames) > target_frame_count:
        # Reduce number of frames by slicing
        return frames[:target_frame_count]
    elif len(frames) < target_frame_count:
        # Pad with the last frame if fewer frames than target
        frames.extend([frames[-1]] * (target_frame_count - len(frames)))
    return frames
# def video_upload(request):
#     if request.method == 'POST':
#         # Process the uploaded video file
#         # Ensure you are handling the file upload correctly
#         return JsonResponse({'message': 'Video uploaded successfully!'})
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
