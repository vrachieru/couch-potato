from pytvdbapi import api
from icalendar import Calendar, Event, Timezone
from datetime  import datetime, timedelta

tvdb  = api.TVDB("B43FF87DE395DF56")

shows = [
  "American Dad",
  "Brickleberry",
  "Family Guy",
  "Futurama",
  "Game of Thrones",
  "Hannibal",
  "Narcos",
  "Sherlock",
  "South Park",
  "Vikings"
]

class DateUtil:
  @staticmethod
  def getNextDay(date):
    return date + timedelta(days = 1)


class Show:
  show = None
  episodes = []

  def __init__(self, showName):
    self.getShowByName(showName)
    self.parseEpisodes()

  def getShowByName(self, showName):
    self.show = tvdb.search(showName, "en")[0]

  def parseEpisodes(self):
    self.displayName()
    for season in self.show: 
      for episode in season:
       if episode.FirstAired:
          self.displayEpisode(episode)
          self.episodes.append(ShowEvent(self.show, episode))

  def displayName(self):
    print "\n%s" % self.show.SeriesName

  def displayEpisode(self, episode):
    print "%s S%02dE%02d - %s" % (DateUtil.getNextDay(episode.FirstAired), episode.SeasonNumber, episode.EpisodeNumber, episode.EpisodeName)


class ShowEvent:
  event = None

  def __init__(self, show, episode):
    self.event = Event()
    self.event.add("summary", self.getSummary(show, episode))
    self.event.add("description", self.getDescription(episode))
    self.event.add("dtstart", self.getDate(episode))
    self.event.add("dtend", DateUtil.getNextDay(self.event['DTSTART'].dt))
    self.event.add("dtstamp", datetime.now())
    self.event["uid"] = self.getUid(self.event['DTSTART'].dt, str(self.event['SUMMARY']))

  def getSummary(self, show, episode):
    return "%s S%02dE%02d" % (show.SeriesName, episode.SeasonNumber, episode.EpisodeNumber)

  def getDescription(self, episode):
    return "%s\n%s" % (episode.EpisodeName, episode.Overview)

  def getDate(self, episode):
    return DateUtil.getNextDay(episode.FirstAired)

  def getUid(self, date, summary):
    timestamp = date.strftime("%Y%m%d")
    summary = "".join(summary.lower().split(" "))
    return summary + "_" + timestamp


class ShowCalendar:
  calendar = None

  def __init__(self, calendarName):
    self.calendar = Calendar()
    self.calendar.add("version", "2.0")
    self.calendar.add("prodid", "-//%s//%s//" % (calendarName, "-".join(calendarName.lower().split(" "))))
    self.calendar.add("x-wr-calname", "%s" % (calendarName))

  def addEvents(self, showEvents):
    for showEvent in showEvents:
      self.calendar.add_component(showEvent.event)

  def save(self, path):
    handle = open(path, "w")
    handle.write(self.calendar.to_ical())
    handle.close()


def main(calendarName, calendarPath):
  calendar = ShowCalendar(calendarName)
  for showName in shows:
    show = Show(showName)
    calendar.addEvents(show.episodes)
  calendar.save(calendarPath)

main("TV Shows", "tv-shows.ical")