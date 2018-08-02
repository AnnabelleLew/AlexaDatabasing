from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import json
import random
from face_rec.main import *

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    welcome_message = 'Hello! Would you like for me to detect faces or log a person?'
    return question(welcome_message)

@ask.intent("LogIntent")
def log_faces(Name):
    confirmation = "Logged {} in database successfully".format(Name)
    log_person(Name)
    return statement(confirmation)

@ask.intent("DetectIntent")
def name_faces():
    msg = detect()
    return statement(msg)

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent("AMAZON.NoIntent")
def stop_alexa():
    quit = "Alright, goodbye."
    return statement(quit)

def detect():
    faces = labelling()
    if len(faces) == 0:
        msg = "I don't see any faces."
    elif len(faces) == 1:
        if faces[0] != "???":
            msg = "I see {}.".format(faces[0])
        else:
            msg = "I see a face I don't recognize."
    else:
        msg = "I see "
        new_faces = 0
        for face in faces:
            if face != "???":
                msg += face + ", "
            else:
                new_faces += 1
        msg += " and {} new faces.".format(new_faces)
    return msg

if __name__ == '__main__':
    app.run(debug=True)
