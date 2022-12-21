#!/usr/bin/python

from os import strerror
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

if len(sys.argv) != 1:
    print("Incorrect usage. Specify source file.")
else:
    #tmp = tempfile.NamedTemporaryFile("w+t",delete=False)
    #sys.argv[i]