import csv
from random import *
import random
import requests
import pronouncing
import re, string, timeit

timeTweets = dict()
releases = dict()

def main():
	# get tweets & map to date
	with open('tweets.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			time = row['timestamp'][0:10]
			if not time in timeTweets:
				timeTweets[time] = set()
			timeTweets[time].add(row['text'])
		# write 10 poems
		for x in range (0, 10):
			poem = []
			date = random.choice(timeTweets.keys()) # pick a random tweet date
			archives = requests.get("http://www.wsj.com/public/page/archive-" + date + ".html")
			archivesHtml = archives.text # fetch WSJ Archive HTML
			print ""
			print date
			print
			counter = 0
			for tweet in timeTweets[date]: # iterate through all tweets on selected date
				data = archivesHtml.split("archivedArticles")
				data = data[1].split("col4wide margin-left")
				data = data[0].split("<li>")
				data = data[randrange(2, len(data))]
				data = data.split("<h2>")[1]
				loc1 = data.index(">")
				loc2 = data.index("</a>")
				newsArr = data[loc1 + 1: loc2].split(" ") # split up random headline into arr
				poem.extend(newsArr)
				poem.extend(tweet.split(" "))
				date2 = "" + date[0:4] + "/" + date[5:7] # format date for State Department scraper
				press = requests.get("https://2009-2017.state.gov/r/pa/prs/ps/" + date2 + "/index.htm")
				date2 = "" + date[5:7] + "/" + date[8:10] + "/" + date2[2:4] # format for HTML search
				pressHtml = press.text # fetch state department press release HTML
				pressHtml = pressHtml.split(date2)
				if (counter + 2) < len(pressHtml): # iterate through all press releases
					state = pressHtml[counter]
					state = state.split("htm")
					state = state[1][2:]
					state = state.split("</a")[0]
					poem.extend(state.split(" "))
				counter = counter + 1
			count = 0
			for s in poem:
				s = s.replace(",", "")
				s = s.replace(".", "")
				phones = pronouncing.phones_for_word(s.lower())
				if len(phones) > 0:
					print s.lower(),
					count = count + pronouncing.syllable_count(phones[0])
					if count >= 10:
						print
						count = 0
			print



if __name__ == "__main__":
    main()





