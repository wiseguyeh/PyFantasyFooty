import urllib
import sgmllib
import re
import calendar
import datetime

class PlayerParser(sgmllib.SGMLParser):
    "An html parser that can extract player statistics from soccernet.espn.go.com gamelog pages."
    
    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        
class FixtureParser(sgmllib.SGMLParser):
    "An html parser that can extract fixture information from soccernet.espn.go.com fixture pages."
    
    def parse(self, s, year):
        "Parse the given string 's'."
        self.year = year
        self.feed(s)
        self.close()
        

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.inData = False
        self.inMonthHeader = False
        self.fixtureResults = []
        self.pos = 0
        self.currentMonth = None
        self.year = 0
        
    def start_tr(self, attributes):
        self.pos = 0
        self.inMonthHeader = False
        self.inData = False
        for key, value in attributes:
            if key == "class" and value == "colhead":
                self.inMonthHeader = True
            elif key == "class" and "row" in value:
                self.inData = True
        
    def start_td(self, attributes):
        self.pos += 1
        
    def end_tr(self):
        self.pos = 0
            
    def handle_data(self, data):
        if self.inMonthHeader:
            monthAbbr = data[0:3]
            self.currentMonth =  list(calendar.month_abbr).index(monthAbbr)
            self.inMonthHeader = False
        elif self.inData:
            if self.pos == 1:
                #date column data. date example value: 'Sun. 18'
                month = int(data[5:])
                self.fixtureResults.append((datetime.date(self.year, self.currentMonth, month)))

    def get_fixture_results(self):
        return self.fixtureResults
        
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
    
f = urllib.urlopen("http://soccernet.espn.go.com/team/results?id=359&season=2009&cc=5739&_league=all")
s = f.read()
fp = FixtureParser()
fp.parse(s, 2009)


