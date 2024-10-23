#!/bin/bash

if ! command -v dialog &> /dev/null; then
    echo "Installing dialog..."
    pkg install dialog -y
fi

SERVER_IP=$(dialog --inputbox "Enter the IP address of the users device:" 8 40 --stdout)
SERVER_PORT=9999

COMMANDS_FILE="commands.txt"

while IFS= read -r command; do
    echo "Sending command: $command"
    echo "$command" | nc "$SERVER_IP" "$SERVER_PORT"
    
    response=$(nc -w 2 "$SERVER_IP" "$SERVER_PORT")
    echo "Response: $response"
done < "$COMMANDS_FILE"
