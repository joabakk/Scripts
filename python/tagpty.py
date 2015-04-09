import pynmea2 
import re
import serial
import time
import MySQLdb
import RPi.GPIO as GPIO
import polar
import operator
import math

#variables

windspeedplus = 0.1
windspeedminus = 0.1
winddirplus = 0.5
winddirminus = 0.5

vmgtime = winddirtime = windspeedtime = boatspeedtime = rottime = 0

txtime = 0
test = 0  #used to test stuff later

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #used to identify if hat is on or not...

#functions

def checksum(nmeadata):
    calc_cksum = reduce(operator.xor, (ord(s) for s in nmeadata), 0)
    return calc_cksum

def read_serial(filename):
    com = None
    while 1:

        if com is None:
          try:
            com = serial.Serial(filename, timeout=5.0)
          except serial.SerialException:
            print('could not connect to %s' % filename)
            time.sleep(5.0)
            continue

        data = com.readline()
        line=data
        tags = line.split('\\') 
        
        """looks like \s:log*71\ or \c:1387191186*0E\ 
        or \s:kplex,c:1387191537*0F\ combined?? print tags"""
    
        line = tags[-1]#last item in list is nmea sentence
        NMEAtag = tags[1] #first item is NMEA tags (combined)
        NMEAtagParts = NMEAtag.split(',')
        #NMEAsource = NMEAtagParts[0][2:]
        NMEAtime = NMEAtagParts[1][2:-3]
        try:
            reader = pynmea2.NMEAStreamReader()
            for msg in reader.next(line):
                try:
                    print(msg)
                    msg = pynmea2.parse(line)
                    print repr(msg)
                    if msg.sentence_type == 'ROT':
                        rateofturn = msg.rate_of_turn
                        if rateofturn != '':
                            rottime = NMEAtime
                            print "ROT: ", rateofturn
                    elif msg.sentence_type == 'RPM':
                        rpm = msg.speed
                        print "RPM: ", rpm
                    elif msg.sentence_type == 'HDM':
                        mag_heading = msg.heading
                        print "heading M: ", mag_heading
                    elif msg.sentence_type == 'HDT':
                        true_heading = msg.heading
                        print "heading T: ", true_heading
                    elif msg.sentence_type == 'VPW':
                        vmg = msg.speed_kn
                        if vmg != '':
                            vmgtime = NMEAtime
                            print "VMG: ", vmg
                    elif msg.sentence_type == 'MWV':
                        if msg.reference == 'R':
                                winddir = msg.wind_angle
                                if winddir != '':
                                    winddirtime = NMEAtime
                                    print "Wind angle rel: ", winddir
                                    if msg.wind_speed_units == 'M':
                                        windspeed = msg.wind_speed
                                        if windspeed != '':
                                            windspeedtime = NMEAtime
                    elif msg.sentence_type == 'VHW':
                        boatspeed = msg.water_speed_knots
                        if boatspeed != '':
                            boatspeedtime = NMEAtime
                    elif msg.sentence_type == 'VWR':
                        winddir = msg.deg_r
                        if winddir != '':
                            winddirtime = NMEAtime
                            windtack = msg.l_r
                            windspeed = msg.wind_speed_ms
                            if windspeed != '':
                                windspeedtime = NMEAtime
                    else:
                        pass
                
                    if test == 1:
                        mintime = 1
                        timediff = 1
                        vmgtime = winddirtime = windspeedtime = boatspeedtime = rottime = NMEAtime = 10
                
                    #print vmgtime, winddirtime, windspeedtime, boatspeedtime, rottime
                    mintime = min(int(vmgtime), int(winddirtime), int(windspeedtime), int(boatspeedtime), int(rottime))
                    maxtime = max(int(vmgtime), int(winddirtime), int(windspeedtime), int(boatspeedtime), int(rottime))
                    timediff = (maxtime - mintime)
                    
                    if test == 1:
                        mintime = 1
                        timediff = 1
                        vmgtime = winddirtime = windspeedtime = boatspeedtime = rottime = NMEAtime
                        windspeed = 9.8
                        winddir = 35
                        boatspeed = 1.2
                        rateofturn = 0
                        vmg = 2
                        windtack = "l"
                        
                    if mintime != 0 and timediff < 2:
                        #less than two seconds since all sentences updates)
                        pbs = polar.polarcheck( windspeed, winddir, boatspeed);
                        print "polar boat speed: ",pbs
                        vmgtime = winddirtime = windspeedtime = boatspeedtime = rottime = 0 
                        
                        if pbs == 0 and (GPIO.input(21)) == 0:#CHECK IF ENGINE OFF
                            print "no items better, adding"
                            #result = polar.polaradd( NMEAtime, windspeed, winddir, boatspeed, rateofturn, vmg, windtack );                            print "result from sql injection: ", result
                        elif pbs != "error":
                            print "not better than alredy logged"
                        else:#error in sql query
                            pass
                    elif mintime != 0 and (max(int(winddirtime), int(windspeedtime), int(boatspeedtime), int(rottime)) - min(int(winddirtime), int(windspeedtime), int(boatspeedtime), int(rottime)) < 2):
                        vmg = boatspeed * math.cos(winddir)
                        pbs = polar.polarcheck( windspeed, winddir, boatspeed);
                        print "polar boat speed: ",pbs
                        vmgtime = winddirtime = windspeedtime = boatspeedtime = rottime = 0 
                        
                        if pbs == 0 and (GPIO.input(21)) == 0:#CHECK IF ENGINE OFF
                            print "no items better, adding"
                            #result = polar.polaradd( NMEAtime, windspeed, winddir, boatspeed, rateofturn, vmg, windtack );                            print "result from sql injection: ", result
                        elif pbs != "error":
                            print "not better than alredy logged"
                        else:#error in sql query
                            pass
                    else:   
                        print "keep calm, carry on"
                        pass
                        
                    if test == 1:
                        txtime = int(NMEAtime) - 1
                        
                    if txtime < NMEAtime:
                            txtime = NMEAtime
                            tbs, tra = polar.findtbs( windspeed, winddir, boatspeed );
                            #print "target boat speed: ", tbs
                            #print "polar boat speed: ", pbs
                            #print "target relative angle: ", tra
                            #print "target speed:",tbs
                            #print "target angle: ", tra

                            tbsmsg = "PSILTBS,{0:1.1f},N" .format(tbs)
                            ck = polar.checksum(tbsmsg)
                            NMEAfullsentence = "$"+str(tbsmsg)+"*"+str(ck)
                            NMEAfullsentence = NMEAfullsentence+'\r\n'
                            com.write(NMEAfullsentence)
                            
                            cfdmsg = "PSILCD1,{0:1.1f},{1:1.1f}" .format(pbs, tra)
                            ck = polar.checksum(cfdmsg)
                            NMEAfullsentence = "$"+str(cfdmsg)+"*"+str(ck)
                            NMEAfullsentence = NMEAfullsentence + '\r\n'
                            com.write(NMEAfullsentence)
                            
                except:
                    pass           
        except:
            pass

filename="/dev/pty23"
try:
    read_serial(filename)
except:
    time.sleep(0.2)
