from flask import Flask
from config import Config

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Import the routes module
from . import routes

