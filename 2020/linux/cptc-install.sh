## Direct binary installs
apt update
apt install ftp cadaver snmpenum sqsh default-mysql-client postgresql-client nmap dnsrecon -y --upgrade

## Python Environment
apt install python3.7 python3-pip

## Pentest Framework

git clone https://github.com/trustedsec/ptf.git
echo "modules/intelligence-gathering/sublist3r
modules/intelligence-gathering/gobuster
modules/intelligence-gathering/ssh-audit
modules/intelligence-gathering/linux-exploit-suggester
modules/intelligence-gathering/linuxprivchecker
modules/exploitation/nosqlmap" > ptf/modules/custom_list/cptc.txt
cd ptf
pip install -r requirements.txt
cd ..
git clone https://github.com/maaaaz/nmaptocsv.git
cd nmaptocsv
pip3 install -r requirements.txt
export PATH=$PATH:~/nmaptocsv