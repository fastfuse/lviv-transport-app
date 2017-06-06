
import os
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

client = MongoClient()
db = client[app.config['DATABASE_URL']]


from app import views
