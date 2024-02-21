# --------------------------------------------------
# ARF Gaussian pulse example, (c) MOGLabs 2016-2019
# --------------------------------------------------
from __future__ import print_function
from mogdevice import MOGDevice
import numpy as np

# connect to the device
dev = MOGDevice("10.1.1.45")
print("Device info:", dev.ask("info"))

# construct the pulse
N = 200
X = np.linspace(-2, 2, N)
Y = 30 * (np.exp(-(X ** 2)) - 1)  # -30 to 0dBm

dev.cmd("MODE,1,TSB")  # set CH1 into table mode
dev.cmd("TABLE,ENTRIES,1,0")  # clear existing table
for y in Y:  # upload the entries
    dev.cmd("TABLE,APPEND,1,100,%.2f,0,5" % y)
print(dev.cmd("TABLE,ARM,1"))  # ready for execution
