#!/bin/bash

mkdir target result yara
chmod 777 target result
sudo apt install python3 python3-pip python3-magic qemu-kvm virt-manager libvirt-bin bridge-utils mongodb npm nginx autoconf
sudo pip3 install -r setup/requirements.txt
