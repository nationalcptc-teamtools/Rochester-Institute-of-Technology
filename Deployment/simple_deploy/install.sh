#!/bin/bash

sudo apt-get update -y 

echo "Sleeping for 5 seconds for the dpkg locks."
sleep 5
echo "If something goes wrong, lsof /var/lib/dpkg/lock-frontend | grep dpkg"
sleep 2

# Install packages and repos 
cat packages.txt | xargs sudo apt-get install -y 
for repo in $(cat repo.txt); do reponame=$(echo $repo | cut -d'/' -f2 | cut -d'.' -f1); git clone https://github.com/$repo /opt/$reponame; done
apt-get install -y golang 

wget https://github.com/OJ/gobuster/releases/download/v3.0.1/gobuster-linux-amd64.7z -O /opt/gobuster.7z
7z x /opt/gobuster.7z

echo "Find nmap directory and copy over vulners.nse script"
find / -name "nmap" 2>/dev/null 
echo "Then issue nmap --script-updatedb"
# vulners usage: nmap -p<ports> --script vulners --script-args mincvss=5.0 <target> 

# Downloading basic directory listing dictionary 
wget https://raw.githubusercontent.com/thesp0nge/enchant/master/db/directory-list-2.3-small.txt -O /opt/directory-list-2.3-small.txt
wget https://github.com/thesp0nge/enchant/raw/master/db/directory-list-2.3-medium.txt -O /opt/directory-list-2.3-medium.txt

cp .vimrc ~/.vimrc
