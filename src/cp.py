#!/usr/bin/python
#The cp.py module is responsible of saving the location of the file(s) to copy


import os
from os import strerror
import sys
import tempfile

#Writes the path of the file to copy in a temporary file
#In order not to create dependency of Python 3.5+, I have chosen to store the temporary file not in a subdirectory in the home directory
#(which would result me to use python's pathlib to mkdir and thus Python 3.5+), but simply in $HOME
def writetemplocation(location):
    try:
        fullloc = os.getenv('HOME') + '/.cppytemploc.txt'   #TODO: Test on Windows
        print(f"temploc: {fullloc}")
        print(f"location: {location}")
        temporaryfilelocation = open(fullloc, "at")
        temporaryfilelocation.write(location + '\n')
        temporaryfilelocation.close()
    except FileNotFoundError as e:
        print("Could not open temporary file location", strerror(e.errno))
    except IOError as e:
        print("Error opening source file", strerror(e.errno))
        temporaryfilelocation.close()
        

#I'm too new to Python not to utilise my previous, much more elegant dogma
def main():
    #I considered using NamedTemporaryFile but given that I had no elegant way to handle location, I chose to use "my own" temporary file
    if len(sys.argv) - 1 != 1:
        print("Incorrect usage. Specify source file.")
    else:
        try:
            if(os.path.exists(sys.argv[1])):
                writetemplocation(os.path.realpath(sys.argv[1]))
            else:
                raise BaseException("Source file does not exist.")
        except BaseException as e:
            print(e.__str__())

main()