### note:
> This doesn't have to be used for malicious intent, you can use it like a remote terminal. just be careful! Please use this responsibly, i am not responsible for your actions!

---

# What is this?

This repo consists of essentially a Remote Access Tool (RAT). It allows a user to remotely access and control another users or their own computer(kinda), execute commands, upload files and execute them, and potentially steal sensitive data or deploy malware. THIS IS NOT MALWARE, but has an example in it lol!

# How to use & info:

## rat-v1.py
Description - This is a simple easily editable python script that uses remote execution using termux to execute commands on a windows desktop!

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


## rat-v2.py
Description - This is the same as `rat-v1.py` but you can now upload and execute a file from your phone to your pc.

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

* this will destroy a pc(not literaly) if executed properly, please be responsible!

---

# oth/

* other versions of the script(s) made in diffrent languages.
