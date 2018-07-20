#!/bin/bash

sudo rm librecust-0.0.1.deb 
sudo apt -y purge librecust
sudo dpkg-deb --build librecust-0.0.1/
sudo dpkg -i librecust-0.0.1.deb