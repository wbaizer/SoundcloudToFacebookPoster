import facebook
import json


def run(channel_id):
	''' Driver for program '''

	print "Starting poster..."
	graph = setup(channel_id)
	episodes = get_episodes(channel_id)
	if not episodes:
		print "No episodes to post."
		print "Ending poster..."
		return
	else:
		post_to_page(graph, episodes)
	print "Ending poster..."

def setup(channel_id):
	with open('credentials.json', 'r') as readfile:
		credentials = json.load(readfile).get('facebook-'+channel_id)
	graph = facebook.GraphAPI(credentials.get('access_token'))
	return graph

def post_to_page(graph, episodes):
	for episode in episodes:
		msg = episode.get('description')
		link = episode.get('link')
		graph.put_object(parent_object='me',connection_name='feed', message=msg, link=link)

def get_episodes(channel_id):
	with open('data/' + channel_id + '-soundcloud-output.json', 'r') as reddit_output:
		episodes = json.load(reddit_output)
	return episodes

if __name__ == "__main__":
	run('183036682')
	
#How to get page_access_token using long lasting access_token
#How to make a long lasting access token https://stackoverflow.com/questions/10467272/get-long-live-access-token-from-facebook
#graph = facebook.GraphAPI(long_lasting_access_token)
#resp = graph.get_object('me/accounts')
#page_access_token = None
#for page in resp['data']:
#	if page['id'] == facebook page id:
#		page_access_token = page['access_token']
#print page_access_token