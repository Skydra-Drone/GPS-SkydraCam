import cv2
import requests
from flask import Flask, request, jsonify
import threading

# Flask server for receiving GPS data
app = Flask(__name__)
gps_data = {"lat": None, "lon": None}

@app.route("/update_location", methods=["POST"])
def update_location():
    global gps_data
    data = request.json
    gps_data["lat"] = data.get("latitude")
    gps_data["lon"] = data.get("longitude")
    return jsonify({"status": "ok"})

def run_server():
    app.run(host="0.0.0.0", port=5000)

# Start server thread
threading.Thread(target=run_server, daemon=True).start()

# IP Webcam video stream
phone_ip = "192.168.1.6:8080"  # <-- change to your phone's IP
video_url = f"http://{phone_ip}:8080/video"

cap = cv2.VideoCapture(video_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Overlay GPS coordinates if available
    if gps_data["lat"] and gps_data["lon"]:
        overlay_text = f"Lat: {gps_data['lat']:.6f}, Lon: {gps_data['lon']:.6f}"
        cv2.putText(frame, overlay_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Live Video + GPS", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
