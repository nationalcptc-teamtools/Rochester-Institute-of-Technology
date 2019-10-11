#!/bin/bash
# Ready ?
# Made with love by github.com/m507


echo 'This script takes two paramters, $1 is hosts.txt file, and $2 is where the outputs will be saved'

# $1 = hosts.txt should have a list of ips or domains
#
#	Usege: ./start.sh hosts.txt cptc-dir1
#
#

# Set parameters
[ -z "$1" ] && hosts='hosts.txt' || hosts=$1
[ -z "$2" ] && sfile='Aquatone-files' || sfile=$2

# Create a dir
mkdir $sfile

# Run aquatone
cat $hosts | /opt/aquatone/aquatone -ports large -out $sfile
# This /\ will create a file called aquatone_urls.txt inside aquatone.out which will have all valid url that nikto can use.

# Pre scan
mkdir -p $sfile/nikto

# For every url scan for the basic problems
for line in $(cat $sfile/aquatone_urls.txt);

	do
		# Fix slashes
		line=$(echo $line | cut -d/ -f 3)
		# Save using tee so you can see the results while sacning
		nikto -h $line | tee $sfile/nikto/$line.out	&
	done


# Downlaod directory-list-2.3-small.txt if it does not exist
FILE=/opt/dirsearch/directory-list-2.3-small.txt
if [ -f "$FILE" ]; then
    echo "$FILE exist"
else
	mkdir -p /opt/dirsearch/;wget http://acacha.org/~sergi/wordlists/dirbuster/directory-list-2.3-small.txt -O $FILE
fi


# Scan urls
for line in $(cat $sfile/aquatone_urls.txt);

        do
                # Fix slashes
                line=$(echo $line | cut -d/ -f 3)

		# Scan using /opt/dirsearch/directory-list-2.3-small.txt
		/opt/dirsearch/dirsearch.py -w /opt/dirsearch/directory-list-2.3-small.txt -e txt,html,php -f -t 5 -u $ip &
	done

