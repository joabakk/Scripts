import pynmea2
pty = open("/home/pi/kplexlogs/example.log")
streamreader = pynmea2.NMEAStreamReader(pty)

while 1:
 for msg in streamreader.next():
  cont = pynmea2.parse(msg)
print cont
