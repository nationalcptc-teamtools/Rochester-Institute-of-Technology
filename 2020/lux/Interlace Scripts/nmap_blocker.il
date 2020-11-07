_block:nmap
mkdir -p target/_target_/nmap
sudo chmod +777 target/_target_
nmap _target_ --top-ports 100 -oA target/_target_/nmap/_target_-nmap-top-ports
nmap _target_ -sC -sV -oA target/_target_/nmap/_target_-nmap-service-scan
nmap _target_ -p- -oA target/_target_/nmap/_target_-nmap-port-scan
nmap _target_ -sUV -F -oA target/_target_/nmap/_target_-nmap-UDP-scan
_block:nmap_
