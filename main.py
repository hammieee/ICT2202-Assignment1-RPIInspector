import pyfiglet
import os
import sys
import datetime
import generatepdf as reportpdf

ascii_banner = pyfiglet.figlet_format("RPI Inspector")
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
    print("\n")
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
        
        while True:
            selection=input("\nReport type:\n\n1. Report activity from all time\n2. Report activity from specific day/period\n3. Back to main menu\n\nPlease select a report type that you wish to generate: ") 
            
            # if generating report for activities from all time
            if selection =='1': 
                # generate reports
                filename="RPIReport_GeneralInfo.pdf"
                reportpdf.generateReportGeneralInfo(path, filename)

                filename="RPIReport_OtherInfo_AllTime.pdf"
                reportpdf.generateReportAllTime(path, filename)

                filename="RPIReport_Syslog_AllTime.pdf"
                reportpdf.generateSyslogAllTime(path, filename)
            
            # if generating report for activities from specific period
            elif selection == '2': 

                try:
                    print("\nIf you want to generate report for a specific day instead of a specific period, you may just put the same date for both start and end date.")
                    startdate=input("\nPlease select a start date of the period [ddmmyyyy]: ") 
                    enddate=input("\nPlease select a end date of the period [ddmmyyyy]: ") 
                    s_d = startdate[:2]
                    s_m = startdate[2:4]
                    s_y = startdate[4:8]
                    e_d = enddate[:2]
                    e_m = enddate[2:4]
                    e_y = enddate[4:8]
                    
                    # check whether the input is convertable to date format
                    startdate = datetime.date(int(s_y),int(s_m),int(s_d))
                    enddate = datetime.date(int(e_y),int(e_m),int(e_d))
                    
                    # check whether the startdate and enddate is valid                    
                    if (startdate > enddate):
                        print("\nPlease enter valid start date and end date.\n")
                        break
                except ValueError:
                    print("\nPlease enter correct date format [ddmmyyyy]\n")
                    break

                # generate reports
                filename="RPIReport_GeneralInfo.pdf"
                reportpdf.generateReportGeneralInfo(path, filename)
                
                if startdate == enddate:
                    filename1="RPIReport_OtherInfo_"+str(startdate)+".pdf"
                    filename2="RPIReport_Syslog_"+str(startdate)+".pdf"
                else:
                    filename1="RPIReport_OtherInfo_"+str(startdate)+"_"+str(enddate)+".pdf"
                    filename2="RPIReport_Syslog_"+str(startdate)+"_"+str(enddate)+".pdf"
                reportpdf.generateReportSpecificPeriod(path, filename1, startdate, enddate)
                reportpdf.generateSyslogSpecificPeriod(path, filename2, startdate, enddate)

            # if back to main menu
            elif selection == '3': 
                print("\n\n")
                break
                
            else:
                print("Unknown Option Selected!") 

    else:
        print('\nPlease mount the file system (option 2) before generating report\n')

def m1(sector,start1):
    cmd = "sudo umount -q "+path+"/filesystem/"
    os.system(cmd)
    print("Mounting Image 1..."+ start1 +"...")
    cmd = "sudo mount -r "+dest_path+" -o loop,offset=$(( "+sector+" * "+start1+")) "+path+"/mbr/"
    print(cmd)
    os.system(cmd) 
    print("MBR Mounted!")
    print("\nYou can now access it from "+path+"/mbr\n")
    
def m2(sector,start2):
    cmd = "sudo umount -q "+path+"/mbr/"
    os.system(cmd)
    print("Mounting Image 2..."+ start2 +"...")
    cmd = "sudo mount -r "+dest_path+" -o ro,norecovery,loop,offset=$(( "+sector+" * "+start2+")) "+path+"/filesystem/"
    os.system(cmd) 
    print("File System Mounted!")
    print("\nYou can now access it from "+path+"/filesystem\n")

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
