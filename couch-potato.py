from bs4 import BeautifulSoup
import datetime
import requests
import re


def getTitle(episode):
	return episode.find_next('td').find_next('td').text

def getAirDate(episode):
	airDate = episode.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('span').find_next('span').string
	if airDate:
		match = re.search('(\d+)-(\d+)-(\d+)', airDate)
		if match:
			return datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3))).strftime('%d/%m/%Y')
	return "unknown"

def getEpisodes(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text)
	for node in soup.find_all('tr', attrs = { 'class':'vevent' }):
		title = getTitle(node)
		airDate = getAirDate(node)
		print(airDate + ":" + title)


getEpisodes("https://en.wikipedia.org/wiki/List_of_Family_Guy_episodes")
