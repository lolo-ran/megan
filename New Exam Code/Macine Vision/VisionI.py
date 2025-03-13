
import cv2
import numpy as np
import mediapipe as mp
import os

# Define the directory to save videos
save_directory = 'videos'  # Changed to be in the current directory
# Create the directory if it does not exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Initialize MediaPipe Pose and Hands
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose()
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Define the indexes for arm landmarks from Pose solution
pose_landmarks = [
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.LEFT_ELBOW,
    mp_pose.PoseLandmark.LEFT_WRIST,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_ELBOW,
    mp_pose.PoseLandmark.RIGHT_WRIST
]

# Define hand landmarks indexes and colors for each finger
hand_landmarks = list(range(21))  # 21 landmarks for each hand
outline_color = (0, 0, 0)  # Black for outlines
finger_colors = {
    'thumb': (0, 128, 255),  # Dark Orange
    'index': (0, 0, 255),    # Red
    'middle': (0, 255, 0),   # Green
    'ring': (255, 0, 0),     # Blue
    'pinky': (255, 20, 147)  # Deep Pink
}

# Define finger connections and corresponding colors
finger_connections = {
    'thumb': [(1, 2), (2, 3), (3, 4)],
    'index': [(5, 6), (6, 7), (7, 8)],
    'middle': [(9, 10), (10, 11), (11, 12)],
    'ring': [(13, 14), (14, 15), (15, 16)],
    'pinky': [(17, 18), (18, 19), (19, 20)]
}

# Initialize VideoCapture
cap = cv2.VideoCapture(0)

# Initialize VideoWriters for output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_with_graphics = None
out_graphics_only = None
recording = False
print("Press 'r' to start recording and 's' to stop recording. Press 'ESC' or close the window to exit.")

