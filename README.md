# What is this?
idk, **rat** a remote access tool? idk XD
(honestly, idk what this is classified as)

---

## rat-v1
Description - This is a simple easily editable python script that uses remote execution like a remote bomb to execute commands!

### How to use
On your phone using Termux, you can use `nc` (Netcat) to interact with the script:
* **Ping the script** (check if it's running):
  ```
  echo "ping" | nc {PC_IP_ADDRESS} 9999
  ```

* **Execute a command**:
  ```
  echo "exec <your_command_here>" | nc {PC_IP_ADDRESS} 9999
  ```
  
> NOTE: Replace {PC_IP_ADDRESS} with the IP address of your Windows PC. Make sure your firewall allows connections on port 9999.
---


## rat-v2
Description - This is the same as `bomb-v1` but you can now upload a file from your phone to your pc

### How to use
On your phone using Termux, you can use `nc` (Netcat) to interact with the script:
* **Ping the script** (check if it's running):
  ```
  echo "ping" | nc {PC_IP_ADDRESS} 9999
  ```

* **Execute a command**:
  ```
  echo "exec <your_command_here>" | nc {PC_IP_ADDRESS} 9999
  ```

* **Upload a file** to the Windows PC
  ```
  echo "upload your_file_name.exe" | nc {PC_IP_ADDRESS} 9999
  cat your_file_name.exe | nc {PC_IP_ADDRESS} 9999
  ```

* **Execute the uploaded file:**
  ```
  echo "exec your_file_name.exe" | nc {PC_IP_ADDRESS} 9999
  ```

> NOTE: Replace `your_file_name.exe` with the file you want to upload and `{PC_IP_ADDRESS}` with the IP address of your Windows PC.


---

# src/bomb.py
(this is an example on how you can make a "remote bomb" out of this script lol)

* this will destroy a pc(not literaly) if executed properly
