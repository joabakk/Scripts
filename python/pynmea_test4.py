import pynmea2
with open("/home/pi/kplexlogs/example.log", "r") as fo:
  for line in fo:
        print "Read: %s" % (line)
        msg = pynmea2.parse(line)
        print repr(msg)
        try:
                print msg.rate_of_turn
        except:
                pass
        try:
                print msg.latitude
        except:
                pass
