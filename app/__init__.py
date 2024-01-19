from flask import Flask
from .tello_controller import TelloController

app = Flask(__name__)

tello_controller = TelloController()  # Créez l'instance ici
from app import routes
