List the raw github url in the pwlisturl.txt file, separated by new lines. This script will download all
password lists into a new directory. PW list files are renamed to their order in the
download list. When running automate.py, this will crack only one type of hash at a time. The names are specified in John the ripper's documentation. 
Automate.py will try to crack the hashes while following the order of the download list. It will also read lists from the directory
that dlpwlist.sh downloads to, so no adjustements to directories needs to be made. The output will be placed in formattedcrackedhashes.txt with the following order:
username, plaintextpw, hashofpw
installjohn.sh installs john the ripper and any prerequisites it might need.
