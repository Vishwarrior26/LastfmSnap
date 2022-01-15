# TODO: Manage imports
from datetime import date, datetime
import datetime
from bs4 import BeautifulSoup
from operator import itemgetter
import pandas as pd
import math
import requests
import re
import unidecode

# TODO: Write class docstring
"""
"""


class scrape:
    # TODO Delete user default?
    def __init__(self, size=50, start="TODAY", end="NONE", user="vishwarrior"):
        """
        Makes a scrape object and sets some default Parameters; Defaults to size of 50 (1 page), start date as current date and end date also as curent date.

        Parameters:
            size (int): Determines the number of entries to be returned per query.
            start (str): Start date for the query in YYYY-MM-DD format.
            end (str): End date for the query in the same format.
            user (str): last.fm user to make the query upon.

        """
        self.setUser(user)
        self.setTime(start, end)
        self.setSize(size)

    def __info(self, type):
        """
        The fundemental function of Scape. Gets information on a given user during the given timeframe.

        Parameters:
            type (str): Type of information wanted, viz. artists, albums, or tracks.

        Returns:
            list: Contains 'size' number of entries about type.

        """
        # Builds first url to scrape for
        self.url = "https://www.last.fm/user/" + self.user + "/library/" + \
            type + "?from=" + self.start + "&to=" + self.end
        urls = [self.url]
        # Calculate the number of pages if size is MAX
        if self.size == "MAX":
            req = requests.get(self.url)
            soup = BeautifulSoup(req.text, "html.parser")
            description = soup.find_all(class_="pagination-page")
            try:
                # Get the last page number
                self.pages = int(re.findall(
                    '[0-9]+', str(description[-1]))[-1])
            except:
                # Else pages is just 1
                self.pages = 1
        # Build the URLS for all the pages needed for the query
        for x in range(2, self.pages + 1):
            urls.append(self.url + "&page=" + str(x))
        info = []
        # Get data from each URL needed
        for tempUrl in urls:
            req = requests.get(tempUrl)
            soup = BeautifulSoup(req.text, "html.parser")
            # Find the list of info on page
            description = soup.find_all("meta", property="og:description")
            if len(description) > 1:
                html = str(description[1])
                # NOTE: Use Regex to find artist that has quotes in it?
                # Deal with finding the list if an artist/album(?)/track(?) name has double quotes; changes from double to single quotes
                if '"Weird Al"' in html:
                    init = html.find("content='") + 9
                    fini = html.find("' property", init + 1)
                else:
                    init = html.find('content="') + 9
                    fini = html.find('" property', init + 1)
                # Create a temporary list of all entries and clean it slightly
                tempInfoList = html[init:fini].split("), ")
                tempInfoList[-1] = tempInfoList[-1][:-1]
                # Create the final info list
                for tempEntry in tempInfoList:
                    # Find the play in each temporary entry
                    play = int(tempEntry.split(" ")[-1][1:])
                    # Get the unsplit un cleaned entries
                    unsplit = tempEntry[:tempEntry.find(str(play)) - 2]
                    if type != 'artists':
                        # Find the album/track for each entry
                        splitter = unsplit.find('—')
                        artist = unsplit[:splitter - 1]
                        type = unsplit[splitter + 2:]
                        # Add the info to the final info list
                        info.append([artist, type, play])
                    else:
                        # Add info to the final info list
                        info.append([unsplit, play])
        # Clean up some of the track titles/artists
        for entry in info:
            entry[0] = entry[0].replace("&quot;", " ").lstrip(' ')
            entry[0] = entry[0].replace("&amp;", "&")
            entry[0] = unidecode.unidecode(entry[0])
            entry[-2] = unidecode.unidecode(entry[-2])
            entry[-2] = entry[-2].replace("&amp;", "&")
            entry[-2] = entry[-2].replace("&quot;", " ").lstrip(' ')
        # Return the number of entries requested
        return info[:self.size]

    def setSize(self, size):
        """
        Sets the number of entries to be returned from a query; if MAX, then all entries in the time period will be returned.

        Parameters:
            size (int): Number of queries to return.

        """
        if size != "MAX":
            self.size = int(size)
            # Finds the number of pages by determing how many 50s are needed to return the given number of entries
            self.pages = int(math.ceil(self.size / 50))

    def __getVeryStart(self):
        """
        Gets the date of the first scrobbles of given last.fm account; used for MAX calculation.

        Returns:
            str: First date of scrobbling on a last.fm account, in YYYY-MM-DD format.

        """
        self.url = "https://www.last.fm/user/" + \
            self.user + "/library/"  # Builds URL to scrape
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all(class_="pagination-page")
        self.url += "?page=" + \
            str(re.findall('[0-9]+', str(description[-1]))[-1]
                )  # Finds last page of last.fm account scrobbles
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        # NOTE: Potential edge case where the first scrobbling date has too many scrobbles so that the date header is on the previous page?
        # Gets all dates on the last scrobble date
        description = soup.find_all(class_="date-heading")
        # Get all the proponents of the last date found on the page
        pieces = str(description[-1])[25:-5].split(" ")
        month = f"{datetime.datetime.strptime(pieces[2], '%B').month:02}"
        day = f"{int(pieces[1]):02}"
        year = pieces[3]
        # Convert date to format to use in scraping
        return year + "-" + month + "-" + day

    def setTime(self, start, end="NONE"):
        """
        Sets the date range which the query is run on; supports some special arguements such as TODAY, which sets the date to the current day, ALL, which finds the earliest day using the getVeryStart() function, and then sets the end to TODAY. If an end isn't given, it defaults to the start date, this is the default value as well.

        Parameters:
            start (str): Start date of timeframe.
            end (str): End date of timeframe.

        """
        self.start = start
        self.end = end
        if start == "TODAY":
            self.start = str(date.today())
        elif start == "ALL" or end == "ALL":
            # Maintain ALL integrity when swapping users; see setUser()
            self.all = True
            self.start = self.__getVeryStart()
            end = "TODAY"
        if end == "NONE":
            self.end = self.start
        elif end == "TODAY":
            self.end = str(date.today())

    def setUser(self, user):
        """
        Sets the last.fm user

        Determines the last.fm user whose information is going to be scraped and then queried.

        Parameters:
            user (str): User to scrape information from.

        """
        self.user = user
        try:
            # Maintain ALL integrity when changing users so that the start date is reset
            if self.all == True:
                self.setTime("ALL", self.end)
        except:
            pass

    def artistInfo(self):
        """ Gets info about artists & their scrobbles. See info() for more details. """
        return self.__info('artists')

    def albumInfo(self):
        """ Gets info about albums, album artists, & their scrobbles. See info() for more details. """
        return self.__info('albums')

    def trackInfo(self):
        """ Gets info about tracks, artists for each track, & their scrobbles. See info() for more details. """
        return self.__info('tracks')
