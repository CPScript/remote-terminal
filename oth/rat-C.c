//This code creates a TCP server that listens on port 9999 and accepts incoming connections. 
//When a client connects, it creates a new thread to handle the client. 
//The client can send commands to the server, such as "ping", "exit", "upload <file_name>", and "exec <file_name>". 
//The server responds accordingly, uploading files to the "uploads/" directory and executing files in that directory.
//
// NOTE:
//This code uses the POSIX socket API and the pthread library for threading. 
//It also uses the system function to execute files, which can be a security risk if not used carefully. 
//Additionally, this code does not handle errors as robustly as it could, and it does not implement any authentication or authorization mechanisms.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define UPLOAD_DIR "uploads/"
#define PORT 9999
#define BUFFER_SIZE 1024

void* handle_client(void* arg);
void create_directory(const char* dir);

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    pthread_t thread;

    // Create upload directory if it doesn't exist
    create_directory(UPLOAD_DIR);

    // Create socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Set address and port number for the server
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Forcefully attaching socket to the port 9999
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    // Bind the socket to the address and port
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 5) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    printf("Listening on port %d...\n", PORT);

    while (1) {
        // Accept incoming connection
        if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }

        printf("Accepted connection from IP address %s and port %d...\n", inet_ntoa(address.sin_addr), ntohs(address.sin_port));

        // Create a new thread to handle the client
        pthread_create(&thread, NULL, handle_client, &new_socket);
    }

    return 0;
}

void* handle_client(void* arg) {
    int new_socket = *((int*)arg);
    char buffer[BUFFER_SIZE];
    char command[BUFFER_SIZE];
    char file_name[BUFFER_SIZE];
    int file_size;
    FILE* file;
    int received;

    while (1) {
        // Receive command from client
        recv(new_socket, command, BUFFER_SIZE, 0);
        command[strcspn(command, "\n")] = 0; // Remove newline character

        if (strcasecmp(command, "ping") == 0) {
            send(new_socket, "Running", 7, 0);
        }
        else if (strcasecmp(command, "exit") == 0) {
            break;
        }
        else if (strncmp(command, "upload ", 7) == 0) {
            // Receive file size from client
            recv(new_socket, buffer, BUFFER_SIZE, 0);
            file_size = atoi(buffer);

            // Send ready signal to client
            send(new_socket, "Ready to receive file", 20, 0);

            // Extract file name from command
            strncpy(file_name, command + 7, BUFFER_SIZE - 7);
            file_name[BUFFER_SIZE - 7] = 0; // Ensure null termination

            // Create file
            file = fopen(UPLOAD_DIR file_name, "wb");
            if (file == NULL) {
                perror("fopen");
                continue;
            }

            received = 0;
            while (received < file_size) {
                // Receive file data from client
                recv(new_socket, buffer, BUFFER_SIZE, 0);
                fwrite(buffer, 1, strlen(buffer), file);
                received += strlen(buffer);
            }

            fclose(file);
            send(new_socket, "File uploaded", 12, 0);
        }
        else if (strncmp(command, "exec ", 5) == 0) {
            // Extract file name from command
            strncpy(file_name, command + 5, BUFFER_SIZE - 5);
            file_name[BUFFER_SIZE - 5] = 0; // Ensure null termination

            // Check if file exists
            if (access(UPLOAD_DIR file_name, F_OK) != -1) {
                // Execute file
                char cmd[256];
                sprintf(cmd, "%s%s", UPLOAD_DIR, file_name);
                system(cmd);
                send(new_socket, "Execution started", 15, 0);
            }
            else {
                send(new_socket, "File not found", 13, 0);
            }
        }
    }

    close(new_socket);
    return NULL;
}

void create_directory(const char* dir) {
    if (mkdir(dir, 0777) == -1) {
        if (errno != EEXIST) {
            perror("mkdir");
            exit(EXIT_FAILURE);
        }
    }
}
