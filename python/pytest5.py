import pynmea2 
with open("/home/pi/kplexlogs/nmea.log.1", "r") as fo:
  N=2000
  for i in range(N):
	print "line no: %s" % (i)
	line=fo.next().strip()
        print "Read: %s" % (line)
        sep = '\\' # \ is used to separate nmea v4 tags from sentence
	res = line.find(sep, 0, len(line))
	tags = line.split('\\') #looks like \s:log*71\ or \c:1387191186*0E\ or 
        #\s:kplex,c:1387191537*0F\ combined?? print tags
        
	line = tags[-1]#last item in list is nmea sentence
	if line[0] == '$' and line[0].count('*') == 1: #is there any point of passing the sentence to pynmea?
		msg = pynmea2.parse(line)
        	print repr(msg) #show all values with name
	        try :
        		#print msg.sentence_type
			      if msg.sentence_type == 'HDM':
				      mag_heading = msg.heading
				      print "heading M: ", mag_heading
   		      elif msg.sentence_type == 'HDT':
      	      true_heading = msg.heading
      	      print "heading T: ", true_heading
    	      elif msg.sentence_type == 'ROT':
      	      rot = msg.rate_of_turn
      	      print "ROT: ", rot
    	      elif msg.sentence_type == 'RPM':
      	      rpm = msg.speed
      	      print "RPM: ", rpm
     	      elif msg.sentence_type == 'VPW':
      	      vmg = msg.speed_kn
      	      print "VMG: ", vmg
		except: 
			pass
#print mag_heading #works, then we have global scope
fo.close