# TODO: Rewrite docstring to be coherent later

    def __artistCountsPerType(self, type):
        """
        Gets the number of albums/tracks which have the same artists.

        Parameters:
            type (function): Function to run to get artist counts; can be albumInfo or trackInfo.

        Returns:
            list: List of total of counts of artists from either albums/tracks in the timeframe.

        """
        artists = []
        # Goes through the info list of each type and then sums the counts of each artist, sorted by count
        for temp in type():
            artist = temp[0]
            if artist not in (row[0] for row in artists):
                artists.append([artist, 1])
            else:
                for row in artists:
                    if row[0] == artist:
                        row[-1] += 1
        return sorted(artists, key=itemgetter(-1), reverse=True)

    def artistCountsPerAlbum(self):
        """ Gets info about artist counts per album, see artistCountsPerType() for more details. """
        return self.__artistCountsPerType(self.albumInfo)

    def artistCountsPerTrack(self):
        """ Gets info about artist counts per track, see artistCountsPerType() for more details. """
        return self.__artistCountsPerType(self.trackInfo)

    def __metaInfo(self, type=""):
        """
        Finds the number of scrobbles or unique artists/albums/tracks.

        Parameters:
            type (str): type of info to get counts. If blank, finds scrobbles over timeframe.
        Returns:
            str: Either the number of scrobbles, or the number of unique artist, albums or tracks in the timeframe.

        """
        self.url = "https://www.last.fm/user/" + self.user + "/library" + type + "?from=" + \
            str(self.start) + "&to=" + str(self.end)
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all(class_="metadata-display")
        if len(description) > 0:
            temp = str(description[0])
            # Gets the info through a regex search for numbers
            self.total = int("".join(str(x) for x in re.findall(
                "[0-9]", temp[temp.find(">") + 1:temp.find("<", 1)])))
            return self.total

    def scrobbleCounts(self):
        """ Get number of scrobbles in timeframe. See metaInfo() for more details. """
        return self.__metaInfo()

    def artistCounts(self):
        """ Get number of unique artists in timeframe. See metaInfo() for more details. """
        return self.__metaInfo("/artists")

    def albumCounts(self):
        """ Get number of unique albums in timeframe. See metaInfo() for more details. """
        return self.__metaInfo("/albums")

    def trackCounts(self):
        """ Get number of unique tracks in timeframe. See metaInfo() for more details. """
        return self.__metaInfo("/tracks")

    def __dailyInfo(self, info):
        """
        Gets info about entries for each day in the sepcified time period, inclusive. Uses info(), so see that for more details.

        Parameters:
            info (function): Type of info to get, either artist, album, or track, using their respective functions.

        Returns:
            list: Information for every date in the timeframe about the requested type.

        """
        results = []
        origStart = self.start
        origEnd = self.end
        # Go through every day in the timeframe
        for day in pd.date_range(start=self.start, end=self.end):
            # Get the date, change it, and then get the information requested
            curday = str(day.date())
            self.setTime(curday)
            # Add the date and the info to the info list
            results.append([curday, info()])
        # Reset the timeframe
        self.setTime(origStart, origEnd)
        return results

    def dailyArtists(self):
        """ Get daily info about artists. """
        return self.__dailyInfo(self.artistInfo)

    def dailyAlbums(self):
        """ Get daily info about albums. """
        return self.__dailyInfo(self.albumInfo)

    def dailyTracks(self):
        """ Get daily info about tracks. """
        return self.__dailyInfo(self.trackInfo)

    def dailyScrobbles(self):
        """ Get daily info about scrobbles. """
        return self.__dailyInfo(self.scrobbleCounts)

    # NOTE: Perhaps copying, sorting, then binary seaching is a viable, more efficient option?
    def __specInfo(self, search, info, index=0):
        """
        Searches for a specific entry in the info list in the given timeframe.

        Parameters:
            serach (str): Item to search for.
            info (str): Where to search for item; artists, albums, tracks, etc.
            index (int): Information to pull from matching results.

        Returns:
            list: List of all matching results.

        """
        results = []
        origSize = self.size
        self.setSize("MAX")
        # Get all info in the timeframe
        for x in info():
            if x[index].lower() == search.lower():
                # Add matching results
                results.append(x)
        self.setSize(origSize)
        if len(results) == 0:
            results.append("No matches found; check spelling and such.")
        return results

    def specArtist(self, artist):
        """ Finds info about the specified artist. """
        return self.__specInfo(artist, self.artistInfo)

    def specAlbum(self, album):
        """ Finds info about the specified album. """
        return self.__specInfo(album, self.albumInfo, -2)

    def specAlbumArtist(self, artist):
        """ Finds info about albums by the specified artist. """
        return self.__specInfo(artist, self.albumInfo)

    def specTrack(self, track):
        """ Finds info about the specified track. """
        return self.__specInfo(track, self.trackInfo, -2)

    def specTrackArtist(self, artist):
        """ Finds info about tracks by the specified artist. """
        return self.__specInfo(artist, self.trackInfo)
