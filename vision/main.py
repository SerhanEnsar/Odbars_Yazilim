# Copyright (c) 2026 Serhan Ensar. All rights reserved.
import cv2
import time
import numpy as np
from flask import Flask, Response, jsonify

app = Flask(__name__)

# Kamera objeleri - izin hatası için güvenli başlatma
cameras = {}

try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cameras['fwd'] = cap
        print("✅ Kamera 0 (FWD) başarıyla açıldı.")
    else:
        print("⚠️  Kamera 0 açılamadı, dummy mod aktif.")
except Exception as e:
    print(f"⚠️  Kamera başlatma hatası: {e}")


def make_dummy_frame(cam_id, message="NO SIGNAL"):
    """Sinyal yoksa siyah ekranda metin gösteren dummy kare üretir."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(frame, f"CAM_{cam_id.upper()}", (200, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (80, 80, 80), 2)
    cv2.putText(frame, message, (220, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 80, 200), 2)
    return frame


def generate_frames(cam_id):
    """Kameradan kareleri okuyup MJPEG formatında yayınlar."""
    cap = cameras.get(cam_id)

    # Kamera yoksa dummy akış
    if cap is None or not cap.isOpened():
        while True:
            frame = make_dummy_frame(cam_id)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.1)
        return

    # Gerçek kamera akışı
    while True:
        success, frame = cap.read()
        if not success:
            # Okuma başarısız olursa dummy göster
            frame = make_dummy_frame(cam_id, "READ ERROR")
        else:
            # --- GORUNTU ISLEME ALANI ---
            # Buraya YOLO / OpenCV algoritmaları eklenecek
            if cam_id == 'fwd':
                cv2.putText(frame, "ODBARS VISION CORE ONLINE", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/cam_fwd')
def cam_fwd():
    return Response(generate_frames('fwd'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam_rear')
def cam_rear():
    return Response(generate_frames('rear'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam_aim')
def cam_aim():
    return Response(generate_frames('aim'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "cameras": {k: v.isOpened() for k, v in cameras.items()}
    })

if __name__ == '__main__':
    print("🚀 ODBARS Vision Core başlatılıyor...")
    print("   Stream URL'leri: http://127.0.0.1:8765/cam_fwd")
    # Port 8765 (Mac AirPlay 5000'i kullanır)
    app.run(host='0.0.0.0', port=8765, threaded=True)
