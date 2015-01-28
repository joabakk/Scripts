import pynmea2 
import re
import time

#variables
windspeed = 1
winddir = 1
boatspeed = 1
rateofturn = 1
vmg = 1
rpm = 1
mag_heading = 1
true_heading = 1

with open("/home/pi/kplexlogs/nmea.log.1", "r") as fo:
#with open("/home/pi/kplexlogs/example.log", "r") as fo:
  
  #for line in fo: #if reading all lines
  #OR:
  N=20
  for i in range(N):
	print "line no: %s" % (i)

	line=fo.next().strip()
        print "Read: %s" % (line) 
	#todo: strip off any timestamp/source tag 
        #split(str="", num=string.count(str))
        #Splits string according to delimiter str (space if not provided) and returns 
        #list of substrings; split into at most num substrings if given
        #http://amsa-code.github.io/risky/ais/cobertura/au.gov.amsa.util.nmea.NmeaMessageParser.html 
        sep = '\\'
	res = line.find(sep, 0, len(line))
	tags = line.split('\\') #looks like \s:log*71\ or \c:1387191186*0E\ or 
        #\s:kplex,c:1387191537*0F\ combined?? print tags
        
	line = tags[-1]#last item in list is nmea sentence
	
	#if re.search('^\$.[A-Z]{5}*\*[0-9A-Fa-f]{2}', line): print "TRUE!!"
	if 1 == 1: #line.count('*') == 1 and re.search(r"$[A-Z]{5} [0-9]*", line):
		try: 
			msg = pynmea2.parse(line)
		except:
			msg = 'foobar'
        	try: 
			print repr(msg)
		except:
			pass
	        #print msg.type 
		try :
		#print msg.sentence_type
			if msg.sentence_type == 'HDM':
				mag_heading = msg.heading
				print "heading M: ", mag_heading
		#print msg.sentence_type
               		elif msg.sentence_type == 'HDT':
                        	true_heading = msg.heading
                        	print "heading T: ", true_heading
 		#print msg.sentence_type
                	elif msg.sentence_type == 'ROT':
				rateofturn = msg.rate_of_turn
				rottime = str(time.time())
                        	print "ROT: ", rateofturn
		#print msg.sentence_type
                	elif msg.sentence_type == 'RPM':
                        	rpm = msg.speed
        	                print "RPM: ", rpm
		#print msg.sentence_type
                	elif msg.sentence_type == 'VPW':
		             	vmg = msg.speed_kn
				vmgtime = str(time.time())
                        	print "VMG: ", vmg
			elif msg.sentence_type == 'MWV':
                                winddir = msg.wind_angle
				windspeed = msg.wind_speed
				winddirtime = str(time.time())
                                print "Wind angle rel: ", winddir
			elif msg.sentence_type == 'VHW':
                                boatspeed = msg.water_speed_knots
				boatspeedtime = str(time.time())
                        #        print "VMG: ", vmg



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

print "Wind Speed: ", windspeed
print "Apparent direction: ", winddir
print "Boat Speed: ", boatspeed
print "ROT: ", rateofturn
print "Velocity made good: ", vmg
print "RPM: ", rpm
print "Heading M: ", mag_heading
print "Heading T: ", true_heading
