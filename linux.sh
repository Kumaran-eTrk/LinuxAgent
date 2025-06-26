#!/usr/bin/bash -i 

# Update package lists (recommended before adding PPAs)
sudo apt update

# Add deadsnakes PPA (replace with 'ppa:deadsnakes/nightly' for nightly builds)
echo "enter" | sudo add-apt-repository ppa:deadsnakes/ppa

# Update package lists again (to reflect changes from the PPA)
sudo apt update -y

# Install desired Python 3.9 packages
sudo apt install python3.9-venv python3.9-dev python3.9-distutils -y

# Install build-essential (outside the PPA for potential compatibility reasons)
sudo apt-get install build-essential -y

echo "Python 3.9 development environment and build-essential installed!"

# create a symbolic link for python 3.9
ls -la /usr/bin/python3
sudo rm /usr/bin/python3
sudo ln -s python3.9 /usr/bin/python3

#To verify python3
python3 --version

#Flameshot is a powerful yet simple to use screenshot software
sudo apt install flameshot -y

#Tesseract is an open-source OCR engine that enables the recognition of text within images
sudo apt install tesseract-ocr -y

#xdotool is a command-line tool for simulating keyboard input and mouse activity in X11
sudo apt install xdotool -y

# Create log foler and log files
sudo mkdir -p /var/log/UserMonitor/ && sudo chmod 777  /var/log/UserMonitor

#Create Virtual Environment
sudo mkdir -p /usr/local/share/usermonitor && sudo chmod -R 777 /usr/local/share/usermonitor
source ~/.bashrc
echo "export monitor=/usr/local/share/usermonitor" >> ~/.bashrc
source ~/.bashrc
echo "this is monitor path:$monitor"
cd $monitor
python3 -m venv .venv
source .venv/bin/activate

#Install pip
sudo apt install python3-pip
pip install --upgrade pip setuptools


#To create a service user agent service files
#To find current user
username=$(id -u -n)
echo "The current user is: $username"
#To check display
display=($DISPLAY)
echo "This current display is: $display"

# File path
file_path="/etc/systemd/system/usermonitor.service"

# Configuration to insert
config="[Unit]
Description=Usermonitor service
After=network.target

[Service]
Environment="DISPLAY=:$display"
Environment=\"XAUTHORITY=$monitor/.Xauthority\"
ExecStart=/bin/bash -c 'source $monitor/.venv/bin/activate && cd $monitor/.venv/bin && python3 agent.py start'
User=$username
Restart=always
PIDFile=/tmp/usermonitor.pid

[Install]
WantedBy=multi-user.target
"

# Check if the file exists, if not, create it
if [ ! -f "$file_path" ]; then
    touch "$file_path"
fi

# Insert the configuration into the file
echo "$config" | sudo tee -a "$file_path" >/dev/null

echo "Configuration inserted into $file_path"

