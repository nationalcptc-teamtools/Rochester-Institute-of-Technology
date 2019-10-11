#!/bin/bash
# Ready ?
# Made with love by github.com/m507


echo '
web - install web packages
all - install everything
'

echo -n "What repos? >"
read value

if [[ $value == *"all"* ]]; then gitfile='all_github_repos.txt'; fi
if [[ $value == *"web"* ]]; then gitfile='web_github_repos.txt'; fi

echo -n "What packages? >"
read value

if [[ $value == *"all"* ]]; then packfile='all_packages.txt'; fi
if [[ $value == *"web"* ]]; then packfile='web_packages.txt'; fi

#if [[ $value == *"web"* ]]; then gitfile='all_github_repos.txt'; fi

echo $gitfile
echo $packfile
#
# Loop through $gitfile lines and clone every repo
for repo in $(cat $gitfile); do reponame=$(echo $repo | cut -d'/' -f2 | cut -d'.' -f1); git clone https://github.com/$repo /opt/$reponame; done
# Loop and apt install every line
for package in $(cat $packfile); do apt install -y $package; done




if [[ $value == *"web"* ]];
	then
# Uncomment these line incase of a problem
#sudo killall apt apt-get

# Remove the lock files using the commands
#sudo rm /var/lib/apt/lists/lock
#sudo rm /var/cache/apt/archives/lock
#sudo rm /var/lib/dpkg/lock

# Reconfigure the packages
#sudo dpkg --configure -a
#sudo apt install -f

# Install Golang
sudo apt-get install -y python-software-properties
sudo add-apt-repository ppa:duh/golang
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y git
sudo apt-get install -y golang
sudo apt-get install -y chromium-browser
go get github.com/michenriksen/aquatone


# Install Aquatone
cd /opt
git clone https://github.com/michenriksen/aquatone.git
cd aquatone
sudo bash build.sh
go build
fi

