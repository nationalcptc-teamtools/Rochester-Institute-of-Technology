## -sV (Version detection)
## -n (No DNS resolution)
## -T4 normal time
## -O (Enable OS detection) .
## -F (Fast (limited port) scan) to 100 | should I remove this ?
## -oA output to all formats
nmap --verbose -sV -n -T4 -O -F -oA ${1/"/"/"_"}_os_detect $1
nmaptocsv.py -x ${1/"/"/"_"}_os_detect.xml -o ${1/"/"/"_"}_os_detect.csv -d ','