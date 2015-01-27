import pynmea2
fo = open("/home/pi/kplexlogs/example.log", "r")
line = fo.readline()
#streamreader = pynmea2.NMEAStreamReader(line)

print "Read: %s" % (line)

msg = pynmea2.parse(line)
print msg
print msg.heading
