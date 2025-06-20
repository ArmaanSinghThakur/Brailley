from vosk import Model, KaldiRecognizer
import pyaudio
import json
from Scan_Function import Scan

import pymysql as msc
import numpy as np
import pyttsx3 as pyttsx

speak= pyttsx.init()

mydb = msc.connect(
    user="root",
    password="1234567890",
    host = "localhost"
)

crs =mydb.cursor()
qry01 ="CREATE DATABASE IF NOT EXISTS Products"
crs.execute(qry01)
qry02 ="USE Products"
crs.execute(qry02)

qry03 ="CREATE TABLE IF NOT EXISTS products(Product_Id int8 primary key, Product_name varchar(200), Product_description varchar(300), Product_Mrp int, Product_Discount int)"
crs.execute(qry03)

qry04= 'insert into products values(8901207004681, "Honey Tus Syrup", "Dabur Honitus Syrup is an Ayurvedic herbal cough remedy that provides effective relief from cough and throat irritation without causing drowsiness.",230,10)'

qry05= """INSERT INTO products (Product_Id, Product_name, Product_description, Product_Mrp, Product_Discount) VALUES
(35000740045, 'Colgate Total Toothpaste 220g', 'Anticavity fluoride toothpaste – Clean Mint', 250, 15),
(6920354811852, 'Colgate Optic White 100g', 'Sparkling White Mint anticavity toothpaste', 300, 10),
(0067238891190, 'Dove Original Beauty Bar 135g', 'Moisturising cream bar soap, ¼ glycerin', 120, 12),
(8711600804357, 'Dove Shea Butter & Vanilla Soap (2×100g)', 'Moisturising cream bar with shea & vanilla', 220, 15),
(8000700000050, 'Dove Beauty Cream Bar 4×90g', 'Moisturising cream bars, pack of 4', 350, 10);"""







speak= pyttsx.init()

voices= speak.getProperty('voices')
voice_id= "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_enUS_MarkM"
speak.setProperty("voice", voice_id)
speak.setProperty("rate", 140)


model = Model("C:\\Users\\hp\\PycharmProjects\\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

print("🎤 Say something...")
__name__== "__main__"
def cmd():
    data = stream.read(4096, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        command = result.get("text", "").lower()
        return command

def Wake(text):
    print("Assistant:", text)
    speak.say(text)
    speak.runAndWait()

def handle_command(command):
    command = command.lower()

    if any(word in command for word in ["hello", "hi", "hey"]):
        say("Hello! How can I assist you today?")

    elif any(word in command for word in ["scan", "product", "information"]):
        print("Scanning")
        num = int(Scan())
        qry05 = f"Select * from Products Where Product_id={num} "
        crs.execute(qry05)
        items = np.array(crs.fetchall())
        if items.any():
            for item in items:
                id = int(item[0])
                name = item[1]
                desc = item[2]
                rate = int(item[3])
                dis = int(item[4])

            text = f"Product {id}, Name {name}, Description {desc}, Rate {rate}, Final price {rate - (rate * dis / 100)}"

    elif "your name" in command:
        say("I am your assistant. You can call me Assistant.")

    elif any(word in command for word in ["bye", "exit", "goodbye", "stop"]):
        say("Goodbye! Have a great day.")
        exit()

    else:
        say("I'm not sure how to respond to that.")


def check(command):

        if any(word in command for word in ["scan","product", "information"]):
            print("Scanning")
            num= int(Scan())
            qry05 = f"Select * from Products Where Product_id={num} "
            crs.execute(qry05)
            items = np.array(crs.fetchall())
            if items.any():
                for item in items:
                    id = int(item[0])
                    name = item[1]
                    desc = item[2]
                    rate = int(item[3])
                    dis = int(item[4])

                text = f"Product {id}, Name {name}, Description {desc}, Rate {rate}, Final price {rate - (rate * dis / 100)}"

                speak.setProperty(rate, 600)
                speak.say(text)
                speak.runAndWait()
                speak.stop()




while __name__ =="__main__":
    command= cmd()
    if any(word in command for word in ["brailey", "bailey", "braley", "braly", "brely"]):
        Wake()


