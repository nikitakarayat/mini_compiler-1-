from flask import Flask, request, jsonify, send_from_directory
import os
import base64
import cv2
import numpy as np
from deepface import DeepFace
import random

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/music/<emotion>/<filename>')
def serve_music(emotion, filename):
    return send_from_directory(f'music/{emotion}', filename)

@app.route('/detect', methods=['POST'])
def detect_emotion():
    data = request.get_json()
    img_data = data.get("image", "")

    if 'base64,' in img_data:
        img_data = img_data.split('base64,')[1]

    try:
        image_bytes = base64.b64decode(img_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion'].lower()

        music_folder = os.path.join('music', emotion)
        if not os.path.exists(music_folder) or not os.listdir(music_folder):
            return jsonify({'emotion': emotion, 'music': None})

        music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        selected_song = random.choice(music_files)

        return jsonify({'emotion': emotion, 'music': f'/music/{emotion}/{selected_song}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
