import cv2
import time
from flask import Flask, Response, jsonify

app = Flask(__name__)

# Kameralar için VideoCapture objeleri (Bilgisayarın kamerasını veya USB kameraları temsil eder)
# Gerçek sahada bunlar Jetson'un CSI kameraları veya RTSP streamleri olabilir.
cameras = {
    'fwd': cv2.VideoCapture(0), # 0 numaralı varsayılan kamera (FWD)
    # Eğer birden fazla kamera takılıysa cv2.VideoCapture(1) vs yapılabilir.
    # Şimdilik arka ve nişan kamerasını simüle etmek için dummy döneceğiz.
}

def generate_frames(cam_id):
    """Kameradan kareleri okuyup MJPEG formatında yayınlar."""
    cap = cameras.get(cam_id)
    
    # Eğer kamera yoksa boş siyah ekran / dummy frame üret
    if cap is None or not cap.isOpened():
        while True:
            # Siyah ekran oluştur (640x480)
            import numpy as np
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"CAM_{cam_id.upper()} NOT FOUND", (100, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)
    
    # Kamera başarılıysa gerçek akış
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Burada Görüntü İşleme (YOLO / OpenCV) algoritmaları çalışacak
            # Örnek: Hedef kutusu çizimi (Demo)
            if cam_id == 'fwd':
                cv2.putText(frame, "ODBARS VISION CORE ONLINE", (20, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Kareyi JPEG formatına dönüştür
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            # MJPEG formatında yield et
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/cam_fwd')
def cam_fwd():
    """Ön Kamera Akışı"""
    return Response(generate_frames('fwd'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam_rear')
def cam_rear():
    """Arka Kamera Akışı (Şimdilik dummy)"""
    return Response(generate_frames('rear'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam_aim')
def cam_aim():
    """Nişan (Atış) Kamerası Akışı (Şimdilik dummy)"""
    return Response(generate_frames('aim'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def status():
    return jsonify({"status": "online", "cameras": {k: v.isOpened() for k, v in cameras.items()}})

if __name__ == '__main__':
    # React ile aynı bilgisayarda çalıştığı için localhost (127.0.0.1) ve Port 5000 üzerinden yayın yapar.
    # Jetson'a geçtiğinizde host='0.0.0.0' yaparak ağa açmalısınız.
    print("🚀 ODBARS Vision Core başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, threaded=True)
