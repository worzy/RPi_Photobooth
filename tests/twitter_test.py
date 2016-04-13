import config
import random
from twython import Twython

# setup the twitter api client
twitter_api = Twython(
config.twitter_CONSUMER_KEY,
config.twitter_CONSUMER_SECRET,
config.twitter_ACCESS_KEY,
config.twitter_ACCESS_SECRET,
)

hashtags = "#Clarl2016"

statuses = [
"Beep Boop! I was programmed to love!",
"Weddings are fun! Beep Boop!",
"Beep Boop! A memento of the day!",
"Don't they look great!?"
]

print 'hello, I am about to tweet. HERE WE GO'


# get filename for this group of photos
#now = jpg_group
now = "test"
fname = config.file_path + now + '.gif'
# choose new status from list and at the hashtags
status_choice = random.choice(statuses)
status_total = status_choice + " " + hashtags

print "Tweeting: " + fname + " with status : " + status_total
#twitter_photo = open(fname, 'rb')  # open file
twitter_photo = open("../samplepics/test.gif", 'rb')
response = twitter_api.upload_media(media=twitter_photo)  # upload to twitter
# update status with image and new status
twitter_api.update_status(media_ids=[response['media_id']], status=status_total)



print 'I did it! are you proud of me?'
