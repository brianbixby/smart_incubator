# coding=utf-8
import sys
from datetime import datetime
from time import sleep, time
import serial

from gpiozero import DigitalOutputDevice
import Adafruit_DHT
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

import cv2

DHT_PIN = 4
DHT_MODEL = 11
HEAT_PIN = 17
COOL_PIN = 27
LIGHT_PIN = 18
lastUpdate = 0

print "Initializing grbl communication"
grbl = serial.Serial('/dev/serial0', 115200)
grbl.write("\r\n\r\n")

print "Creating heat/cool pins"
# https://gpiozero.readthedocs.io/en/stable/api_output.html
heatRelay = DigitalOutputDevice(HEAT_PIN)
coolRelay = DigitalOutputDevice(COOL_PIN)
lightRelay = DigitalOutputDevice(LIGHT_PIN)
lightRelay.on()
heatRelay.on()
coolRelay.on()

print "Authenticating with firebase..."
# Use a service account
cred = credentials.Certificate('/home/pi/Pycotronics/private_firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mycotronics2.firebaseio.com/'
})

print "Fetching settings from firebase..."
settings = db.reference("settings/3")
print "Getting reference to logs"
doc = db.reference("logs/3")
print "Getting reference to image bucket"
bucket = storage.bucket("mycotronics2.appspot.com")

def dumpAtLeastOneLine():
    print grbl.readline().strip()
    while grbl.in_waiting:
        print grbl.readline().strip()

print "Initializing VideoCapture"
# noinspection PyArgumentList
cam = cv2.VideoCapture()
print "Finishing grbl initialization"
grbl.flushInput()
grbl.write("G90\n")
dumpAtLeastOneLine()



def regulateTemperature(diff):
    if diff >= 1:
        print "Heating +{0}°C".format(diff)
        coolRelay.on()
        sleep(0.1)  # give time to the relay
        heatRelay.off()
    elif diff <= -2:
        print "Cooling {0}°C".format(diff)
        heatRelay.on()
        sleep(0.1)  # give time to the relay
        coolRelay.off()
    else:
        print "Temperature stabilized, delta={0}°C".format(diff)
        coolRelay.on()
        heatRelay.on()
        sleep(0.1)  # we never know, there might be a bug in the code


def setPosition(angle):
    print "Setting carousel angle to {0}...".format(angle)
    grbl.write("G0 X{0}\n".format(angle))
    sleep(7)
    dumpAtLeastOneLine()

def uploadImage(imageName):
    global bucket
    try:
        blob = bucket.blob("{0}.jpg".format(imageName))
        lightRelay.off()
        sleep(0.02)
        print "Opening camera..."
        cam.open(0)
        print "Taking snapshot"
        _, img = cam.read()
        lightRelay.on()
        print "Closing camera"
        cam.release()
        print "Compressing image"
        b = cv2.imencode('.jpg', img)[1].tostring()
        print "Uploading image..."
        blob.upload_from_string(b, "image/jpeg")
        print "Image uploaded"
    except:
        print "Error", sys.exc_info()[0]

def loop():
    global lastUpdate
    while True:
        print "Fetching T and RH..."
        RH, T = Adafruit_DHT.read_retry(DHT_MODEL, DHT_PIN)
        currentTime = time()
        try:
            print "Polling settings changes"
            settingsResult = settings.get()
            diff = settingsResult["temperature"] - T
        except:
            print "Unexpected error:", sys.exc_info()[0]
            sleep(5)
            continue
        regulateTemperature(diff)
        interval = settingsResult["interval"]
        if currentTime > lastUpdate + interval:
            print "Prepare uploading", interval
            lastUpdate = currentTime - currentTime % interval
            data = {
                "timestamp": {".sv": "timestamp"},
                "temperature": T,
                "humidity": RH,
                "pics": len(settingsResult["states"])
            }
            print "Uploading...", data, datetime.now()
            dataName = doc.push(data).key
            print "Uploaded. Name = ", dataName
            print "Homing..."
            grbl.write("$H\n")
            dumpAtLeastOneLine()
            for key, val in enumerate(settingsResult["states"]):
                setPosition(val)
                uploadImage("{0}_{1}".format(dataName, key))
loop()
