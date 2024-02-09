#!/usr/bin/bash
sudo apt-get install python python-yaml python-setuptools python-pexpect python-requests python-twisted omxplayer fbi -y
sudo python setup.py install
sudo cp -f launcher/raspi-signage-startup.sh /usr/local/bin
grep -q raspi-signage-startup /etc/rc.local || sudo sed -i '/^exit 0$/i /usr/local/bin/raspi-signage-startup.sh' /etc/rc.local
