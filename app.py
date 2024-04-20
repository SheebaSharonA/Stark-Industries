from flask import Flask, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
import urllib
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)
mp_face_mesh = mp.solutions.face_mesh

def detect_deepfake(video_url):
    try:
        video_stream = urllib.request.urlopen(video_url)
    except Exception as e:
        return {'error': str(e)}
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        frame_count = 0
        fps = 0
        interval = 0
        start_frame = 0
        deepfake_detected = False

        while True:
            bytes = video_stream.read(1024)
            if not bytes:
                break

            frame_count += 1
            nparr = np.frombuffer(bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                continue
            if frame_count == 1:
                fps = int(map.get(cv2.CAP_PROP_FPS))
                interval = fps * 180  

            video_stream.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            previous_landmarks = None
            consecutive_detections_fake = 0
            consecutive_detections_real = 0
            deepfake_detected = False
            real_video_detected = False

            for _ in range(interval):
                ret, frame = map.read()
                if not ret:
                    break
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb_frame)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        landmark_points = []
                        for landmark in face_landmarks.landmark:
                            landmark_x = int(landmark.x * frame.shape[1])
                            landmark_y = int(landmark.y * frame.shape[0])
                            landmark_points.append((landmark_x, landmark_y))

                        for idx, landmark in enumerate(face_landmarks.landmark):
                            cx, cy = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                            cv2.circle(frame, (cx, cy), 2, (0, 255, 0), -1)

                        if previous_landmarks is not None:
                            euclidean_dist = np.linalg.norm(np.array(landmark_points) - np.array(previous_landmarks))

                            if euclidean_dist > 80:  
                                consecutive_detections_fake += 1
                                consecutive_detections_real = 0

                                if consecutive_detections_fake >= 3:  
                                    deepfake_detected = True
                                    break
                            else:
                                consecutive_detections_real += 1
                                consecutive_detections_fake = 0

                                if consecutive_detections_real >= 3:  
                                    real_video_detected = True
                                    break

                        previous_landmarks = landmark_points

                if deepfake_detected or real_video_detected:
                    break

            if deepfake_detected:
                break

            start_frame += interval

    video_stream.close()
    return deepfake_detected

@app.route('/detect_deepfake_youtube', methods=['POST'])
def detect_deepfake_youtube():
    data = request.get_json()
    if 'video_url' not in data:
        return jsonify({'error': 'Missing video_url parameter'}), 

    video_url = data['video_url']
    is_deepfake=detect_deepfake(video_url)
    #is_deepfake = False
    
    return jsonify({'is_deepfake': is_deepfake})

if __name__ == '__main__':
    app.run(debug=True)
