#This will clone the repo and edit the config. file to install the required tools


#updating sources list
sudo apt-get udpate
echo "-------->>Sources List Updated<<--------"

if [ ! -d "ptf/" ]; then
  git clone https://github.com/trustedsec/ptf.git
fi
echo "-------->>Cloning Repo Complete<<--------"

if [ ! -d "nmaptocsv/" ]; then
  git clone https://github.com/maaaaz/nmaptocsv.git
fi

echo "-------->>Editing Config File<<--------"
sed -i 's+INCLUDE_ONLY_THESE_MODULES=""+INCLUDE_ONLY_THESE_MODULES="modules/exploitation/impacket,modules/exploitation/kerberoast,modules/exploitation/kerbrute,modules/exploitation/mitm6,modules/exploitation/nosqlmap,modules/intelligence-gathering/gobuster,modules/intelligence-gathering/linux-exploit-suggester,modules/intelligence-gathering/linuxprivchecker,modules/intelligence-gathering/msfenum,modules/intelligence-gathering/ntlmrecon,modules/intelligence-gathering/nulllinux,modules/intelligence-gathering/spiderfoot,modules/intelligence-gathering/ssh-audit,modules/intelligence-gathering/sublist3r,modules/intelligence-gathering/windows-exploit-suggester,modules/password-recovery/hashcat,modules/password-recovery/seclist,modules/post-exploitation/bloodhound,modules/post-exploitation/empire,modules/post-exploitation/evilwinrm,modules/post-exploitation/privexchange,modules/powershell/nishang,modules/powershell/powersploit,modules/vulnerability-analysis/rdpscan"+g' ptf/config/ptf.config
sed -i 's+AUTO_UPDATE="ON"+AUTO_UPDATE="OFF"+g' ptf/config/ptf.config

#installing pip & pip3
apt-get install python-pip
apt-get install python3-pip
echo "-------->>Acquired Pip & Pip3<<--------"

echo "-------->>Starting PTF<<--------"
cd ptf/
pip install -r requirements.txt
./ptf << EOF
use modules/install_update_all
yes
yes
yes
yes
yes
EOF

#Update cmd
#sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get dist-upgrade -y && apt-get -q --allow-downgrades --allow-remove-essential --allow-change-held-packages -y install build-essential && sudo apt-get autoremove -y && apt-get autoclean -y && updatedb

:' List of modules added
modules/exploitation/impacket.py,
modules/exploitation/kerberoast.py,
modules/exploitation/kerbrute.py,
modules/exploitation/mitm6.py,
modules/exploitation/nosqlmap.py,
modules/intelligence-gathering/enum4linux.py,
modules/intelligence-gathering/gobuster.py,
modules/intelligence-gathering/linux-exploit-suggester.py,
modules/intelligence-gathering/linuxprivchecker.py,
modules/intelligence-gathering/msfenum.py,
modules/intelligence-gathering/ntlmrecon.py,
modules/intelligence-gathering/nulllinux.py,
modules/intelligence-gathering/spiderfoot.py,
modules/intelligence-gathering/ssh-audit.py,
modules/intelligence-gathering/sublist3r.py,
modules/intelligence-gathering/windows-exploit-suggester.py,
modules/password-recovery/hashcat.py,
modules/password-recovery/seclist.py,
modules/post-exploitation/bloodhound.py,
modules/post-exploitation/empire.py,
modules/post-exploitation/evilwinrm.py,
modules/post-exploitation/privexchange.py,
modules/powershell/nishang.py,
modules/powershell/powersploit.py,
modules/vulnerability-analysis/rdpscan.py'
