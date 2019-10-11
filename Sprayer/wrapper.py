import subprocess
import csv
import socket 
import sys 


def parse(lines):
    # Parsing data from linenum.sh report... 
    for line in lines:
        
        # Parse OS information 
        if '[-] Kernel information:' in line:
            kernel.append(lines[lines.index(line)+1])
        
        # Parse ip address and netmask 
        if 'inet ' in line:
            ipAddr = line.split('inet')[1].split('netmask')[0].strip()
            netmask = line.split('netmask')[1].split('broadcast')[0].strip()
            ip.append(ipAddr+":"+netmask)

        if 'tcp ' in line or 'tcp6 ' in line:
            tcp.append(line.split()[3]+":"+line.split()[6])

        if 'udp ' in line or 'udp6 ' in line:
            udp.append(line.split()[3]+":"+line.split()[5])
            #print(line)

def main():
    if len(sys.argv) != 2:
        print("[DEBUG] Usage: python3 wrapper.py <linenum.sh_file>")
        exit()

    fd = open(sys.argv[1],'r')
    total = []
    for line in fd:
        total.append(line.strip())

    parse(total)

    print(kernel)
    print(ip)
    print(socket.gethostname())
    print(socket.getfqdn())
    print(tcp)
    print(udp)

if __name__ == '__main__':
    ip = []
    tcp = []
    udp = []
    kernel = []

    main()
        

