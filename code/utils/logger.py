__author__ = 'Marcelo d\'Almeida'

#http://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-both-file-and-console-with-scripting

import sys
import os

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout

        newpath = './info/log/'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        self.log = open("info/log/logfile.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

