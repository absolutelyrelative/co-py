#!/usr/bin/python

from os import strerror
import sys
import tempfile

try:
    tmp = tempfile.NamedTemporaryFile("w+t",delete=False)
    tmp.name = 'cppysource.tmp'
    print(sys.argv[1])
    tmp.write(sys.argv[1])
except BaseException as e:
    print("Error creating temporary file", strerror(e.errno))