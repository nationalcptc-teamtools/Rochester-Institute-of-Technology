# FlaskMap: A Distributed Framework for NMAP
##### Author: Will Eatherly | will.eatherly@gmail.com

### What is FlaskMap?
FlaskMap is a highly portable NMAP framework designed to cut down on large-scale network discovery times. This is
accomplished through creating a rudimentary distributed framework in python's Flask framework that reduces the scan load 
on any single device. This allows for more scanning to be done in a reduced amount of time with a single source of 
automated control.

### How does it work?

Flaskmap works by utilizing the asynchronous nature of http requests. With devices calling out at different times, the
network allows for commands to be evenly distributed to devices not executing them. Think of it like an asynchronous botnet that works
for your team, not against you.

### File Overview

##### server.py
`server.py` acts as the C2 for the distributed computing system. It distributes commands via `/GET` requests made to it. Requires file named `targets.txt` to be in the same directory, example format for this filel has been included in this repository.

API Functions:

- `/GET`: Allows bots to recieved queue'd commands
- `/PUT`: Allows users to manually enter commands after the server is created
- `/GET/queue/size`: Allows users to observer the size of the queue non-destructively

Dependencies: 

- Flask
- queue
- os

##### slave.py
`slave.py` is the slave handler for commands to be run on other devices. It sends get requests to the server, retrieves commands,
runs them, then sends the results back via authenticated SFTP server. This file requires no interaction from the user beyond startup,
which prompts for the IP of the server and the password for the sftp user.

Dependencies: 

- requests
- time
- datetime
- pytz
- os
- pysftp
