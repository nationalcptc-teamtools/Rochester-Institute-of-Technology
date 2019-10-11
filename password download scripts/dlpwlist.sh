#!/bin/bash
mkdir pwlists
#counter to rename pwfiles
counter=1
#read through list of pwlist urls
while read pwfile; do
#download the password lists to pwlist directory
	wget $pwfile -P "./pwlists" -O ./pwlists/$counter
	let counter=counter+1
done < pwlisturl.txt	

#wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt
