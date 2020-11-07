## -p port ranges 
## -n (No DNS resolution)
## -T4 Timing template normal
## -A (Aggressive scan options) (enables OS detection / version scanning / script scanning / traceroute)
## -oA basename (Output to all formats) .

nmap --verbose -p 1-65535 -n -T4 -A -oA ${1/"/"/"_"}_full_tcp $1
nmaptocsv.py -x ${1/"/"/"_"}_full_tcp.xml -o ${1/"/"/"_"}_full_tcp.csv -d ','