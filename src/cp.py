#!/usr/bin/python

import os
import sys
import tempfile

#TODO:
#CHECK if dest file already exists with os.path.exists(path_to_file)
def file_cp(source, destination):
    #Opening file to copy
    try:
        sourcefile = open(source, "rb")

    except IOError as e:
        print("Error opening source file", strerror(e.errno))
        #exit(e.errno)
        return False

    #Opening file to copy into
    try:
        destfile = open(destination, "wb")

    except IOError as e:
        sourcefile.close()
        print("Error opening source file", strerror(e.errno))
        #exit(e.errno)
        return False

    #Perform copy operation
    try:
        #Using bytearray(stream.read()) works but for very large files it will be an issue
        ctr = 0
        totalwritten = 0
        databytearray = bytearray(0xFFFF) #Create a buffer 65536 bytes = 64 kbytes long
        bytesread = sourcefile.readinto(databytearray)
        while bytesread > 0: #Great, but if the file is small the null 0s trailing will be copied. readinto() returns the number of bytes read
            writtenbytes = destfile.write(databytearray[0:bytesread])
            totalwritten += writtenbytes
            ctr += 1
            bytesread = sourcefile.readinto(databytearray)
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
        sourcefile.close()
        destfile.close()

        return condition #TODO: Test

def writetemplocation(location):
    try:
        fullloc = os.getenv('HOME')+ '/cppy/temploc.txt'
        temporaryfilelocation = open(fullloc, "at")
        temporaryfilelocation.write(location)
        temporaryfilelocation.close()

    except IOError as e:
        print("Error opening source file", strerror(e.errno))
        temporaryfilelocation.close()
        


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
    #writetemplocation(sys.argv[1])


    """ try:
        #tmp = tempfile.NamedTemporaryFile("w+t",delete=False)
        #tmp.name = 'cppysource.tmp'
        #os.environ["TOCOPY"] = 'a' #not possible outside of the execution environment
        
        tmp.write(sys.argv[1])
    except BaseException as e:
        print("Error creating temporary file", strerror(e.errno))
    finally:
        tmp.close() """