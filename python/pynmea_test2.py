import pynmea2
pty = open("/home/pi/kplexlogs/nmea.log.1")
streamreader = pynmea2.NMEAStreamReader(pty)

while 1:
 for msg in streamreader.next():
  msg
  cont = pynmea2.parse(msg)
print cont
