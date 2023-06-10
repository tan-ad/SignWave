import mediapipe as mp
import cv2
import numpy as np
import os
import json

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Folder containing video files
video_folder = 'word videos/'

# Open JSON file for writing
json_file = open('reference.json', 'w')

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    # Create a dictionary to store the hand coordinates
    data = {}

    # Iterate over video files in the folder
    for idx, filename in enumerate(os.listdir(video_folder)):
        if filename.endswith(".mp4"):
            video_file = os.path.join(video_folder, filename)

            # Extract the file name without extension
            file_name = filename.split('.')[0]
            data[file_name] = []

            # Open video file
            cap = cv2.VideoCapture(video_file)

            frame_number = 0

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                # Resize the frame to 800x750
                frame = cv2.resize(frame, (800, 750))

                # Convert the frame to RGB
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detections
                results = hands.process(image_rgb)

                # Check if hand landmarks are detected
                if results.multi_hand_landmarks:
                    # Initialize hand coordinates
                    hand_coordinates = []

                    for hand_landmarks in results.multi_hand_landmarks:
                        hand = hand_landmarks.landmark

                        # Determine handedness based on landmark positions
                        if hand[mp_hands.HandLandmark.WRIST].x < hand[mp_hands.HandLandmark.THUMB_CMC].x:
                            handedness = "Left"
                        else:
                            handedness = "Right"

                        # Store coordinates and joint index in the hand coordinates list
                        for joint_id, landmark in enumerate(hand):
                            x, y, z = landmark.x, landmark.y, landmark.z
                            joint_data = {
                                "Joint Index": joint_id,
                                "Coordinates": [x, y, z]
                            }
                            hand_coordinates.append(joint_data)

                        # Draw landmarks on the frame
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                                  mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2,
                                                                         circle_radius=4),
                                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2,
                                                                         circle_radius=2))

                    # Add frame data to the dictionary
                    data[file_name].append({
                        "Frame": frame_number,
                        "Left Hand Coordinates": hand_coordinates if handedness == "Left" else [],
                        "Right Hand Coordinates": hand_coordinates if handedness == "Right" else []
                    })

                    # Increment the frame number
                    frame_number += 1

                # Display the video frame with landmarks
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()

        # Print the current word during each loop iteration
        print(f"Processing video {idx + 1} of {len(os.listdir(video_folder))}: {file_name}")

    # Serialize the data dictionary to JSON and write it to the file
    json.dump(data, json_file)

# Close the JSON file
json_file.close()

# Open the JSON file for reading
json_file = open('reference.json', 'r')
data = json.load(json_file)
json_file.close()

# Check for large gaps between frames and interpolate
for word in data:
    frames = data[word]
    num_frames = len(frames)

    if num_frames > 1:
        interpolated_frames = []

        for i in range(num_frames - 1):
            current_frame = frames[i]
            next_frame = frames[i + 1]

            if next_frame["Frame"] - current_frame["Frame"] > 1:
                # Compute the gap between frames
                gap = next_frame["Frame"] - current_frame["Frame"]

                # Interpolate hand coordinates for the gap frames
                for j in range(1, gap):
                    interpolation_ratio = j / gap

                    interpolated_coordinates = []

                    # Interpolate each joint's coordinates
                    for joint_data in current_frame["Left Hand Coordinates"]:
                        current_coordinates = joint_data["Coordinates"]
                        next_coordinates = next_frame["Left Hand Coordinates"][joint_data["Joint Index"]]["Coordinates"]

                        interpolated_coordinates.append({
                            "Joint Index": joint_data["Joint Index"],
                            "Coordinates": [
                                current_coordinates[0] + (next_coordinates[0] - current_coordinates[0]) * interpolation_ratio,
                                current_coordinates[1] + (next_coordinates[1] - current_coordinates[1]) * interpolation_ratio,
                                current_coordinates[2] + (next_coordinates[2] - current_coordinates[2]) * interpolation_ratio
                            ]
                        })

                    # Add interpolated frame to the list
                    interpolated_frames.append({
                        "Frame": current_frame["Frame"] + j,
                        "Left Hand Coordinates": interpolated_coordinates,
                        "Right Hand Coordinates": []
                    })

        # Append the interpolated frames to the original frames
        frames.extend(interpolated_frames)

# Serialize the updated data dictionary to JSON and write it to the file
json_file = open('reference.json', 'w')
json.dump(data, json_file)
json_file.close()