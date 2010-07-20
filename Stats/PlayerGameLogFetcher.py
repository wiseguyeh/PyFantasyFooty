import shelve
import urllib
from lxml import etree
import re
import calendar
import datetime
from Teams import teams


class PlayerGame:
    """
    Represents a single game played by a player, recording statistics about thier performance within a game.
    """
    
    player_name = ""
    played_for_team = ""
    fixture = None
    minutes_played = 0
    started = False
    goals = 0
    assists = 0
    shots = 0
    shots_on_goal = 0
    yellow_cards = 0
    red_cards = 0
    fouls_commited = 0
    fouls_suffered = 0
    saves = 0
    offsides = 0

class PlayerGameLogFetcher:
    """
    Retrieves statistics on all players who have played in english leauge games (no cups/european tournaments) for a specified season.
    Games are parsed from the espn game log pages, where urls are of the form: 
    
    http://soccernet.espn.go.com/players/gamelog?id=<player_id>&season=<year>
    
    where <player_id> is a positive integer and <season_year> is the opening year of a season 
    (i.e. the season_year value for the 2009/2010 season would be 2009)
    
    Once all game logs for a specified year have been succesfully parsed, they will be 'shelved'
    """
    
    def get_player_games(self, year, use_local=True):
        """
        Gets statistics about every english leauge game players competed in for the specified year (year must be between 2005 & 2010).
        If use_local is True, then if they exist, the shelved player games for the year will be returned 
        without resorting to re-parsing the fixtures for each team.
        """
        