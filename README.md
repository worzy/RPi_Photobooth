Pibooth - photobooth
=======================

A DIY photo booth using a Raspberry Pi that automatically:
- Sends animated gifs to a Twitter account
- IFTTT used to create pintrest/tumblr collections

Based off of: 
 - http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/ -  [Code - Github](https://github.com/drumminhands/drumminhands_photobooth)
 - http://www.instructables.com/id/Raspberry-Pi-photo-booth-controller/  - [Code - Github](https://github.com/safay/RPi_photobooth)

This requires:
  - PiCamera -- http://picamera.readthedocs.org/
  - GraphicsMagick -- http://www.graphicsmagick.org/
  - twython -- https://github.com/ryanmcgrath/twython

  Updated as of April 2016 - Latest versions of libaries + APIs
  Things new in this version:
   - idle mode which checks if internet is back for any files not uploaded
   - better handling of errors with pygame and picamera - should exit gracefully in more cases now
