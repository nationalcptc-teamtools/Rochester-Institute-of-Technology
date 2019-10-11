#By Will Eatherly

from flask import Flask
import queue
import os

# global queue that can be used by any function in the application
q = queue.Queue()
app = Flask(__name__)


# Gets the next command. If there are no commands, returns the string "empty"
@app.route('/', methods=['GET'])
def GetJob():
    if q.empty():
        return "empty"
    else:
        return q.get()


# Allows a user to use a PUT request to add a command to the queue in FIFO fashion
@app.route('/<string:command>', methods=['PUT'])
def AddJob(command):
    q.put(command)

# Allows a user to get the queue size
@app.route('/queue/size', methods=['GET'])
def QueueLength():
    return str(q.qsize())


if __name__ == "__main__":

     # Reads in commands from file and puts them in the queue
    # This command makes it so it will search in the local folder, regardless of OS
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'targets.txt')

    # This file is not pre-populated. This will have to be done on the spot
    commands = open(my_file, "r")

    targ = set()

    line = commands.readlines()

    for target in line:
        targ.add(target)

    for i in targ:
        q.put("nmap -p- " + i)
        q.put("nmap -p- -sU " + i)

    # starts the app
    # openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
