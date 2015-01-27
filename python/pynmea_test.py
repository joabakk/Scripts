import pynmea2

from pynmea2.stream import NMEAStreamReader

with open('/home/pi/kplexlogs/example.log', 'r') as data_file:
    streamer = NMEAStreamReader(data_file)
    next_data = streamer.next()
    data = []
    while next_data:
        data += next_data
        next_data = streamer(data)

msg = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
print msg
print msg.latitude
