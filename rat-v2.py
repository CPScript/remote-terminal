import socket
import threading
import subprocess
import os
import hashlib
import logging

UPLOAD_DIR = os.path.join('uploads')
BUFFER_SIZE = 1024

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    """Handle commands from the client."""
    try:
        while True:
            command = client_socket.recv(BUFFER_SIZE).decode().strip()
            if not command:
                break

            logging.info(f"Received command: {command}")
            response = handle_command(command, client_socket)

            client_socket.send(response.encode())

    except Exception as e:
        logging.error(f"Client handling error: {e}")
    finally:
        client_socket.close()
        logging.info("Connection closed")

def handle_command(command, client_socket):
    """Process commands from the client."""
    if command.lower() == 'ping':
        return 'Running'

    elif command.lower() == 'exit':
        return 'Connection closing'

    elif command.lower().startswith('upload '):
        return handle_upload(command[7:], client_socket)

    elif command.lower().startswith('exec '):
        return handle_exec(command[5:])

    return 'Unknown command'

def handle_upload(file_name, client_socket):
    """Handle file upload from the client."""
    try:
        file_path = safe_path(UPLOAD_DIR, file_name)
        file_size = int(client_socket.recv(BUFFER_SIZE).decode())
        client_socket.send(b'Ready to receive file')

        with open(file_path, 'wb') as f:
            received = 0
            while received < file_size:
                data = client_socket.recv(min(file_size - received, BUFFER_SIZE))
                if not data:
                    break
                f.write(data)
                received += len(data)

        logging.info(f'File uploaded: {file_path}')
        checksum = calculate_checksum(file_path)
        return f'File uploaded. Checksum: {checksum}'

    except Exception as e:
        logging.error(f"Upload failed: {e}")
        return f'Upload failed: {str(e)}'

def handle_exec(file_name):
    """Execute a file if it exists."""
    file_path = safe_path(UPLOAD_DIR, file_name)
    if os.path.isfile(file_path):
        try:
            subprocess.Popen(file_path, shell=True)
            logging.info(f"Execution started for {file_path}")
            return 'Execution started'
        except Exception as e:
            logging.error(f"Execution failed: {e}")
            return f'Execution failed: {str(e)}'
    return 'File not found'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    logging.info('Listening on port 9999')

    try:
        while True:
            client_socket, addr = server.accept()
            logging.info(f'Accepted connection from {addr}')
            client_socket.settimeout(60)
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        logging.error(f"Server error: {e")
    finally:
        server.close()

if __name__ == '__main__':
    main()
