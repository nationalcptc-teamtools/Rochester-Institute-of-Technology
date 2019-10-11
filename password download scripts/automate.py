#!/usr/bin/python

#edited heavily from a script by Matthew C. Jones

import sys
import argparse
import subprocess
import os

def main(argv):
    
    #build parser
    parser = argparse.ArgumentParser(description='Runs through several passwordlists')
    parser.add_argument("hashFile", action="store", help="File with hashes")
    parser.add_argument("--hashtype", "--t", action="store", help='hash type')
    args = parser.parse_args()
    
    #file with hases
    inputfile = args.hashFile
    hashtype = args.hashtype
    #dir with all the pwlists
    wordlistdir = "./pwlists/"
    
    #default to md5
    if hashtype == None:
        hashtype="raw-md5"
    
    #open list of urls for naming purposes
    pwList = open("pwlisturl.txt")
    for fileName in os.listdir(wordlistdir):
		#notifies user which list is being used to crack something
        print("Using " + pwList.readline() + " to crack")
        #do the cracking
        subprocess.Popen("john --wordlist="+wordlistdir + fileName + " --format="+hashtype+" " + inputfile, shell=True).wait()
    pwList.close()
    
    print "finished cracking"
    
    #get results from john.pot
    subprocess.Popen("john --show --format="+hashtype+" " + inputfile + "> crackedhashes.txt", shell=True).wait()
    
    #open the file with john.pots results
    pwFile = open("crackedhashes.txt", "rw")
    #uncracked hahses
    hashFile = open(inputfile, "r")
    #file where formatted csv output will go
    newPwFile = open("formattedCrackedPws.txt", "r+b")
    
    for line in hashFile:
        #this is opened each time so that it can be matched up with
        #each hash
        pwFile = open("crackedhashes.txt", "rw")
        for pwFileLine in pwFile:
			#check if cracked creds username matches the hashe's username
            if pwFileLine.split(':')[0] == line.split(':')[0]:
				#add to the formatted file
                newLine = pwFileLine.rstrip() + ':' + line
                newLine = newLine.replace(':',',')
                newPwFile.write(newLine)
        pwFile.close()
        
    #close stuff
    pwFile.close()
    hashFile.close()
    newPwFile.close()
	
	#rm intermediate file
    os.system("rm crackedhashes.txt")
    print("Output formatted hashes to formattedCrackedPWs.txt")

if __name__ == "__main__":
    main(sys.argv[1:])

