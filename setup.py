#!/usr/bin/python3
# File name   : setup.py for PIPPY
# Date        : 2020/11/24

import os
import time
import re

curpath = os.path.realpath(__file__)
thisPath = os.path.dirname(curpath)

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

def run_command(command, retries=3):
    for _ in range(retries):
        if os.system(command) == 0:
            return True
    return False

# Update and upgrade system packages
run_command("sudo apt update")
run_command("sudo apt -y dist-upgrade")
run_command("sudo apt clean")

# Upgrade pip
run_command("sudo pip3 install -U pip --break-system-packages")

# Install necessary packages
run_command("sudo apt-get install -y python-dev python3-pip libfreetype6-dev libjpeg-dev build-essential")
run_command("sudo -H pip3 install --upgrade luma.oled --break-system-packages")
run_command("sudo apt-get install -y i2c-tools")
run_command("sudo apt-get install -y python3-smbus")
run_command("sudo pip3 install icm20948 --break-system-packages")
run_command("sudo pip3 install flask --break-system-packages")
run_command("sudo pip3 install flask_cors --break-system-packages")
run_command("sudo pip3 install websockets --break-system-packages")

# Configure system settings
try:
    replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on')
except:
    print('Failed to modify /boot/config.txt for I2C')

try:
    replace_num("/boot/config.txt",'[all]','[all]\ngpu_mem=128')
except:
    print('Failed to modify /boot/config.txt for GPU memory')

try:
    replace_num("/boot/config.txt",'camera_auto_detect=1','#camera_auto_detect=1\nstart_x=1')
except:
    print('Failed to modify /boot/config.txt for camera settings')

# Install OpenCV with retries
if not run_command("sudo pip3 install opencv-contrib-python==3.4.11.45 --break-system-packages"):
    run_command("sudo pip3 install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple opencv-contrib-python==3.4.11.45 --break-system-packages")

# Install numpy dependencies
run_command("sudo apt-get install -y gfortran libopenblas-dev liblapack-dev")

# Uninstall and reinstall numpy with retries
run_command("sudo pip3 uninstall -y numpy --break-system-packages")
if not run_command("sudo pip3 install numpy==1.21 --only-binary=:all: --break-system-packages"):
    # Fallback to source installation if binary fails
    if not run_command("sudo pip3 install numpy==1.21 --break-system-packages"):
        run_command("sudo apt-get install -y python3-numpy")

# Install additional libraries (excluding libjasper-dev)
run_command("sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libatlas-base-dev")
if not run_command("sudo pip3 install imutils zmq pybase64 psutil --break-system-packages"):
    run_command("sudo pip3 install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple imutils zmq pybase64 psutil --break-system-packages")

run_command("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
run_command("sudo pip3 install pi-ina219 --break-system-packages")

# Clone and install create_ap if not already present
if not os.path.exists(os.path.join(thisPath, "../create_ap")):
    run_command("cd " + thisPath + " && cd .. && sudo git clone https://github.com/oblique/create_ap")
    run_command("cd " + thisPath + " && cd .. && cd create_ap && sudo make install")

# Modify rc.local to start the web server on boot
replace_num('/etc/rc.local','exit 0','cd '+thisPath+' && sudo python3 webServer.py &\nexit 0')

print('Completed!')

# Reboot the system
os.system("sudo reboot")