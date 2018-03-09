# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from bs4 import SoupStrainer
import re #regex
import json
import urllib2
import sqlite3

sqlFile = 'example.db' #need to find better path
conn = sqlite3.connect(sqlFile)
c = conn.cursor()

only_a_tags = SoupStrainer("a")
only_class_table = SoupStrainer(id="classes")

#First, find the race and classes
RaceUUID = "fa9760af-4fa1-4f02-b393-18764459ea66" #Faerdern 2017

url = "http://www.manage2sail.com/no/event/" + RaceUUID + "#!/classes"

content = urllib2.urlopen(url).read()
soup = BeautifulSoup(urllib2.urlopen(url), "lxml")
raceName = soup.title.string.rsplit(' ', 1)[0].replace(' ', '_');
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS ''' + raceName + '''
             (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    sailNumber   TEXT UNIQUE ON CONFLICT IGNORE,
    type         TEXT,
    boatName         TEXT,
    skipper      TEXT,
    crew         TEXT,
    yachtClub TEXT,
    startClass  TEXT,
    class       TEXT,
    rating       DOUBLE,
    startTime     TIME,
    course         TEXT)''')

# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
classList = BeautifulSoup(content, "xml", parse_only=only_class_table)
classTable = [];

for row in classList.findAll("tr"):
    s = unicode(row.td); #strip off tags <td>IF</td>
    start = '<td>';
    end = '</td>';
    cn = re.search('%s(.*)%s' % (start, end), s);
    className = 'className';
    if cn:
        className = cn.group(1);

    s = unicode(row.a); #find second uuid .../#!entries\?classId=0dde6075-4c60-4e70-9cc0-d793f245954c"><i...
    start = '/#!entries\?classId=';
    end = '"><i';
    cu = re.search('%s(.*)%s' % (start, end), s);
    classUUID = 'classUUID';
    if cu:
        classUUID = cu.group(1);

    classTable.append([className,classUUID]);
    #print className
    #print classUUID

for row in classTable:
    conn = sqlite3.connect(sqlFile)
    c = conn.cursor()

    #print(row);
    print "http://www.manage2sail.com/api/event/" + RaceUUID + "/regattaentry?regattaId=" + row[1];
    url = "http://www.manage2sail.com/api/event/" + RaceUUID + "/regattaentry?regattaId=" + row[1];
    data = json.load(urllib2.urlopen(url));
    if data.has_key("RegattaName"):
        #print data;
        className = data['RegattaName']
        for boat in data['Entries']:
            boatHcp = boatType = ''
            boatName = boat['BoatName']#.replace("'", "\'")
            if boat.has_key("Hcp"):
                boatHcp = str(boat['Hcp'])
            if boat.has_key("BoatType"):
                boatType = boat['BoatType']#.encode('utf-8')
            print boat['SailNumber'] + ' ' + className + ' ' + boatName
            c.execute("REPLACE INTO " + raceName + "(sailNumber, boatName, rating, type, skipper, crew, yachtClub, class) VALUES (?,?,?,?,?,?,?,?)",(boat['SailNumber'], boatName, boatHcp , boatType, boat['SkipperName'], boat['Crew'], boat['ClubName'], className))


        # Save (commit) the changes
        conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    #http://www.manage2sail.com/api/event/fa9760af-4fa1-4f02-b393-18764459ea66/regattaresult/235f6ec8-94c6-4d17-af8b-0d78abb148ae
