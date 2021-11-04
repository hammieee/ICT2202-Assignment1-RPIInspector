import subprocess
import datetime
from fpdf import FPDF

class PDF(FPDF):
    def reporttitle(self,title):
        self.set_font('Arial', 'BU', 18) # Arial bold underline 18
        self.cell(0, 20, txt = title, ln = 20, align = 'C')	# witdh=0, height=20, text=text, border=0/1, position-next-cell, alignment=C/L/R
        
    def description(self,title):
        self.set_font('Arial', 'B', 11)
        self.cell(0, 0, txt = title, ln = 20, align = 'C')
        
    def subheader(self,title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, txt = title, ln = 20, align = 'L')
        
    def subheader2(self,title):
        self.set_font('Arial', 'B', 11)
        self.cell(0, 10, txt = title, ln = 20, align = 'L')
        
    def sourcepath(self,content):
        self.set_font('Arial', '', 10)
        self.cell(0, 10, txt = "Source(s): " + content, ln = 20, align = 'L')
        
    def contentinbox(self,content):
        self.set_font('Arial', '', 9)
        if len(content) == 0:
            self.multi_cell(189, 5, "Nothing found.", 1, 1)
        else:
            self.multi_cell(189, 5, content, 1, 1)
    
    def normaltext(self,content):
        self.set_font('Arial', '', 10)
        self.cell(0, 5, txt = content, ln = 20, align = 'L')
        
    def linebreak(self):
        self.cell(0, 10, txt = "", ln = 20, align = 'L')

    def footer(self):
        self.set_y(-15)	# 15mm from bottom
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# ----------------------------- function related to generating report about general info --------------------------------------

