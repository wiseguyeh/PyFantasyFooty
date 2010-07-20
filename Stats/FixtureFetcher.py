import calendar
from lxml import etree
import re
import datetime
from Teams import teams
import YearlyStatsFetcher

class Fixture:
    """
    Represents a game played in the premier league.
    """
    
    date_played = None
    home_team = ""
    away_team = ""
    home_team_goals = 0  
    away_team_goals = 0
    league = ""
    
    def __str__ (self):
        if self is not None:
            return str(self.home_team) + "(" + str(self.home_team_goals) + ") vs " + str(self.away_team) + "(" + str(self.away_team_goals) + ") @ " + str(self.date_played) + " in the " + self.league
        else:
            return "(Empty)"


class FixtureFetcher(YearlyStatsFetcher.YearlyStatsFetcher):
    """
    Retrieves a list of leauge fixtures (no cups/european tournaments) for the specified season.
    Fixtures are parsed from the espn fixtures pages, where urls are of the form: 
    
    http://soccernet.espn.go.com/team/results?id=<team_id>&season=<season_year>
    
    where <team_id> is a positive integer and <season_year> is the opening year of a season 
    (i.e. the season_year value for the 2009/2010 season would be 2009)
    
    Once all fixtures for a specified year have been succesfully parsed, they will be 'shelved'
    """
    
    
    def get_fixtures(self, year, use_local=True):
        """
        Gets all premier league fixtures for the specified year (year must be between 2005 & 2010).
        If use_local is True, then if they exist, the shelved fixtures for the year will be returned 
        without resorting to re-parsing the fixtures for each team.
        """
        
        return self._YearlyStatsFetcher__get_stats(year, use_local)
        
    
    def _YearlyStatsFetcher__get_stat_page_urls(self, year):
        urls = []
        for team in teams:
            team_id = team[0]
            urls.append("http://soccernet.espn.go.com/team/results?id=" + str(team_id) + "&season=" + str(year))
        return urls
           
    
    def _YearlyStatsFetcher__get_shelf_file_name(self):
        return "fixtures.shelf"
            
    
    def _YearlyStatsFetcher__parse_stats_page(self, html, year, url):
        """ Parses the html of a espn fixture page, returning all league fixtures on the page """
        
        print "Parsing url: " + url
        dom = etree.HTML(html)
        rows = dom .xpath("//table[@class='tablehead']/tr")
        
        current_month = None
        fixtures = []
        for row in rows:
            cells = row.xpath("./td")
            if "class" in row.attrib and "row" in row.attrib["class"]:
                #home_team_id = int(re.search("(?<=id=)[0-9]{2,4}", cells[2][0].attrib["href"]).group())
                
                competition = cells[6].text
                is_english_leauge = re.search("league", competition, re.IGNORECASE) and re.search("english", competition, re.IGNORECASE)
                status = cells[1].text
                if is_english_leauge and status == None: 
                    newFixture = Fixture()
                    #day played cell, example value: "Sun. 18". Need to extract the day value.
                    day = int(cells[0].text[5:])
                    #if the game was played before june, it is in the later year part of the season
                    newFixture.date_played = datetime.date(year if current_month > 6 else year + 1, current_month, day)
                    #home team name cell (cell contains <a/> element which home team name)
                    newFixture.home_team = cells[2][0].text
                    #score cell, example value: 4-10. Must get home/away value (home score is leftmost value).
                    score_m = re.search("(?P<home_score>[0-9]+)[^$]*(?P<away_score>[0-9]+)", cells[3].text)
                    newFixture.home_team_goals = int(score_m.group("home_score"))
                    newFixture.away_team_goals = int(score_m.group("away_score"))
                    #away team name cell (cell contains <a/> element which home team name)
                    newFixture.away_team = cells[4][0].text
                    newFixture.league = competition
                    fixtures.append(newFixture)
            elif "class" in row.attrib and row.attrib["class"] == "colhead":
                #month/year column data, example value = "Aug. '09". Must fetch the month abreviation and convert that into the numeric month value.
                monthAbbr = cells[0].text[0:3]
                current_month = list(calendar.month_abbr).index(monthAbbr)
        return fixtures
    
                
fp = FixtureFetcher()
fixtures = fp.get_fixtures(2005, False)
print "There are %(count)d fixtures" % {"count" : len(fixtures)}
fixtures = sorted(fixtures, lambda x, y: cmp(x.home_team, y.home_team))
i = 0
team_fixture_count = dict( [(f.home_team, 0) for f in fixtures])
print team_fixture_count
for f in fixtures:
    print "#" + str(i) + " : " + str(f)
    team_fixture_count[f.home_team] =  team_fixture_count[f.home_team] + 1
    i += 1
    
print team_fixture_count


    