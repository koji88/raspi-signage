# rspi-signage

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

Create yaml file based on [rspi-signage.yml](sample/rspi-signage.yml).

# Launch

~~~
$ sudo rspi-signage -c sample/rspi-signage.yml
~~~