def interpolate_points(start, end, num_points=5):
    """Interpolate additional points between start and end."""
    start = np.array(start)
    end = np.array(end)
    return [(start + (end - start) * t / num_points).astype(int) for t in range(num_points + 1)]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Flip the image horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    
    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image and find poses and hands
    pose_results = pose.process(rgb_frame)
    hand_results = hands.process(rgb_frame)
    
    # Create a blank white image for graphics only
    blank_image = np.ones_like(frame) * 255
    
    if pose_results.pose_landmarks:
        # Draw arm landmarks and lines for the arms
        arm_landmarks_px = []
        for landmark_idx in pose_landmarks:
            landmark = pose_results.pose_landmarks.landmark[landmark_idx]
            landmark_px = (int(landmark.x * width), int(landmark.y * height))
            arm_landmarks_px.append(landmark_px)
            cv2.circle(frame, landmark_px, 5, outline_color, -1)
            cv2.circle(blank_image, landmark_px, 5, outline_color, -1)

        # Draw lines connecting arm landmarks
        connections = [
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
            (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
            (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
            (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
        ]
        for start_idx, end_idx in connections:
            cv2.line(frame,
                    (int(pose_results.pose_landmarks.landmark[start_idx].x * width),
                    int(pose_results.pose_landmarks.landmark[start_idx].y * height)),
                    (int(pose_results.pose_landmarks.landmark[end_idx].x * width),
                    int(pose_results.pose_landmarks.landmark[end_idx].y * height)),
                    outline_color, 2)
            cv2.line(blank_image,
                    (int(pose_results.pose_landmarks.landmark[start_idx].x * width),
                    int(pose_results.pose_landmarks.landmark[start_idx].y * height)),
                    (int(pose_results.pose_landmarks.landmark[end_idx].x * width),
                    int(pose_results.pose_landmarks.landmark[end_idx].y * height)),
                    outline_color, 2)

        # Draw arm outlines (polylines) for left and right arms with additional points
        left_arm = [pose_results.pose_landmarks.landmark[idx] for idx in [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST
        ]]
        right_arm = [pose_results.pose_landmarks.landmark[idx] for idx in [
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST
        ]]
        left_arm_points = []
        for start, end in zip(left_arm, left_arm[1:]):
            left_arm_points.extend(interpolate_points([start.x * width, start.y * height], [end.x * width, end.y * height]))
        
        right_arm_points = []
        for start, end in zip(right_arm, right_arm[1:]):
            right_arm_points.extend(interpolate_points([start.x * width, start.y * height], [end.x * width, end.y * height]))

        left_arm_points = np.array(left_arm_points, np.int32)
        right_arm_points = np.array(right_arm_points, np.int32)
        cv2.polylines(frame, [left_arm_points], isClosed=False, color=outline_color, thickness=2)
        cv2.polylines(blank_image, [left_arm_points], isClosed=False, color=outline_color, thickness=2)
        cv2.polylines(frame, [right_arm_points], isClosed=False, color=outline_color, thickness=2)
        cv2.polylines(blank_image, [right_arm_points], isClosed=False, color=outline_color, thickness=2)
    
    if hand_results.multi_hand_landmarks:
        for hand_landmarks_list in hand_results.multi_hand_landmarks:
            hand_landmarks_px = []
            for i, landmark_idx in enumerate(hand_landmarks):
                landmark = hand_landmarks_list.landmark[landmark_idx]
                landmark_px = (int(landmark.x * width), int(landmark.y * height))
                hand_landmarks_px.append(landmark_px)
                # Determine which finger the landmark belongs to
                if 1 <= i <= 4:
                    finger = 'thumb'
                elif 5 <= i <= 8:
                    finger = 'index'
                elif 9 <= i <= 12:
                    finger = 'middle'
                elif 13 <= i <= 16:
                    finger = 'ring'
                else:
                    finger = 'pinky'
                # Draw landmarks with corresponding color
                cv2.circle(frame, landmark_px, 5, finger_colors[finger], -1)
                cv2.circle(blank_image, landmark_px, 5, finger_colors[finger], -1)
            
            # Draw lines connecting hand landmarks with corresponding color
            for finger, connections in finger_connections.items():
                color = finger_colors[finger]
                for start_idx, end_idx in connections:
                    cv2.line(frame,
                            (int(hand_landmarks_list.landmark[start_idx].x * width),
                            int(hand_landmarks_list.landmark[start_idx].y * height)),
                            (int(hand_landmarks_list.landmark[end_idx].x * width),
                            int(hand_landmarks_list.landmark[end_idx].y * height)), 
                            color, 2)
                                
                    cv2.line(blank_image,
                            (int(hand_landmarks_list.landmark[start_idx].x * width),
                            int(hand_landmarks_list.landmark[start_idx].y * height)),
                            (int(hand_landmarks_list.landmark[end_idx].x * width),
                            int(hand_landmarks_list.landmark[end_idx].y * height)),
                            color, 2)
            
            # Draw hand outlines (polylines) with additional points
            for finger, points in {
                'thumb': [1, 2, 3, 4],
                'index': [5, 6, 7, 8],
                'middle': [9, 10, 11, 12],
                'ring': [13, 14, 15, 16],
                'pinky': [17, 18, 19, 20]
            }.items():
                finger_points = []
                for start, end in zip(points, points[1:]):
                    finger_points.extend(interpolate_points(
                        [hand_landmarks_list.landmark[start].x * width,
                         hand_landmarks_list.landmark[start].y * height],
                        [hand_landmarks_list.landmark[end].x * width, 
                         hand_landmarks_list.landmark[end].y * height]))
                
                finger_points = np.array(finger_points, np.int32)
                cv2.polylines(frame, [finger_points], isClosed=False, color=outline_color, thickness=2)
                cv2.polylines(blank_image, [finger_points], isClosed=False, color=outline_color, thickness=2)

    # Display the frame with overlay
    cv2.imshow("Pose Detection - With Graphics", frame)
    cv2.imshow("Pose Detection - Graphics Only", blank_image)

    # Write to video files if recording
    if recording:
        if out_with_graphics:
            out_with_graphics.write(frame)
        if out_graphics_only:
            out_graphics_only.write(blank_image)
    
    key = cv2.waitKey(1) & 0xFF  # Convert to 8-bit
    if key == 27:  # ESC key
        # Exit the program
        break
    elif key == ord('r') and not recording:
        # Start recording
        recording = True
        out_with_graphics = cv2.VideoWriter(os.path.join(save_directory, 'recording_with_graphics.mp4'), fourcc, 20.0, (width, height))
        out_graphics_only = cv2.VideoWriter(os.path.join(save_directory, 'recording_graphics_only.mp4'), fourcc, 20.0, (width, height))
        print("Recording started")
    elif key == ord('s') and recording:
        # Stop recording
        recording = False
        if out_with_graphics:
            out_with_graphics.release()
        if out_graphics_only:
            out_graphics_only.release()
        print("Recording stopped")
    
    # Check if the window was closed
    if cv2.getWindowProperty("Pose Detection - With Graphics", cv2.WND_PROP_VISIBLE) < 1:
        break
        
# Release resources
cap.release()
if out_with_graphics:
    out_with_graphics.release()
if out_graphics_only:
    out_graphics_only.release()
cv2.destroyAllWindows()
