import config

from twython import Twython


#setup the twitter api client
twitter_api = Twython(
    config.twitter_CONSUMER_KEY,
	config.twitter_CONSUMER_SECRET,
	config.twitter_ACCESS_KEY,
	config.twitter_ACCESS_SECRET,
);

print 'hello'
