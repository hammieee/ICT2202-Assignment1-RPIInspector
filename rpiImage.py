import pyfiglet
import os
import sys

ascii_banner = pyfiglet.figlet_format("RPI Inspector v4")
print(ascii_banner)

menu = {}
menu['1']="Disk Imaging" 
menu['2']="Mount Image"
menu['3']="Generate Report"
menu['4']="Exit"

src_path = None
dest_path = None

path = os.getcwd()

def image():
    #Reference: https://stackoverflow.com/questions/17008042/python-disk-imaging
    description = "This option is to image the Raspberry Pi's SD card. You can also specify the sector size you want."
    print(description)
    cmd = 'lsblk'
    os.system(cmd)
    print("\nCurrent Directly: " + path)
    source = input("\nEnter the source's absolute path (/dev/sda): ")
    dest   = input("Enter the destination's filename (e.g. image.dd): ")
    global src_path
    src_path = source
    global dest_path
    dest = path+'/'+dest
    dest_path = dest
    cmd = 'sudo dd if=' + source + ' of=' + dest + ' bs=4096 conv=noerror,sync status=progress'
    os.system(cmd)
    print("\nRaspberry Pi has been imaged! \n\nThe SHA256 hash is:")
    cmd = 'sudo sha256sum ' + source
    os.system(cmd)
    cmd = 'sudo sha256sum ' + dest
    os.system(cmd)
    
    #sector = int(input("Enter sector size (Default:512) : "))
    #with open(source,'rb') as f:
    #    with open(dest, "wb") as i:
    #        while True:
    #            if i.write(f.read(sector)) == 0:
    #                print("Done Imaging")
    #                break

def mount():
    cmd = 'mkdir -p '+path+'/mbr '+path+'/filesystem'
    os.system(cmd)
    global dest_path
    if dest_path != None:
        cmd = 'fdisk -l '+dest_path
    else:
        dest   = input("Enter the image's name (e.g. image.dd): ")
        dest_path = path+'/'+dest
        cmd = 'fdisk -l '+dest
    os.system(cmd)

    print("\nTake note of the start block for Sector size, sdb1 and sdb2 that you wish to mount\n")
    sector = input("Enter the Sector size: ")
    start1 = input("Enter the start sector of image 1: ")
    start2 = input("Enter the start sector of image 2: ")
    print(dest_path)
    while True:
        choice = input("Select the image you would like to mount (1 or 2 | 0 to exit): ")
        if choice == '1':
            m1(sector,start1)
        elif choice == '2':
            m2(sector,start2)
        elif choice == '0':
            print("\n\n")
            break
        else:
            print("Unknown Option Selected!") 

def generate():
    if os.path.isdir(path+'/filesystem') == True:
        ssh()
        installedpack()
        upgradedpack()
        removedpack()
        loginoutrecord()
        filenames = ['SSHLogin.txt', 'InstalledPackages.txt', 'UpgradedPackages.txt', 'RemovedPackages.txt', 'LoginoutRecords.txt']
        with open('Report.txt', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)
        cmd = 'mkdir report'
        os.system(cmd)
        cmd = 'mv SSHLogin.txt report'
        os.system(cmd)
        cmd = 'mv InstalledPackages.txt report'
        os.system(cmd)
        cmd = 'mv UpgradedPackages.txt report'
        os.system(cmd)
        cmd = 'mv RemovedPackages.txt report'
        os.system(cmd)
        cmd = 'mv LoginoutRecords.txt report'
        os.system(cmd)
    else:
        print('\nPlease mount the file system (option 2) before generating report\n')
    
def ssh():
    fopen = open('SSHLogin.txt', 'w+')
    fopen.write("SSH Login Attempts \n")
    cmd = 'cat '+path+'/filesystem/var/log/auth.log >> SSHLogin.txt'
    os.system(cmd)
    fopen.close()

def installedpack():
    fopen = open('InstalledPackages.txt', 'w+')
    fopen.write("History of installed packages\n")
    cmd = 'grep "install" '+path+'/filesystem/var/log/dpkg.log >> InstalledPackages.txt'
    os.system(cmd)
    cmd = 'grep "install" '+path+'/filesystem/var/log/dpkg.log.1 >> InstalledPackages.txt'
    os.system(cmd)
    #for i in range(2, 13):
        #str1 = 'zgrep "install" /var/log/dpkg.log.'
        #str2 = '.gz >> InstalledPackages.txt'
        #cmd = str1 + str(i) + str2
        #os.system(cmd)
    cmd = 'zgrep "install" '+path+'/filesystem/var/log/dpkg.log.2.gz >> InstalledPackages.txt'
    os.system(cmd)
    fopen.close()

