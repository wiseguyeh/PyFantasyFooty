import shelve
import urllib

class YearlyStatsFetcher:
    """
    Provides common methods for fetching and storing yearly football statistical 
    data from web pages.
    
    Implementors are required to override the 3 methods:
    
      __parse_stats_page
      __get_shelf_file_name
      __get_stat_page_urls
    """
    
    __min_year = 2002
    __max_year = 2010
    
    
    def __get_stats(self, year, use_local=True):
        """
        Fetches statistics for a specified year.
        If use_local is True and if they have allready been parsed, the shelved stats for 
        the year will be returned without resorting to fetching & parsing any web pages.
        """
        
        #preconditions
        if year is None or year < self.__min_year or year > self.__max_year:
            raise Exception("Param 'year' must be an integer between " + str(self.__min_year) + " and " + str(self.__max_year))
         #get stats for year (either from parsing web pages or from shelf)
        shelf = shelve.open(self.__get_shelf_file_name())
        stats = None
        if str(year) in shelf and use_local:
            stats = shelf[str(year)]
        else:
            stats = self.__parse_stats(year)
            shelf[str(year)] = stats
            shelf.close()
        return stats
    
    
    def __parse_stats(self, year):
        """
        Parses stats for the specified year.
        Stats are parsed from web pages, specified by the __get_stat_page_urls() method.
        """
        
        stats = []
        for url in self.__get_stat_page_urls(year):
            f = urllib.urlopen(url)
            s = f.read()
            stats.extend(self.__parse_stats_page(s, year, url))
        return stats 
    
    
    def __parse_stats_page(self, html, year, url):
        """
        Must override. Parses a web page's content, extracting statistics from it and returning them.
        """
        return None
        
    def __get_shelf_file_name(self):
        """
        Must override. Returns the name of the file to shelve parsed statistics.
        """
        return ""
    
    def __get_stat_page_urls(self, year):
        """
        Must override. Returns a list of url's that represent pages that hold stats for the given year.
        """
        return []
    
        
        
        