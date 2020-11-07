#Edit port numbers as needed
nmap -sCV -T4 -v -p21,22,25,53,161,1433,2049,3306,5432 -oA ${1/"/"/"_"}_specific_port $1