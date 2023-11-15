#!/bin/bash
sudo apt-get install git supervisor
sudo git clone https://github.com/DexterInd/GrovePi

sudo cp supervisord.conf /etc/supervisor/supervisord.conf

sudo chmod +x GrovePi/Script/install.sh
cd GrovePi/Script/
sudo sh install.sh
