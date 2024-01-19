from flask import render_template, Flask, Response
from app import app, tello_controller 
import cv2
from flask import jsonify
import os 



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/free-control')
def free_control():
    tello_controller.setFreemodeCam()
    return render_template('page/freeControl.html')

@app.route('/rescue-control')
def rescue_control():
    tello_controller.setRescuemodeCam()
    return render_template('page/rescueControl.html')

@app.route('/security-control')
def security_control():
    tello_controller.setSecuritymodeCam()
    return render_template('page/securityControl.html')


@app.route('/gallery')
def gallery():
    image_folder = os.path.join(app.static_folder, 'assets/img/droneSaved')
    images = os.listdir(image_folder)
    return render_template('page/photoGalery.html', images=images)

@app.route('/video')
def video():
    video_folder = os.path.join(app.static_folder, 'assets/video/droneSaved')
    videos = os.listdir(video_folder)
    return render_template('page/videoGalery.html', videos=videos)


def generate_video_stream():
    while True:
        frame = tello_controller.get_frame()  # Récupère la frame traitée depuis votre TelloController
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command/<cmd>')
def send_command(cmd):
    print(cmd)
    tello_controller.control_drone(cmd)
    return "Command sent"

@app.route('/drone/status')
def drone_status():
    return jsonify({"connected": tello_controller.connected})


@app.route('/drone/reconnect')
def drone_reconnect():
    try:
        tello_controller.connect_drone()  # Tentative de reconnexion
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
