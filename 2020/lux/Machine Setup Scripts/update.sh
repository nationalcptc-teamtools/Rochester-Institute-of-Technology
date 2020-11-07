echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list
#apt update
apt install nikto -y
apt install cewl -y
apt install w3af -y
apt install sqlmap -y
apt-get install net-tools -y

#ptf requirements
pip install -r /opt/ptf/requirements.txt

#wpscan
cd /opt/wpscan
sudo apt-get install zlib1g-dev -y
gem install wpscan
wpscan --update

#Interlace
cd /opt/Interlace
python3 setup.py install

#SirepRAT - Windows IoT RCE
cd /opt/SirepRAT
pip install -r requirements.txt



