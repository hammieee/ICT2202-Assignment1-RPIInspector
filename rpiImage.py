import pyfiglet
import os

ascii_banner = pyfiglet.figlet_format("RPI Inspector")
print(ascii_banner)

menu = {}
menu['1']="Disk Imaging" 
menu['2']="Function 2"
menu['3']="Function 3"
menu['4']="Exit"

def image():
    #Reference: https://stackoverflow.com/questions/17008042/python-disk-imaging
    description = "This option is to image the Raspberry Pi's SD card. You can also specify the sector size you want."
    cmd = 'lsblk'
    os.system(cmd)
    source = input("\nEnter the source's absolute path (/dev/sda): ")
    dest   = input("Enter the destination's absolute path (/home/kali/image.dd): ")
    sector = int(input("Enter sector size (Default:512) : "))
    with open(source,'rb') as f:
        with open(dest, "wb") as i:
            while True:
                if i.write(f.read(sector)) == 0:
                    break




while True: 
    options=menu.keys()
    #options.sort()
    for entry in options: 
        print(entry, menu[entry])

    selection=input("\nPlease Select: ") 
    if selection =='1': 
        image() 
    elif selection == '2': 
        print("func2")
    elif selection == '3':
        print("func3")
    elif selection == '4': 
        print("Exiting~")
        break
    else: 
        print("Unknown Option Selected!") 
