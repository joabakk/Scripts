import pynmea2
with open("/home/pi/kplexlogs/example.log", "r") as fo:
  for line in fo:
        #print "Read: %s" % (line)
        #todo: strip off any timestamp/source tag
        msg = pynmea2.parse(line)
        print repr(msg)
        #print msg.type
        #print msg.sentence_type
        #print msg.sentence
        #print msg.NMEASentenceType
        #print msg.cls
        #print msg.TalkerSentence
        #try:
        #        print msg.rate_of_turn
        #except:
        #        pass
        #try:
        #        print msg.latitude
        #except:
        #        pass
