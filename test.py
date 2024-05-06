import time
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

sleep = time.sleep
fc = FritzConnection(address='192.168.178.1', password='')  # enter password here!

fh = FritzHomeAutomation(fc)  # same here: use existing instance for initialisation
ain = ''  # enter AIN of the switch here
sleep(10)
fh.set_switch(ain, on=True)
sleep(90)
fh.set_switch(ain, on=False)
