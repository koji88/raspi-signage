#!/usr/bin/bash
sudo apt-get install fbi python2 python-setuptools python-dev -y
pushd /tmp
curl -O https://archive.raspberrypi.org/debian/pool/main/o/omxplayer/omxplayer_20190723+gitf543a0d-1+bullseye_armhf.deb
sudo apt install ./omxplayer_20190723+gitf543a0d-1+bullseye_armhf.deb -y
popd
pushd /usr/lib/arm-linux-gnueabihf
sudo curl -sSfLO https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libbrcmEGL.so
sudo curl -sSfLO https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libopenmaxil.so
sudo curl -sSfLO https://raw.githubusercontent.com/raspberrypi/firmware/master/opt/vc/lib/libbrcmGLESv2.so
