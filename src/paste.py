#!/usr/bin/python
#The paste.py module is responsible of getting the location of files to copy and pasting it to the specified location (CWD or otherwise)

from os import strerror
import os
import sys
import tempfile
import hashlib
#TODO: Include the possibily of pasting ALL files copied with an argument (ex. -a)
#TODO: Include the possibily of not removing the contents of the temporary file to allow pasting the files to multiple locations

#Function that copies the file in chunks
#TODO: CHECK if dest file already exists with os.path.exists(path_to_file)
def file_cp(source, destination):
    #Opening file to copy
    try:
        sourcefile = open(source, "rb")

    except IOError as e:
        print("Error opening source file", strerror(e.errno))
        return False

    #Opening file to copy into
    try:
        headtailtuple = headtailsplit(source)
        if headtailtuple[1] == None: #If source file is a folder (i.e. leaf is None) raise an exception
            raise IOError
        else:
            destfile = open(os.path.join(destination, headtailtuple[1]), "wb")  #TODO: Check for possible error on Windows due to '\/'

    except IOError as e:
        sourcefile.close()
        print("Error opening source file", strerror(e.errno))
        return False

    #Perform copy operation
    try:
        bytearraysize = 0xFFFF
        #Using bytearray(stream.read()) works but for very large files it will be an issue
        ctr = 0
        totalwritten = 0
        databytearray = bytearray(bytearraysize) #Create a buffer 65536 bytes = 64 kbytes long

        md5 = hashlib.md5() #Initiate md5 interface
        bytesread = sourcefile.readinto(databytearray)
        while bytesread > 0: #Great, but if the file is small the null 0s trailing will be copied. readinto() returns the number of bytes read
            md5.update(databytearray[0:bytesread]) #md5.update(a); md5.update(b) = md5.update(a+b), <Python 3.11
            writtenbytes = destfile.write(databytearray[0:bytesread])
            totalwritten += writtenbytes
            ctr += 1
            bytesread = sourcefile.readinto(databytearray)

        print(f"{md5.hexdigest()} buffered md5")
        condition = True
    except IOError as e:
        print("I/O Error:", strerror(e.errno))
        condition = False
    except BufferError as e:
        print("Buffer Error:", strerror(e.errno))
        condition = False
    finally:
        print(f"{totalwritten} Bytes copied.")
        print(f"{ctr} buffers used.")
        with open(os.path.join(destination, headtailtuple[1]), "rb") as f:
            md5digest_dest = hashlib.file_digest(f, "md5") #>Python 3.11
        print(f"{md5digest_dest.hexdigest()} destination md5")
        sourcefile.close()
        destfile.close()

        return condition #TODO: Test

#Fetches the next source file location
def fetchnext(delete = True):
    try:
        fullloc = os.getenv('HOME') + '/.cppytemploc.txt'   #TODO: Test on Windows
        temporaryfilelocation = open(fullloc, "r+")
        temporaryfilelocation.seek(0, 0)
        if delete == True:
            nextline = temporaryfilelocation.readline().replace('\n', '') #Cursor is moved to next line
            stream = temporaryfilelocation.readlines() #Read remaining
            temporaryfilelocation.seek(0) #Reset cursor
            for line in stream:
                if nextline not in line:
                    temporaryfilelocation.write(line)
            temporaryfilelocation.truncate()
        else:
            nextline = temporaryfilelocation.readline().replace('\n', '')
            

    except FileNotFoundError as e:
        print("Could not open temporary file location", strerror(e.errno))
    except IOError as e:
        print("Error opening source file", strerror(e.errno))
    finally:
        temporaryfilelocation.close()
        return nextline

#This function splits the full path into head and tail (filename)
def headtailsplit(path):
    head, tail = os.path.split(path)
    return head, tail

#If no argument is specified the file is copied to the CWD and the entry deleted from the temporary file
def main():
    if len(sys.argv) - 1 != 1: #No arguments passed, CWD paste mode
        file_cp(fetchnext(), os.getcwd())
    else: #paste to destination
        pass

main()
