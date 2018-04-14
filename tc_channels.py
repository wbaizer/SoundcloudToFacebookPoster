def get_channels():
	
	''' Driver for program '''
	channel_ids = []
	with open('channel_ids.txt', 'r') as readfile:
		for channel_id in readfile:
			channel_id = channel_id.replace('\n', '')
			if channel_id:
				channel_ids.append(channel_id)
	return channel_ids