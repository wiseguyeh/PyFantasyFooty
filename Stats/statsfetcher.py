import urllib
import sgmllib
import re
import calendar
import datetime
from xml.dom.minidom import parse, parseString
from lxml import etree

class Fixture:
    date_played = None
    home_team = ""
    away_team = ""
    home_team_goals = 0  
    away_team_goals = 0
    
    def __str__ (self):
        if self is not None:
            return str(self.home_team) + "(" + str(self.home_team_goals) + ") vs " + str(self.away_team) + "(" + str(self.away_team_goals) + ") @ " + str(self.date_played)
        else:
            return "(Empty)"
    
class Player:
    name = ""
    fixtures_played = []
    
    
    

class PlayerParser(sgmllib.SGMLParser):
    "An html parser that can extract player statistics from soccernet.espn.go.com gamelog pages."
    
    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        
#class FixtureParser(sgmllib.SGMLParser):
    #"An html parser that can extract fixture information from soccernet.espn.go.com fixture pages."
    
    
    #def parse(self, s, year):
        #"Parse the given string 's'."
        #self.year = year
        #self.feed(s)
        #self.close()
        
    #def __init__(self, verbose=0):
        #sgmllib.SGMLParser.__init__(self, verbose)
        #self.inData = False
        #self.inMonthHeader = False
        #self.fixtureResults = []
        #self.tdIndex = 0
        #self.currentMonth = None
        #self.year = 0
        #self.currentFixture = None
        
    #def start_tr(self, attributes):
        #self.tdIndex = 0
        #self.inMonthHeader = False
        #self.inData = False
        #for key, value in attributes:
            #if key == "class" and value == "colhead":
                #self.inMonthHeader = True
            #elif key == "class" and "row" in value:
                #self.inData = True
        
    #def start_td(self, attributes):
        #self.tdIndex += 1
        
    #def end_tr(self):
        #self.tdIndex = 0
            
    #def handle_data(self, data):
        #if data == "\n": #ignore blank data
            #return
        #if self.inMonthHeader:
            ##month/year column data, example value = "Aug. '09". Must fetch the month abreviation and convert that into the numeric month value.
            #monthAbbr = data[0:3]
            #self.currentMonth =  list(calendar.month_abbr).index(monthAbbr)
            #self.inMonthHeader = False
        #elif self.inData:
            #print "handle called (in data)"
            #if self.tdIndex == 1:
                ##date column data, example value: "Sun. 18". Need to extract the day value.
                #day = int(data[5:])
                #self.currentFixture = Fixture()
                #self.currentFixture.date_played = datetime.date(self.year, self.currentMonth, day)
            #elif self.tdIndex == 3:
                ##home team name (get entire string)
                #self.currentFixture.home_team =  data
            ##elif self.tdIndex == 4:
                ###score column data, example value: 4-10. Must get home/away value (home score is leftmost value).
                ##scoreM = re.match("(P<homeScore>[0-9]+) - (P<awayScore>[0-9]+)", data)
                ##self.currentFixture.homeScore = int(scoreM.group("homeScore"))
                ##self.currentFixture.awayScore = int(scoreM.group("awayScore"))

    #def get_fixture_results(self):
        #return self.fixtureResults
        
class TeamParser(sgmllib.SGMLParser):
    "An html parser that can extract lists of players names/ids from soccernet.espn.go.com club pages."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.players = {}
        self.inPlayerLink = False
        self.lastPlayerId = 0
        
    def handle_data(self, data):
        if self.inPlayerLink:
            self.players[self.lastPlayerId] = data
            self.inPlayerLink = False

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."
        for name, value in attributes:
            if name == "href" and re.search('player/_/', value) is not None:
                self.inPlayerLink = True
                self.lastPlayerId  = int(re.search('(?<=id/)[^/]+', value).group(0))

    def get_players(self):
        "Return the list of players."
        return self.players
    
    

