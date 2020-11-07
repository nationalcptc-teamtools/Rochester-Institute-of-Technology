#!/bin/bash

#install docker
sudo apt install -y docker.io
sudo systemctl enable docker --now

#install golang
sudo apt install -y golang
#Configure Go
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin/:$GOROOT/bin:$PATH
source .bashrc

#install pip3
sudo apt install python3-pip

#installing git
sudo apt install git-all

#install PTF

#install gobuster
sudo apt install gobuster

#install binwalk
sudo apt install binwalk

#install tmux
sudo apt install tmux
