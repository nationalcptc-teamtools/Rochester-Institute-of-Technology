#!/usr/bin/python

#edited heavily from a script by Matthew C. Jones

import sys
import argparse
import subprocess
import os
import base64
from urllib import unquote

#not sure if dynamic requires jumbo john
#prefix to rename the input file to
formattedPrefix = "adjusted"
#put different types of hashes here
#name of hash refers to arg label input to this script
#JTR_nameofhash refers to the dynamic format for jtr
POSTGRES = "postgres"
JTR_POSTGRES ="'dynamic=md5($p.$s)'"
OPENTRADE = "opentrade"
JTR_OPENTRADE = "'dynamic=sha256($p.$s)'"
#JTR_MYSQL = "'dynamic=sha1(sha1($p))'"

#adjusts the input of the hsahes according to hashtype
def adjustInputFile (inputFile, hashType, constant=""):
    fileToChange = open(inputFile, "r")
    newlyFormattedInput = open(formattedPrefix + inputFile, "w+")
    for line in fileToChange:
        line = line.split(":")
        username = line[0]
        password = line[1]
        if hashType == POSTGRES:
            formattedLine = username + ":" + password[3:].strip() + "$" + username + "\n"
        elif hashType == OPENTRADE:
            #accounts for url encoding, can also comment this out and
            password = unquote(password).decode('utf8')
    	    password = base64.b64decode(password).encode("hex")
    	    print(password)
    	    print(constant)
            formattedLine = username + ":" + password.strip() + "$" + constant + "\n"
        newlyFormattedInput.write(formattedLine)
    fileToChange.close()
    newlyFormattedInput.close()
    return 

#figures out how to adjust input file based on hashtype
def adjustForHashType(hashType, inputFile, constant=""):
    if hashType.lower() == POSTGRES:
        adjustInputFile(inputFile, hashType)
        return JTR_POSTGRES, formattedPrefix + inputFile
    elif hashType.lower() == OPENTRADE:
        adjustInputFile(inputFile, hashType, constant)
        return JTR_OPENTRADE, formattedPrefix + inputFile
    else:
        return hashType, inputFile
        
def main(argv):
    
    #build parser
    parser = argparse.ArgumentParser(description='Runs through several passwordlists')
    parser.add_argument("hashFile", action="store", help="File with hashes")
    parser.add_argument("--hashtype", "--t", action="store", help='hash type')
    parser.add_argument("--constantSalt", action="store", help='constant salt for certain hashes')
    args = parser.parse_args()
    
    #file with hases
    inputfile = args.hashFile
    hashtype = args.hashtype
    constantSalt = args.constantSalt
    #dir with all the pwlists
    wordlistdir = "./pwlists/"
        
    #default to md5
    if hashtype == None:
        hashtype="raw-md5"
    
    if hashtype == OPENTRADE:
    	hashtype, inputfile = adjustForHashType(hashtype, inputfile, constantSalt)
    else:
        hashtype, inputfile = adjustForHashType(hashtype, inputfile)
    
    #open list of urls for naming purposes
    pwList = open("pwlisturl.txt")
    for fileName in os.listdir(wordlistdir):
		#notifies user which list is being used to crack something
        print("Using " + pwList.readline() + " to crack")
        #do the cracking
        print("~/src/john/run/john --wordlist="+wordlistdir + fileName + " --format="+hashtype+" " + inputfile)
        subprocess.Popen("~/src/john/run/john --wordlist="+wordlistdir + fileName + " --format="+hashtype+" " + inputfile, shell=True).wait()
    pwList.close()
    
    print "finished cracking"
    
    #get results from john.pot
    subprocess.Popen("~/src/john/run/john --show --format="+hashtype+ " " + inputfile + "> crackedhashes.txt", shell=True).wait()
    
    #open the file with john.pots results
    pwFile = open("crackedhashes.txt", "rw")
    #uncracked hahses
    hashFile = open(inputfile, "r")
    #file where formatted csv output will go
    newPwFile = open("formattedCrackedPws.txt", "w+")
    
    for line in hashFile:
        #this is opened each time so that it can be matched up with
        #each hash
        pwFile = open("crackedhashes.txt", "r")
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

