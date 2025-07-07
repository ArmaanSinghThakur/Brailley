from time import sleep

import pyttsx3 as pyttsx
from comtypes.tools.tlbparser import void_type
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from Scan_Function import Scan
import time
import numpy as np
from navigate import *
import pymysql as msc
import pandas as pd
import numpy as np
import pyttsx3 as pyttsx
import Scan_Function
from alert import *
import threading
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
(8000700000050, 'Dove Beauty Cream Bar 4×90g', 'Moisturising cream bars, pack of 4', 350, 10),
(8901030553053, 'Dettol Antiseptic Liquid 500ml', 'Antibacterial disinfectant for first aid and hygiene', 180, 10),
(8901030911211, 'Harpic Power Plus Toilet Cleaner 1L', 'Thick liquid toilet cleaner – Removes tough stains', 150, 12),
(8901058820121, 'Vim Dishwash Bar 300g', 'Power of lemons – removes grease effectively', 25, 0),
(8901571001294, 'Parachute Coconut Hair Oil 500ml', 'Pure coconut oil for hair nourishment', 160, 5),
(8904006301903, 'Tata Salt Iodized 1kg', 'Vacuum evaporated iodised salt – India’s most trusted', 28, 0),
(8906013030100, 'Aashirvaad Whole Wheat Atta 5kg', '100% whole wheat flour – chakki ground', 245, 7),
(8901207003901, 'Sunfeast Dark Fantasy Choco Fills 75g', 'Choco-filled cookies – rich and creamy taste', 35, 5),
(8901030513217, 'Pepsodent Germi Check Toothpaste 150g', 'Cavity protection toothpaste with germ shield', 95, 10),
(8901393050282, 'Pears Pure & Gentle Soap 125g', 'Transparent soap with glycerin and natural oils', 65, 12),
(8901063010457, 'Good Knight Gold Flash Refill 45ml', 'Mosquito repellent refill – dual-mode vaporizer', 89, 8),
(8901030860159, 'Closeup Ever Fresh Red Hot Gel 150g', 'Fresh gel toothpaste with active zinc mouthwash', 95, 10),
(8901058826581, 'Lux Soft Touch Soap 150g', 'Floral beauty soap with silk essence & jasmine', 38, 5),
(8908001159165, 'Nestle Everyday Dairy Whitener 400g', 'Instant milk powder for tea & coffee', 195, 12),
(8906007280943, 'Bru Gold Instant Coffee 100g', 'Premium freeze-dried instant coffee blend', 299, 20),
(8901058843397, 'Wheel Green Detergent Powder 1kg', 'Citrus fragrance detergent for clean and fresh clothes', 60, 0),
(8901030367817, 'Glow & Lovely Advanced Multivitamin 80g', 'Fairness cream with vitamin B3 and sunscreen', 99, 15),
(8901030505585, 'Pond’s Pure White Face Wash 100g', 'Face cleanser with activated charcoal', 125, 10),
(8901138823421, 'Kissan Fresh Tomato Ketchup 950g', 'Made with 100% real tomatoes – no preservatives', 115, 5),
(8904004402404, 'MDH Kitchen King Masala 100g', 'Mixed Indian spices for rich curry flavor', 78, 8),
(8901491100508, 'Nestle Maggi Hot & Sweet Sauce 500g', 'Sweet and spicy tomato chilli sauce', 95, 6);"""
crs.execute(qry04)
crs.execute(qry05)




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
def skip(i):
    i= i+1
    return i
def say(text):
    print("Assistant:", text)
    speak.say(text)
    speak.runAndWait()



def product_details(text):

    for i in range(0, len(text)):
        start_time = time.time()
        buffered_audio = b""
        while time.time() - start_time < 1.5:
            data = stream.read(4096, exception_on_overflow=False)
            buffered_audio += data

        # Recognize extended input
        if recognizer.AcceptWaveform(buffered_audio):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").lower()
            print(command)

            if not command:
                say(text[i])
                continue

            print("Heard:", command)

            # 🔐 Always check override first (even without wake word)
            if "skip" in command:
                if i < len(text) - 1:
                    i = skip(i)
                    say(text[i])
                else:
                    pass


            else:
                say(text[i])
        else:
            say(text[i])


def navigation():
    print("Destination: ")
    time.sleep(2)
    # Recognize extended input
    start_time = time.time()
    buffered_audio = b""
    while time.time() - start_time < 5:
        data = stream.read(4096, exception_on_overflow=False)
        buffered_audio += data
    # Recognize extended input
    if recognizer.AcceptWaveform(buffered_audio):
        result = json.loads(recognizer.Result())
        command = result.get("text", "").lower()
        print("Command: ", command)
        if command:
            print("Command:", command)
            if any(word in command for word in ["groceries", "grocery", "grocires"]):
                say("taking you to Groceries")
                selected= "groceries"
                selected_range = check_section(selected)
                say(f" Navigating to: Groceries (Line Color: {selected_range['color']})")
                navigate(selected_range, False, selected)

            elif any(word in command for word in ["pharmacy", "pharm", "pharma", "farm"]):
                say("taking you to Pharmacy")
                selected = "pharmacy"
                selected_range = check_section(selected)
                say(f" Navigating to: Pharmacy (Line Color: {selected_range['color']})")
                navigate(selected_range, False, selected)

            elif any(word in command for word in ["bakery", "baker", "bread", "cake", "biscuit", "cookie", "cookies"]):
                say("taking you to Bakery")
                selected = "bakery"
                selected_range = check_section(selected)
                say(f" Navigating to: Bakery (Line Color: {selected_range['color']})")
                navigate(selected_range, False, selected)

            elif any(word in command for word in ["checkout", "check", "counter", "reception"]):
                say("taking you to Checkout")
                selected = "checkout"
                selected_range = check_section(selected)
                say(f" Navigating to: Checkout (Line Color: {selected_range['color']})")
                navigate(selected_range, False, selected)

            else:
                say("section not found")
        else:
            say("i cant do that")
    else:
        print("command not registered")



def handle_command(command):
    command = command.lower()
    if "skip" in command:
        skip()

    elif any(word in command for word in ["hello", "hi", "hey"]):
        say("Hello! How can I assist you today?")

    elif any(word in command for word in ["scan", "scan the product", "product", "scan the build up"]):
        say("Scanning now: ")
        num = int(Scan())
        print(num)
        qry = f"Select * from Products Where Product_id={num} "
        crs.execute(qry)
        items = np.array(crs.fetchall())
        print(items)
        if items.any():
            for item in items:
                id = int(item[0])
                name = item[1]
                desc = item[2]
                rate = int(item[3])
                dis = int(item[4])

            say("Item Found.")
            text = [f"Product: {id}", f"Name of Product: {name}", f"About this product: {desc}",
                    f"Rate on the pack{rate} rupees", f"Discount on product: {dis}%",
                    f"Rate after discount: {rate - (rate * dis / 100)} rupees"]
            product_details(text)

        elif any(word in command for word in ["help", "helped", "helps"]):
            message= alert()
            time.sleep(1)
            say(message)
        else:
            say("No Product Found")

    elif any(word in command for word in ["navi", "navigate", "navigation", "navigated", "navigates"]):
        say("Where do you wanna go? ")
        navigation()



    elif "your name" in command:
        say("I am your assistant. You can call me Assistant.")

    elif any(word in command for word in ["bye", "exit", "goodbye", "stop"]):
        say("Goodbye! Have a great day.")
        exit()

    else:
        say("I'm not sure how to respond to that.")



while True:
    data = stream.read(4096, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        command = result.get("text", "").lower()

        if not command:
            continue

        print("Heard:", command)

        # Check for wake word
        if any(word in command for word in ["brailey", "bailey", "braley", "braly", "brely", "barely", "billy", "really"]):
            say("Yes Sir! How May I Help You?")
            print("Listening for your command...")

            # Extend listening time (5 seconds)
            start_time = time.time()
            buffered_audio = b""
            while time.time() - start_time < 5:
                data = stream.read(4096, exception_on_overflow=False)
                buffered_audio += data

            # Recognize extended input
            if recognizer.AcceptWaveform(buffered_audio):
                result = json.loads(recognizer.Result())
                new_command = result.get("text", "").lower()



                if new_command:
                    print("Command:", new_command)
                    handle_command(new_command)
                else:
                    say("I didn't catch that. Could you repeat?")
            else:
                say("I didn't catch that. Could you repeat?")

