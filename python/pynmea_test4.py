<<<<<<< HEAD
import pynmea2 
with open("/home/pi/kplexlogs/example.log", "r") as fo:
  #for line in fo: #if reading all lines
  N=3
  for i in range(N):
	line=fo.next().strip()
        print "Read: %s" % (line) 
	#todo: strip off any timestamp/source tag 
        #split(str="", num=string.count(str))
        #Splits string according to delimiter str (space if not provided) and returns 
        #list of substrings; split into at most num substrings if given
        #http://amsa-code.github.io/risky/ais/cobertura/au.gov.amsa.util.nmea.NmeaMessageParser.html 
        #if search("\") != None
	#tags = split(line="\") #looks like \s:log*71\ or \c:1387191186*0E\ or 
        #\s:kplex,c:1387191537*0F\ combined?? print tags
        #msg = tags(len)
	msg = pynmea2.parse(line)
        print repr(msg)
        #print msg.type 
	try :
		print msg.sentence_type
		if msg.sentence_type == 'HDM':
			mag_heading = msg.heading
			print "heading M: ", mag_heading
		#print msg.sentence_type
                if msg.sentence_type == 'HDT':
                        true_heading = msg.heading
                        print "heading T: ", true_heading
 		#print msg.sentence_type
                if msg.sentence_type == 'ROT':
                        rot = msg.rate_of_turn
                        print "ROT: ", rot
		#print msg.sentence_type
                if msg.sentence_type == 'RPM':
                        rpm = msg.speed
                        print "RPM: ", rpm
		#print msg.sentence_type
                if msg.sentence_type == 'VPW':
                        vmg = msg.speed_kn
                        print "VMG: ", vmg


	except: 
		pass
	#print msg.sentence 
	#print msg.NMEASentenceType 
	#print msg.cls 
	#print msg.TalkerSentence 
	#try:
        #        print msg.rate_of_turn except: pass try: print msg.latitude except: 
        #        pass
#print mag_heading #works, then we have global scope
fo.close
=======
import pynmea2
with open("/home/pi/kplexlogs/example.log", "r") as fo:
  for line in fo:
        #print "Read: %s" % (line)
        #todo: strip off any timestamp/source tag
        #split(str="", num=string.count(str))
  |     #Splits string according to delimiter str (space if not provided) and returns list of substrings; split into at most num substrings if given
        #http://amsa-code.github.io/risky/ais/cobertura/au.gov.amsa.util.nmea.NmeaMessageParser.html
        #tags = split(line="\") #looks like \s:log*71\ or \c:1387191186*0E\ or \s:kplex,c:1387191537*0F\ combined??
        #print tags
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
>>>>>>> fac3129d0b7f4271481f0ea6240f7c62387f1775
