import sched, time
import datetime
import soundcloud_scraper
import facebook_poster
import tc_channels


def run(sc):
	st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	print "Running program... " + str(st)
	channel_ids = tc_channels.get_channels()
	for channel_id in channel_ids:
		soundcloud_scraper.run(channel_id)
		facebook_poster.run(channel_id)
	print "Program run. Sleeping for 5 mins..."
	s.enter(300, 1, run, (sc,))
		
if __name__ == "__main__":
	s = sched.scheduler(time.time, time.sleep)
	s.enter(1, 1, run, (s,))
	s.run()