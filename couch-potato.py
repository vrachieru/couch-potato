from pytvdbapi import api
from icalendar import Calendar, Event, Timezone
from datetime  import datetime, timedelta

tvdb  = api.TVDB("B43FF87DE395DF56")
shows = ["American Dad", "Family Guy"]

def getShow(showName):
  return tvdb.search(showName, "en")[0]

def getEpisode(show, episode):
  print getTitle(show, episode)
  print getDate(episode)
  print getDescription(episode)
  print 

def getTitle(show, episode):
  return "%s S%02dE%02d" % (show.SeriesName, episode.SeasonNumber, episode.EpisodeNumber)

def getDate(episode):
  return episode.FirstAired

def getDescription(episode):
  return episode.Overview


class ShowCalendar():
  calendar = None
  calendarName = "TV Shows"
  calendarDomain = "tv-shows"

  def __init__(self):
    self.calendar = Calendar()
    self.calendar.add("version", "2.0")
    self.calendar.add("prodid", "-//%s//%s//" % (self.calendarName, self.calendarDomain))
    self.calendar.add("x-wr-calname", "%s" % self.calendarName)

  def addEvent(self, summary, description, date):
    event = Event()
    event.add("summary", summary)
    event.add("description", description)
    event.add("dtstart", date)
    event.add("dtend", self.getNextDay(date))
    event.add("dtstamp", datetime.now())
    event["uid"] = self.getUid(date, summary)
    self.calendar.add_component(event)

  def getUid(self, date, summary):
    timestamp = date.strftime("%Y%m%d")
    summary = "".join(summary.lower().split(" "))
    return summary + "_" + timestamp + "@" + self.calendarDomain

  def getNextDay(self, date):
    return date + timedelta(days = 1)

  def save(self, path):
    handle = open(path, "w")
    handle.write(self.calendar.to_ical())
    handle.close()

def main():
  calendar = ShowCalendar()
  for showName in shows:
    show = getShow(showName)
    for season in show: 
      for episode in season:
      	if getDate(episode):
      	  calendar.addEvent(getTitle(show, episode), getDescription(episode), getDate(episode))
          getEpisode(show, episode)
  calendar.save("calendar.ical")

main()