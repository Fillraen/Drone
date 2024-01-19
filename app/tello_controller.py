# tello_controller.py
from djitellopy import Tello
from ultralytics import YOLO
import cv2
import numpy as np

class TelloController:
    def __init__(self):
        self.connected = False
        self.tello = Tello()
        self.frame_read = None
        self.connect_drone()
        
        # Charger le modèle YOLO
        self.yolo_model = YOLO('yolov8s.pt')
        
        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 60
        

    def connect_drone(self):
        self.tello.connect()
        self.tello.streamoff()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()
                
        self.connected = True

    def get_frame(self):
        frame = self.frame_read.frame
        # Traitement de l'image par YOLO
        yolo_results = self.yolo_model(frame)
        # Dessiner les boîtes englobantes et les étiquettes sur l'image
        for box in yolo_results[0].boxes:
            class_id = yolo_results[0].names[box.cls[0].item()]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            conf = round(box.conf[0].item(), 2)
            
            # Choisir la couleur de la boîte en fonction du type d'objet
            if class_id == 'person':
                color = (0, 0, 255) # Rouge pour les personnes
            else:
                color = (0, 255, 0) # Vert pour les autres objets
            
            # Dessiner la boîte englobante
            start_point = (cords[0], cords[1])
            end_point = (cords[2], cords[3])
            thickness = 2
            cv2.rectangle(frame, start_point, end_point, color, thickness)
            
            # Ajouter le texte (étiquette + probabilité)
            text = f"{class_id}: {conf}"
            cv2.putText(frame, text, (cords[0], cords[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame

    def control_drone(self, command):
        if command == 'takeoff':
            self.tello.takeoff()
        elif command == 'land':
            self.tello.land()
        elif command == 'up':
            self.up_down_velocity = self.speed
        elif command == 'down':
            self.up_down_velocity = -self.speed
        elif command == 'left':
            self.left_right_velocity = -self.speed
        elif command == 'right':
            self.left_right_velocity = self.speed
        elif command == 'forward':
            self.for_back_velocity = self.speed
        elif command == 'back':
            self.for_back_velocity = -self.speed
        elif command == 'counter_clockwise':
            self.yaw_velocity = -self.speed
        elif command == 'clockwise':
            self.yaw_velocity = self.speed
        elif command == 'stop':
            self.stop_movement()

        self.update_movement()

    def stop_movement(self):
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.update_movement()

    def update_movement(self):
        self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                                   self.up_down_velocity, self.yaw_velocity)
        
        
    def __del__(self):
        self.tello.end()

