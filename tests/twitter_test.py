import config
#import os
from twython import Twython


#setup the twitter api client
twitter_api = Twython(
    config.twitter_CONSUMER_KEY,
	config.twitter_CONSUMER_SECRET,
	config.twitter_ACCESS_KEY,
	config.twitter_ACCESS_SECRET,
);

print 'hello, I am about to tweet. HERE WE GO'

twitter_photo = open("../samplepics/hedgehog.gif",'rb')

response =twitter_api.upload_media(media=twitter_photo)
#twitter_api.update_status(status='Beep Boop! I am a robot')
twitter_api.update_status(media_ids=[response['media_id']], status='Beep Boop! Robot on a Pi! Coming atcha')
print 'I did it! are you proud of me?'

