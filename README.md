# raspi-signage

Digital signage by raspberry pi.

# Target

Raspberry PI and simulated system.

# Installation and setup

## Tested system

Raspberry PI2 and raspbian.

## Install scripts

~~~
$ sudo apt-get install python python-yaml omxplayer fbi
$ sudo python setup.py install
~~~

## Edit configuration file

Create yaml file based on [raspi-signage.yml](sample/raspi-signage.yml).

# Launch

~~~
$ sudo raspi-signage -c sample/raspi-signage.yml
~~~
