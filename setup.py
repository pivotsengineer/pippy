#!/usr/bin/python3

import os

def replace_num(file, initial, new_num):
    newline = ""
    str_num = str(new_num)
    with open(file, "r") as f:
        for line in f.readlines():
            if line.find(initial) == 0:
                line = (str_num + '\n')
            newline += line
    with open(file, "w") as f:
        f.writelines(newline)

def run_command(command, retries=3):
    for _ in range(retries):
        if os.system(command) == 0:
            return True
    return False

run_command("sudo apt update")
run_command("sudo apt -y dist-upgrade")
run_command("sudo apt clean")
run_command("sudo pip3 install -U pip --break-system-packages")

# Install dependencies required for building numpy
run_command("sudo apt-get install -y python3-dev python3-pip build-essential gfortran libopenblas-dev liblapack-dev libatlas-base-dev")

# Install numpy using pre-built binary wheels, avoiding source builds
run_command("sudo pip3 install numpy==1.22.4 --only-binary=:all: --break-system-packages")

# Install additional dependencies
run_command("sudo apt-get install -y i2c-tools python3-smbus libfreetype6-dev libjpeg-dev")
run_command("sudo pip3 install opencv-contrib-python==3.4.11.45 --break-system-packages")
run_command("sudo apt-get -y install libhdf5-dev libhdf5-serial-dev util-linux procps hostapd iproute2 iw haveged dnsmasq")
run_command("sudo pip3 install pi-ina219 imutils zmq pybase64 psutil --break-system-packages")

# Clone and install create_ap if not already installed
if not os.path.exists(os.path.join(os.path.dirname(__file__), "../create_ap")):
    run_command("cd .. && sudo git clone https://github.com/oblique/create_ap && cd create_ap && sudo make install")

# Modify rc.local to start the server at boot
replace_num('/etc/rc.local', 'exit 0', 'cd ' + os.path.dirname(__file__) + ' && sudo python3 webServer.py &\nexit 0')

# Reboot the system after installation
os.system("sudo reboot")
