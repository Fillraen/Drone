# tello_controller.py
from djitellopy import Tello
from ultralytics import YOLO
import cv2
import mediapipe as mp

import numpy as np
import time
from datetime import datetime
import os

import face_recognition

class TelloController:
    def __init__(self):
        self.connected = False
        self.tello = Tello()    
        self.frame_read = None    
        self.frame_counter = 0  # Compteur pour le suivi des frames.
        self.authorized_face_encodings = []
        self.authorized_face_names = [] 
        
        self.record_path = r"C:\Users\NTAer\Desktop\t-drone\Drone\app\static\assets\video\droneSaved"
        self.photo_path = r"C:\Users\NTAer\Desktop\t-drone\Drone\app\static\assets\img\droneSaved"
        # Charger le modèle YOLO
        self.yolo_model = YOLO('yolov8s.pt')
        
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(0.75)
        
        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 60
        
        self.detectPerson = False
        self.detectFace = False
        self.authorizePerson = False
        
        self.coordonées_lycée_x = 45.8912211001421
        self.coordonées_lycée_y = 6.122589356914184
        self.frame_counter = 0
        self.orientation = 0
        
        self.photo = False
        self.record = False
        self.record_counter = 0
        
        self.frame_width = 960
        self.frame_height = 720
        
        self.load_authorized_faces()
        self.connect_drone()
        
    def connect_drone(self):
        self.tello.connect()
        self.tello.streamoff()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read() 
        self.connected = True   

    def setFreemodeCam(self):
        self.detectPerson = False
        self.detectFace = False
        self.authorizePerson = False
        
    def setSecuritymodeCam(self):
        self.detectPerson = True
        self.detectFace = True
        self.authorizePerson = True
        
    def setRescuemodeCam(self):
        self.detectPerson = True
        self.detectFace = False
        self.authorizePerson = False

    def get_frame(self):
        frame = self.frame_read.frame
        print("Type de frame:", type(frame))
        print("Forme de frame:", frame.shape if frame is not None else "Frame est None")
        self.frame_counter += 1
        # Traitement de l'image par YOLO
        
        # changer les couleurs en rgb
        
        if self.detectPerson == True:
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
                if self.frame_counter >= 5:
                    self.frame_counter = 0 
                    if(class_id == 'person' and conf > 0.85 and self.detectFace == True):
                        results = self.faceDetection.process(frame)
                        if results.detections:
                            for detection in results.detections:
                                bboxC = detection.location_data.relative_bounding_box
                                ih, iw, ic = frame.shape
                                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                                            int(bboxC.width * iw), int(bboxC.height * ih)
                                face_frame = frame[y:y+h, x:x+w]

                                # Dessiner la boîte englobante du visage sur la frame principale
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)



                                # Reconnaissance faciale avec face_recognition
                                rgb_face_frame = face_frame[:, :, ::-1]
                                try:
                                    face_encodings = face_recognition.face_encodings(rgb_face_frame)
                                    print("face endodings : ", face_encodings)
                                    for face_encoding in face_encodings:
                                        matches = face_recognition.compare_faces(self.authorized_face_encodings, face_encoding)
                                        name = "Inconnu"
                                        if True in matches:
                                            first_match_index = matches.index(True)
                                            name = self.authorized_face_names[first_match_index]
                                        print(name)
                                except Exception as e:
                                    print(f"Erreur lors de l'encodage du visage: {e}")
                      
                      
        deplacement_x = self.tello.get_speed_x()
        nouvelle_coor_x = deplacement_x/10*12 + self.coordonées_lycée_x
        deplacement_y = self.tello.get_speed_y()
        nouvelle_coor_y = deplacement_y/10*12 + self.coordonées_lycée_y
        nouvelle_coor_tot = str(nouvelle_coor_x) + ", " + str(nouvelle_coor_y)
        text_coor = "Coordonees: {}".format(nouvelle_coor_tot)
        cv2.putText(frame, text_coor, (10, 110), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
        
        # Afficher toutes les data sur le stream
        text_bat = "Batterie: {}%".format(self.tello.get_battery())
        cv2.putText(frame, text_bat, (5, 720 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        current_time = datetime.now().strftime("%H:%M:%S")
        altitude = self.get_height()/100
        speed = self.get_speed()
        direction = self.direction_actuelle()
        cv2.putText(frame, f"Heure: {current_time}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Altitude: {altitude} m", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Vitesse: {speed*0.36} Km/h", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Direction: {direction}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        if(self.photo == True):
            photo_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(os.path.join(self.photo_path, photo_name), frame)
            self.photo = False
            
            
        if self.record:
            self.video_writer.write(frame)
            
            
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
        elif command == 'photo':
            self.photo = True
        elif command == 'record':
            self.toggle_recording()
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
             
    def load_authorized_faces(self):
        print("debut encoding") 
        directory = r"C:\Users\NTAer\Desktop\t-drone\Drone\app\static\assets\img\authorizedFaces"
        # Par exemple, charger les visages à partir d'un dossier
        for image_file in os.listdir(directory):
            print(image_file)
            image = face_recognition.load_image_file(directory + "/" + image_file)
            encoding = face_recognition.face_encodings(image)[0]
            print("encoding : ")
            print(encoding)
            self.authorized_face_encodings.append(encoding)
            self.authorized_face_names.append(image_file.split(".")[0])  # Nom sans extension
             
    def get_height(self):
        return self.tello.get_barometer() 
    
    def get_speed(self):
        return self.tello.get_speed_x()
             
             
    def direction_actuelle(self):
        """ Retourne la direction cardinale actuelle du drone """
        if 0 <= self.orientation < 90:
            return "Nord"
        elif 90 <= self.orientation < 180:
            return "Est"
        elif 180 <= self.orientation < 270:
            return "Sud"
        else:
            return "Ouest"
             
             
    def toggle_recording(self):
        # Augmenter le compteur et vérifier si c'est pair ou impair
        self.record_counter += 1
        if self.record_counter % 2 == 1:  # Impair : démarrer l'enregistrement
            self.start_recording()
        else:  # Pair : arrêter l'enregistrement
            self.stop_recording()
            
            
    def start_recording(self):
        # Utiliser le temps actuel pour le nom du fichier
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.record_path}/recording_{current_time}.mp4"  # Nom du fichier avec timestamp

        # Initialiser l'enregistrement vidéo
        self.record = True

        # Définir le codec et créer un objet VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec pour l'enregistrement
        self.video_writer = cv2.VideoWriter(filename, fourcc, 30, (self.frame_width, self.frame_height))

    def stop_recording(self):
        # Arrêter l'enregistrement vidéo
        self.record = False
        self.video_writer.release()
    
    def __del__(self):
        self.tello.end()


