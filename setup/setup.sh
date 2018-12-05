#!/bin/bash

mkdir target result yara
chmod 777 target result
sudo apt install python3 python3-pip qemu-kvm virt-manager libvirt-bin bridge-utils mongodb npm nginx autoconf redis-server
sudo pip3 install -r setup/requirements.txt