def generateReportGeneralInfo(path, filename):

    print("\nGenerating report " + filename + " now...\n")

    # instantiate PDF object
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # set report title
    pdf.reporttitle("RPI Report about General Information")

    pdf.subheader("System Information")
    pdf.sourcepath("/etc/hostname, /etc/os-release, /etc/timezone")
    output1 = subprocess.run(['cat', path+'/filesystem/etc/hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    output2 = subprocess.run(['cat', path+'/filesystem/etc/os-release'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    output3 = subprocess.run(['cat', path+'/filesystem/etc/timezone'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox('HOSTNAME='+ output1 + output2 + 'TIMEZONE='+ output3)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("Network Configuration")
    pdf.subheader2("Access Point Information")
    pdf.sourcepath("/etc/wpa_supplicant/wpa_supplicant.conf")
    output = subprocess.run(['cat', path+'/filesystem/etc/wpa_supplicant/wpa_supplicant.conf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("Static or Dynamic IP Address Configurations")
    pdf.sourcepath("/etc/dhcpcd.conf")
    output = subprocess.run(['cat', path+'/filesystem/etc/dhcpcd.conf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("DNS Server Information")
    pdf.sourcepath("/etc/resolv.conf")
    output = subprocess.run(['cat', path+'/filesystem/etc/resolv.conf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("User and Groups Details")
    pdf.subheader2("Users")
    pdf.sourcepath("/etc/passwd")
    output = subprocess.run(['cat', path+'/filesystem/etc/passwd'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("User Password Hash")
    pdf.sourcepath("/etc/shadow")
    output = subprocess.run(['sudo','cat', path+'/filesystem/etc/shadow'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("User Groups")
    pdf.sourcepath("/etc/group")
    output = subprocess.run(['sudo','cat', path+'/filesystem/etc/group'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("Sudo Permissions")
    pdf.sourcepath("/etc/sudoers")
    output = subprocess.run(['sudo','cat', path+'/filesystem/etc/sudoers'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("User Activity - Bash History")
    pdf.sourcepath("/home/pi/.bash_history")
    output = subprocess.run(['cat', path+'/filesystem/home/pi/.bash_history'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    
    pdf.subheader("Services")
    pdf.sourcepath("/etc/services")
    output = subprocess.run(['cat', path+'/filesystem/etc/services'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    
    # generate report in PDF
    pdf.output(filename, 'F')
    print(filename + " is generated in " + path + " directory.")


# --------------------------- function related to generating report activity from all time ------------------------------------

def generateReportAllTime(path, filename):

    print("\nGenerating report " + filename + " now...\n")

    # instantiate PDF object
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # set report title
    pdf.reporttitle("RPI Report about Other Information")
    pdf.description("(Date: All Time)")
    pdf.linebreak()

    pdf.subheader("Authentication")
    pdf.subheader2("Login and Logout Records")
    pdf.sourcepath("/var/log/wtmp")
    output = subprocess.run(['utmpdump', path+'/filesystem/var/log/wtmp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("Failed Login Records")
    pdf.sourcepath("/var/log/btmp")
    output = subprocess.run(['sudo', 'utmpdump', path+'/filesystem/var/log/btmp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("SSH Authentication Logs")
    pdf.sourcepath("/var/log/auth.log*")
    filepath=path +"/filesystem/var/log/auth.log*"
    cmd="sudo zcat -f `ls -tr "+filepath+"`"
    output,error = subprocess.Popen(cmd, shell=True,universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("Package History")
    pdf.sourcepath("/var/log/apt/history.log")
    output = subprocess.run(['cat', path+'/filesystem/var/log/apt/history.log'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("Mail Logs")
    pdf.sourcepath("/var/log/mail.log*")
    filepath=path +"/filesystem/var/log/mail.log*"
    cmd="sudo zcat -f `ls -tr "+filepath+"`"
    output,error = subprocess.Popen(cmd, shell=True,universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    pdf.contentinbox(output)
    pdf.linebreak()
    
    # generate report in PDF
    pdf.output(filename, 'F')
    print(filename + " is generated in " + path + " directory.")
    
def generateSyslogAllTime(path, filename):

    print("\nGenerating syslog report " + filename + " now...\n")

    # instantiate PDF object
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # set report title
    pdf.reporttitle("RPI Syslog Report")
    pdf.description("(Date: All Time)")
    pdf.linebreak()

    pdf.subheader("Syslog")
    pdf.sourcepath("/var/log/syslog*")
    filepath=path +"/filesystem/var/log/syslog*"
    cmd="sudo zcat -f `ls -tr "+filepath+"`"
    output,error = subprocess.Popen(cmd, shell=True,universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    # generate report in PDF
    pdf.output(filename, 'F')
    print(filename + " is generated in " + path + " directory.")

# ------------------------ functions related to generating report activity from specific day/period ---------------------------------

def subprocessCatGrep(startdate,enddate,cmd1):
    alloutput=""
    day_delta = datetime.timedelta(days=1)
    cmd2 = ""
    while startdate <= enddate:		
        # define cmd2
        cmd2 = ["grep", str(startdate)]
        # run command
        process = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        output = subprocess.run(cmd2, stdin=process.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')    
        process.wait()
        alloutput += output	  # store all command output generated from this loop
        startdate += day_delta    # increase day by 1
        #print("startdate in loop increased: ",startdate)	# debug purpose
    return alloutput

def subprocessFileActivity(path,pdf,activitytype,startdate,enddate,cmdoption):
    if startdate == enddate:
        pdf.subheader2("File "+activitytype+" on "+str(startdate))
    else:
        pdf.subheader2("File "+activitytype+" from "+str(startdate)+" to "+str(enddate))
    if activitytype == "Metadata Changed":
        pdf.normaltext("The changes on metadata can either refer to the file is newly created or refer to the changes on the metadata of an")
        pdf.normaltext("existing file (e.g. file permission).")
    cmd = ["sudo", "find", path+"/filesystem","-type","f",cmdoption,str(startdate),"!",cmdoption,str(enddate+datetime.timedelta(days=1))]
    output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    if len(output)!=0:
        output=output.replace(path+"/filesystem","")
    return output

def subprocessZcat(startdate,enddate,filepath):
    alloutput=""
    day_delta = datetime.timedelta(days=1)
    output=""
    while startdate <= enddate:     
        if startdate.strftime('%d')[:1] == '0' :
            dateformat=startdate.strftime('%b')+"  "+format(int(startdate.strftime('%d')),'01d')
        else:
            dateformat=startdate.strftime('%b')+" "+startdate.strftime('%d')
        cmd="sudo zcat -f `ls -tr "+filepath+"` | grep -a " + "\"^"+dateformat+"\""
        output,error = subprocess.Popen(cmd, shell=True,universal_newlines=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        alloutput += output	# store all command output generated from this loop
        startdate += day_delta	# increase day by 1
        #print("startdate in loop increased: ",startdate)	# debug purpose
    return alloutput

def generateReportSpecificPeriod(path, filename, startdate, enddate):

    print("\nGenerating report " + filename + " now...\n")

    # instantiate PDF object
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # set report title
    pdf.reporttitle("RPI Report about Other Information")
    if startdate == enddate:
        pdf.description("(Date: "+str(startdate)+")")
    else:
        pdf.description("(Date: "+str(startdate)+" to "+str(enddate)+")")
    pdf.linebreak()
    
    pdf.subheader("Authentication")
    pdf.subheader2("Login and Logout Records")
    pdf.sourcepath("/var/log/wtmp")
    output = subprocessCatGrep(startdate,enddate,["utmpdump", path +"/filesystem/var/log/wtmp"])
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("Failed Login Records")
    pdf.sourcepath("/var/log/btmp")
    output = subprocessCatGrep(startdate,enddate,["sudo","utmpdump", path +"/filesystem/var/log/btmp"])
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    pdf.subheader2("SSH Authentication Logs")
    pdf.sourcepath("/var/log/auth.log*")
    output=subprocessZcat(startdate,enddate,path +"/filesystem/var/log/auth.log*")    
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    pdf.subheader("Package History")
    pdf.sourcepath("/var/log/apt/history.log")
    day_delta = datetime.timedelta(days=1)
    tmpstartdate = startdate
    alloutput=""
    while startdate <= enddate:	
        cmd=["sed", "-n", "/"+str(startdate)+"/,/"+str(startdate)+"/p",path +"/filesystem/var/log/apt/history.log"]
        output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
        alloutput += output	  # store all command output generated from this loop
        startdate += day_delta    # increase day by 1
        #print("startdate in loop increased: ",startdate)	# debug purpose
    # the sed command has removed the blank line between the paragraphs, which makes the output less organised
    # therefore, the output will be formatted to add back the removed blank lines so that it is easier for user to read the report
    if len(alloutput)!=0:
        unformatted = alloutput.split("\n")
        alloutput = ""
        for i in unformatted:
            if i.startswith("End-Date:"):
                alloutput+=i+"\n\n"
            else:
                alloutput+=i+"\n"
    pdf.contentinbox(alloutput)
    pdf.linebreak()
    startdate = tmpstartdate	# revert startdate back to original 
    #print(alloutput)		# debug purpose

    pdf.subheader("File Activity")
    output = subprocessFileActivity(path,pdf,"Accessed",startdate,enddate,"-newerat")
    pdf.contentinbox(output)
    pdf.linebreak()		
    #print(output)		# debug purpose
    output = subprocessFileActivity(path,pdf,"Modified",startdate,enddate,"-newermt")
    pdf.contentinbox(output)
    pdf.linebreak()		
    #print(output)		# debug purpose
    output = subprocessFileActivity(path,pdf,"Metadata Changed",startdate,enddate,"-newerct")
    pdf.contentinbox(output)
    pdf.linebreak()		
    #print(output)		# debug purpose

    pdf.subheader("Mail Logs")
    pdf.sourcepath("/var/log/mail.log*")
    output=subprocessZcat(startdate, enddate, path +"/filesystem/var/log/mail.log*")
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose
    
    # generate report in PDF
    pdf.output(filename, 'F')
    print(filename + " is generated in " + path + " directory.")
    
def generateSyslogSpecificPeriod(path, filename, startdate, enddate):

    print("\nGenerating syslog report " + filename + " now...\n")

    # instantiate PDF object
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    # set report title
    pdf.reporttitle("RPI Syslog Report")
    if startdate == enddate:
        pdf.description("(Date: "+str(startdate)+")")
    else:
        pdf.description("(Date: "+str(startdate)+" to "+str(enddate)+")")
    pdf.linebreak()

    pdf.subheader("Syslog")
    pdf.sourcepath("/var/log/syslog*")
    output=subprocessZcat(startdate,enddate,path +"/filesystem/var/log/syslog*")
    pdf.contentinbox(output)
    pdf.linebreak()
    #print(output)		# debug purpose

    # generate report in PDF
    pdf.output(filename, 'F')
    print(filename + " is generated in " + path + " directory.")
