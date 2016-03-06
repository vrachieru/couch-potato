from pytvdbapi import api

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
  return "%s S%sE%s" % (show.SeriesName, episode.SeasonNumber, episode.EpisodeNumber)

def getDate(episode):
  return episode.FirstAired

def getDescription(episode):
  return episode.Overview

def main():
  for showName in shows:
    show = getShow(showName)
    for season in show: 
      for episode in season:
        getEpisode(show, episode)

main()