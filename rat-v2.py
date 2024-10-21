import socket
import threading
import subprocess
import os
import hashlib
import logging

UPLOAD_DIR = os.path.join('uploads')  # Directory to save uploaded files

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of a file for integrity check."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def safe_path(base_dir, file_name):
    """Ensure that the file path is within the intended directory to avoid directory traversal."""
    return os.path.join(base_dir, os.path.basename(file_name))

def handle_client(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            logging.info(f"Received command: {command}")
            
            if command.lower() == 'ping':
                client_socket.send(b'Running')

            elif command.lower() == 'exit':
                client_socket.send(b'Connection closing')
                break

            elif command.lower().startswith('upload '):
                try:
                    file_name = safe_path(UPLOAD_DIR, command[7:])
                    file_size = int(client_socket.recv(1024).decode())
                    client_socket.send(b'Ready to receive file')

                    # File upload process
                    with open(file_name, 'wb') as f:
                        received = 0
                        while received < file_size:
                            data = client_socket.recv(min(file_size - received, 1024))
                            if not data:
                                break
                            f.write(data)
                            received += len(data)

                    client_socket.send(b'File uploaded')

                    # Verify file integrity
                    checksum = calculate_checksum(file_name)
                    client_socket.send(f'Checksum: {checksum}'.encode())

                except Exception as e:
                    logging.error(f"Upload failed: {e}")
                    client_socket.send(f'Upload failed: {str(e)}'.encode())

            elif command.lower().startswith('exec '):
                file_to_run = safe_path(UPLOAD_DIR, command[5:])
                if os.path.isfile(file_to_run):
                    try:
                        subprocess.Popen(file_to_run, shell=True)
                        client_socket.send(b'Execution started')
                        logging.info(f"Execution started for {file_to_run}")
                    except Exception as e:
                        logging.error(f"Execution failed: {e}")
                        client_socket.send(f'Execution failed: {str(e)}'.encode())
                else:
                    client_socket.send(b'File not found')
                    
    except Exception as e:
        logging.error(f"Client handling error: {e}")
    finally:
        client_socket.close()
        logging.info("Connection closed")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # To reuse the socket address
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    logging.info('Listening on port 9999')

    try:
        while True:
            client_socket, addr = server.accept()
            logging.info(f'Accepted connection from {addr}')
            client_socket.settimeout(60)  # Set a timeout for client socket
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    main()