#teams = [('http://soccernet.espn.go.com/team?id=359&cc=5739', 'Arsenal'),
#('http://soccernet.espn.go.com/team?id=362&cc=5739', 'Aston Villa'),
#('http://soccernet.espn.go.com/team?id=392&cc=5739', 'Birmingham City'),
#('http://soccernet.espn.go.com/team?id=365&cc=5739', 'Blackburn Rovers'),
#('http://soccernet.espn.go.com/team?id=358&cc=5739', 'Bolton Wanderers'),
#('http://soccernet.espn.go.com/team?id=346&cc=5739', 'Blackpool'),
#('http://soccernet.espn.go.com/team?id=363&cc=5739', 'Chelsea'),
#('http://soccernet.espn.go.com/team?id=368&cc=5739', 'Everton'),
#('http://soccernet.espn.go.com/team?id=370&cc=5739', 'Fulham'),
#('http://soccernet.espn.go.com/team?id=364&cc=5739', 'Liverpool'),
#('http://soccernet.espn.go.com/team?id=382&cc=5739', 'Manchester City'),
#('http://soccernet.espn.go.com/team?id=360&cc=5739', 'Manchester United'),
#('http://soccernet.espn.go.com/team?id=361&cc=5739', 'Newcastle United'),
#('http://soccernet.espn.go.com/team?id=336&cc=5739', 'Stoke City'),
#('http://soccernet.espn.go.com/team?id=366&cc=5739', 'Sunderland'),
#('http://soccernet.espn.go.com/team?id=367&cc=5739', 'Tottenham Hotspur'),
#('http://soccernet.espn.go.com/team?id=371&cc=5739', 'West Ham United'),
#('http://soccernet.espn.go.com/team?id=350&cc=5739', 'Wigan Athletic'),
#('http://soccernet.espn.go.com/team?id=383&cc=5739', 'West Bromwich Albion'),
#('http://soccernet.espn.go.com/team?id=380&cc=5739', 'Wolverhampton Wanderers')]

#for teamUrl, teamName in teams:
    ## read each team page
    #f = urllib.urlopen(teamUrl)
    #s = f.read()
    ## extract out ids and names of players
    #teamParser = TeamParser()
    #teamParser.parse(s)
    #print teamName + ":" 
    #print teamParser.get_players()
    
#f = urllib.urlopen("http://soccernet.espn.go.com/team/results?id=359&season=2009&cc=5739&_league=all")
#s = f.read()
#fp = FixtureParser()
##fp.parse(s, 2009)

#html = etree.HTML(s)
#rows = html.xpath("//table[@class='tablehead']/tr")

#current_month = None
#fixtures = []
#for row in rows:
    #cells = row.xpath("./td")
    #i=0
    #if "class" in row.attrib and "row" in row.attrib["class"]:
        #if re.search("premier league", cells[6].text, re.IGNORECASE): 
            #newFixture = Fixture()
            ##day played cell, example value: "Sun. 18". Need to extract the day value.
            #day = int(cells[0].text[5:])
            #newFixture.date_played = datetime.date(2009, current_month, day)
            ##home team name cell (cell contains <a/> element which home team name)
            #newFixture.home_team = cells[2][0].text
            ##score cell, example value: 4-10. Must get home/away value (home score is leftmost value).
            #score_m = re.search("(?P<home_score>[0-9]+)[^$]*(?P<away_score>[0-9]+)", cells[3].text)
            #newFixture.home_team_goals = int(score_m.group("home_score"))
            #newFixture.away_team_goals = int(score_m.group("away_score"))
            ##away team name cell (cell contains <a/> element which home team name)
            #newFixture.away_team = cells[4][0].text
            #fixtures.append(newFixture)
    #elif "class" in row.attrib and row.attrib["class"] == "colhead":
        ##month/year column data, example value = "Aug. '09". Must fetch the month abreviation and convert that into the numeric month value.
        #monthAbbr = cells[0].text[0:3]
        #current_month = list(calendar.month_abbr).index(monthAbbr)
#print "There are " + str(len(fixtures)) + " fixtures"
#for f in fixtures:
    #print f
    
f = urllib.urlopen("http://soccernet.espn.go.com/players/gamelog?id=14582&season=2007&cc=5739")
s = f.read()
fp = FixtureParser()
#fp.parse(s, 2009)



html = etree.HTML(s)
rows = html.xpath("//table[@class='tablehead']/tr")

players = []
for row in rows:
    cells = row.xpath("./td")
    i=0
    if "class" in row.attrib and "row" in row.attrib["class"]:
        if re.search("premier league", cells[3].text, re.IGNORECASE): 
            newFixture = Fixture()
            #day played cell, example value: "Sun. 18". Need to extract the day value.
            day = int(cells[0].text[5:])
            newFixture.date_played = datetime.date(2009, current_month, day)
            #home team name cell (cell contains <a/> element which home team name)
            newFixture.home_team = cells[2][0].text
            #score cell, example value: 4-10. Must get home/away value (home score is leftmost value).
            score_m = re.search("(?P<home_score>[0-9]+)[^$]*(?P<away_score>[0-9]+)", cells[3].text)
            newFixture.home_team_goals = int(score_m.group("home_score"))
            newFixture.away_team_goals = int(score_m.group("away_score"))
            #away team name cell (cell contains <a/> element which home team name)
            newFixture.away_team = cells[4][0].text
            fixtures.append(newFixture)
print "There are " + str(len(fixtures)) + " fixtures"
for f in fixtures:
    print f
