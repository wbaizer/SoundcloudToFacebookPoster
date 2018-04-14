#from lxml import html
import soundcloud
import sys
from file_read_backwards import FileReadBackwards
import json
import tc_channels

TRACKS_LIMIT = 10
SCRAPED_TRACKS_FILE = "scraped.txt"
SOUNDCLOUD_OUTPUT = "soundcloud-output.json"

def run(channel_id):
	
	''' Driver for program '''
	
	print "Starting scraper..."
	with open('credentials.json', 'r') as readfile:
		credentials = json.load(readfile).get('soundcloud')
	client = soundcloud.Client(client_id=credentials.get('client_id'))
	scrape(client, channel_id)
	print "Ending scraper..."

def scrape(client, channel_id):
	
	''' Scrape the last TRACKS_LIMIT tracks from channels and create JSON of tracks not yet scraped '''
	# Final array that will be written to twitter tracks outfile
	tracks = client.get('/users/' + channel_id + '/tracks', limit=TRACKS_LIMIT)
	new_tracks = []
	# put into list to reverse later
	#for track in tracks:
		#new_tracks.append(track)
	# Iterate through the subreddit's top X posts
	# Reverse so newest posts are at bottom of file, so they will be searched first by already_scraped()
	for track in reversed(tracks):
		# Check to see if this track has already been seen and scraped
		been_scraped = already_scraped(track.id, channel_id)
		if not been_scraped:
			# Get an object with data for Twitter
			# Append object to list to be exported to JSON
			# Add track to scraped tracks file
			print "\rScraping track" + str(track.id)
			track_obj = create_track_object(track)
			new_tracks.append(track_obj)
			with open("scraped/" + channel_id + "-" + SCRAPED_TRACKS_FILE, "a") as spf:
				spf.write(str(track.id)+"\n")
	# Export to JSON file. This contains newly scraped tracks.
	with open("data/" + channel_id + "-" + SOUNDCLOUD_OUTPUT, 'wb') as outfile:
		json.dump(new_tracks, outfile)	

def already_scraped(track_id, channel_id):
	
	''' 
	Check to see if track with 
	scrape_key = "track_id" 
	exists in file
	'''
	
	# To only check the track going back so far
	# Read line by line backwards to get most up-to-date tracks first
	with FileReadBackwards("scraped/" + channel_id + "-" + SCRAPED_TRACKS_FILE, encoding="utf-8") as spf:
		i = 0
		for line in spf:
			# If we've found a match then stop
			if line == str(track_id):
				return 1
			# If we've gotten past limit of tracks to search then stop
			if i > TRACKS_LIMIT:
				return 0
			i = i+1
	# If there is no match then the current track hasn't been scraped.
	return 0

def create_track_object(track):

	''' Create track object for inclusion in twitter posts file'''
	
	track_obj = {}
	track_obj['description'] = track.description
	track_obj['link'] = track.permalink_url
	return track_obj


if __name__ == '__main__':
	print "Running scraper..."
	channel_ids = tc_channels.get_channels()
	for channel_id in channel_ids:
		run(channel_id)

##How to find channel id
#aggieCast = client.get('/users/aggiecast')
#print aggieCast.id
#print aggieCast.username