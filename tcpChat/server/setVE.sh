#!/bin/bash
#pip install
sudo apt-get install python3-pip
pip3 install --upgrade pip

#virtualenv install
sudo pip3 install virtualenv
virtualenv --system-site-packages VE
fi

#requirements instalation
source VE/bin/activate
pip3 install -r requirements.txt
deactivate


