# --------------------------------------------------
# ARF simple python example, (c) MOGLabs 2016-2019
# --------------------------------------------------
from __future__ import print_function
from mogdevice import MOGDevice

# connect to the device
dev = MOGDevice("10.1.1.23")
# print some information
print("Device info:", dev.ask("info"))

# example command: set frequency
dev.cmd("FREQ,1,100MHz")
# example query: check frequency
print("Freq:", dev.ask("FREQ,1"))
# some queries can return dictionaries
print("Temperatures:", dev.ask_dict("TEMP"))
# other queries respond with binary data
tbl = dev.ask_bin("TABLE,DUMP,1")
print("Binary table:", len(tbl))
# close the connection
dev.close()