def upgradedpack():
    fopen = open('UpgradedPackages.txt', 'w+')
    fopen.write("History of upgraded packages\n")
    cmd = 'grep "upgrade" '+path+'/filesystem/var/log/dpkg.log >> UpgradedPackages.txt'
    os.system(cmd)
    cmd = 'grep "upgrade" '+path+'/filesystem/var/log/dpkg.log.1 >> UpgradedPackages.txt'
    os.system(cmd)
    #for i in range(2, 13):
        #str1 = 'zgrep "upgrade" /var/log/dpkg.log.'
        #str2 = '.gz >> UpgradedPackages.txt'
        #cmd = str1 + str(i) + str2
        #os.system(cmd)
    cmd = 'zgrep "upgrade" '+path+'/filesystem/var/log/dpkg.log.2.gz >> UpgradedPackages.txt'
    os.system(cmd)
    fopen.close()

def removedpack():
    fopen = open('RemovedPackages.txt', 'w+')
    fopen.write("History of removed packages\n")
    cmd = 'grep "remove" '+path+'/filesystem/var/log/dpkg.log >> RemovedPackages.txt'
    os.system(cmd)
    cmd = 'grep "remove" '+path+'/filesystem/var/log/dpkg.log.1 >> RemovedPackages.txt'
    os.system(cmd)
    #for i in range(2, 13):
        #str1 = 'zgrep "remove" /var/log/dpkg.log.'
        #str2 = '.gz >> RemovedPackages.txt'
        #cmd = str1 + str(i) + str2
        #os.system(cmd)
    cmd = 'zgrep "remove" '+path+'/filesystem/var/log/dpkg.log.2.gz >> RemovedPackages.txt'
    os.system(cmd)
    fopen.close()

def loginoutrecord():
    fopen = open('LoginoutRecords.txt', 'w+')
    fopen.write("\nLogin/Logout Records\n")
    cmd = 'last -f ' +path+'/var/log/wtmp >> LoginoutRecords.txt'
    os.system(cmd)
    fopen.close()

def m1(sector,start1):
    cmd = "sudo umount -q "+path+"/filesystem/"
    os.system(cmd)
    print("Mounting Image 1..."+ start1 +"...")
    cmd = "sudo mount -r "+dest_path+" -o loop,offset=$(( "+sector+" * "+start1+")) "+path+"/mbr/"
    print(cmd)
    os.system(cmd) 
    print("MBR Mounted!")
    print("\nYou can now access it from "+path+"/mbr\n")
    #os.system("gnome-terminal -e 'bash -c \"ls ~/Desktop/img1; exec bash\"'")
def m2(sector,start2):
    cmd = "sudo umount -q "+path+"/mbr/"
    os.system(cmd)
    print("Mounting Image 2..."+ start2 +"...")
    cmd = "sudo mount -r "+dest_path+" -o ro,norecovery,loop,offset=$(( "+sector+" * "+start2+")) "+path+"/filesystem/"
    os.system(cmd) 
    print("File System Mounted!")
    print("\nYou can now access it from "+path+"/filesystem\n")
    #os.system("gnome-terminal -e 'bash -c \"ls ~/Desktop/img2; exec bash\"'")

def main():
    while True: 
        options=menu.keys()
        #options.sort()
        for entry in options: 
            print(entry, menu[entry])

        selection=input("\nPlease Select: ") 
        if selection =='1': 
            image() 
            print("Target: "+dest_path+"\n")
        elif selection == '2': 
            mount()
        elif selection == '3':
            generate()
        elif selection == '4':
            clean = input("Do you want to keep the image mounted before you exit? [y/n]")
            if clean.lower() == 'y':
                print("Remember to unmount the image when you are done!")
                break
            elif clean.lower() == 'n':
                print("Exiting~")
                cmd = "sudo umount -q "+path+"/filesystem/"
                os.system(cmd)
                cmd = "sudo umount -q "+path+"/mbr/"
                os.system(cmd)
                cmd = 'sudo rm -rf '+path+'/filesystem/ ' +path+'/mbr/'
                os.system(cmd)
                break
            else:
                print("Unknown Option Selected!") 
        else: 
            print("Unknown Option Selected!") 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        cmd = "sudo umount -q "+path+"/filesystem/"
        os.system(cmd)
        cmd = "sudo umount -q "+path+"/mbr/"
        os.system(cmd)
        cmd = 'sudo rm -rf '+path+'/filesystem/ ' +path+'/mbr/'
        os.system(cmd)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)