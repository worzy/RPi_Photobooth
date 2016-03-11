import Image, ImageDraw, ImageFont


sampledir = "../samplepics/image"
##moving original pics to backup
##copypics = "cp " + file_path + now + "*.jpg "+ file_path
##print copypics
##os.system(copypics)

##resizing + montaging
#print "Resizing Pics..." #necessary?
##convert -resize 968x648 /home/pi/photobooth/pics/*.jpg /home/pi/photobooth/pics_tmp/*_tmp.jpg
#graphicsmagick = "gm mogrify -resize 968x648 " + config.file_path + now + "*.jpg"
#copypics = "cp " + config.file_path + now + "*.jpg "+ config.file_path

##print "Resizing with command: " + graphicsmagick
#os.system(graphicsmagick)
#os.system(copypics)

#print "Montaging Pics..."
#graphicsmagick = "gm montage " + config.file_path + now + "*.jpg -tile 2x2 -geometry 1000x699+10+10 " + config.file_path + now + "_picmontage.jpg"
#print "Montaging images with command: " + graphicsmagick
#os.system(graphicsmagick)

#print "Adding Label..."
#graphicsmagick = "gm convert -append "+real_path+ "/assets/bn_booth_label_h.jpg  " + config.file_path + now + "_picmontage.jpg " + config.file_path + now + "_print.jpg"
#print "Adding label with command: " + graphicsmagick
#os.system(graphicsmagick)

image = list()
image.append(Image.open(sampledir + '01.jpg'))
image.append(Image.open(sampledir + '02.jpg'))
image.append(Image.open(sampledir + '03.jpg'))
image.append(Image.open(sampledir + '04.jpg'))

x_pic = 500
y_pic = 375
x_border = 40
y_border = 10
x_total = 1181
y_total = 1748
new_pic = Image.new('RGB', (x_total, y_total), (255, 255, 255))
new_pic.paste(image[0].resize((x_pic,y_pic), Image.ANTIALIAS), (x_border,y_border))
new_pic.paste(image[1].resize((x_pic,y_pic), Image.ANTIALIAS), (x_border,1*y_pic+2*y_border))
new_pic.paste(image[2].resize((x_pic,y_pic), Image.ANTIALIAS), (x_border,2*y_pic+3*y_border))
new_pic.paste(image[3].resize((x_pic,y_pic), Image.ANTIALIAS), (x_border,3*y_pic+4*y_border))
new_pic.paste(image[0].resize((x_pic,y_pic), Image.ANTIALIAS), (x_total-x_border-x_pic,y_border))
new_pic.paste(image[1].resize((x_pic,y_pic), Image.ANTIALIAS), (x_total-x_border-x_pic,1*y_pic+2*y_border))
new_pic.paste(image[2].resize((x_pic,y_pic), Image.ANTIALIAS), (x_total-x_border-x_pic,2*y_pic+3*y_border))
new_pic.paste(image[3].resize((x_pic,y_pic), Image.ANTIALIAS), (x_total-x_border-x_pic,3*y_pic+4*y_border))
new_pic.save(samepledir + '_total.jpg')
#try:
#	new_pic.save('/home/pi/photobooth/backups/' + now + '_total.jpg')
#except:
#	print "Flash drive not found"
