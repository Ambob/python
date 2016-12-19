# -*- coding: utf-8 -*-
import Image
import ImageDraw
import ImageChops
import colorsys
import sys
import operator
def equalize(h):
    lut = []
    for b in range(0, len(h), 256):
        # 步数
        step = reduce(operator.add, h[b:b+256]) / 255
        # 创建查找表
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]
    return lut
def autoCrop(image,backgroundColor=None):
    '''Intelligent automatic image cropping.
       This functions removes the usless "white" space around an image.
        
       If the image has an alpha (tranparency) channel, it will be used
       to choose what to crop.
        
       Otherwise, this function will try to find the most popular color
       on the edges of the image and consider this color "whitespace".
       (You can override this color with the backgroundColor parameter) 
 
       Input:
            image (a PIL Image object): The image to crop.
            backgroundColor (3 integers tuple): eg. (0,0,255)
                 The color to consider "background to crop".
                 If the image is transparent, this parameters will be ignored.
                 If the image is not transparent and this parameter is not
                 provided, it will be automatically calculated.
 
       Output:
            a PIL Image object : The cropped image.
    '''
     
    def mostPopularEdgeColor(image):
        ''' Compute who's the most popular color on the edges of an image.
            (left,right,top,bottom)
             
            Input:
                image: a PIL Image object
             
            Ouput:
                The most popular color (A tuple of integers (R,G,B))
        '''
        im = image
        if im.mode != 'RGB':
            im = image.convert("RGB")
         
        # Get pixels from the edges of the image:
        width,height = im.size
        left   = im.crop((0,1,1,height-1))
        right  = im.crop((width-1,1,width,height-1))
        top    = im.crop((0,0,width,1))
        bottom = im.crop((0,height-1,width,height))
        pixels = left.tostring() + right.tostring() + top.tostring() + bottom.tostring()
 
        # Compute who's the most popular RGB triplet
        counts = {}
        for i in range(0,len(pixels),3):
            RGB = pixels[i]+pixels[i+1]+pixels[i+2]
            if RGB in counts:
                counts[RGB] += 1
            else:
                counts[RGB] = 1   
         
        # Get the colour which is the most popular:       
        mostPopularColor = sorted([(count,rgba) for (rgba,count) in counts.items()],reverse=True)[0][1]
        return ord(mostPopularColor[0]),ord(mostPopularColor[1]),ord(mostPopularColor[2])
     
    bbox = None
     
    # If the image has an alpha (tranparency) layer, we use it to crop the image.
    # Otherwise, we look at the pixels around the image (top, left, bottom and right)
    # and use the most used color as the color to crop.
     
    # --- For transparent images -----------------------------------------------
    if 'A' in image.getbands(): # If the image has a transparency layer, use it.
        # This works for all modes which have transparency layer
        bbox = image.split()[list(image.getbands()).index('A')].getbbox()
    # --- For non-transparent images -------------------------------------------
    elif image.mode=='RGB':
        if not backgroundColor:
            backgroundColor = mostPopularEdgeColor(image)
        # Crop a non-transparent image.
        # .getbbox() always crops the black color.
        # So we need to substract the "background" color from our image.
        bg = Image.new("RGB", image.size, backgroundColor)
        diff = ImageChops.difference(image, bg)  # Substract background color from image
        bbox = diff.getbbox()  # Try to find the real bounding box of the image.
    else:
        raise NotImplementedError, "Sorry, this function is not implemented yet for images in mode '%s'." % image.mode
         
    if bbox:
        image = image.crop(bbox)
         
    return image
def get_dominant_color(image):
    image = image.convert('RGBA')
    image.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        if y > 0.9:
            continue
        # Calculate the score, preferring highly saturated colors.
        # Add 0.1 to the saturation so we don't completely ignore grayscale
        # colors by multiplying the count by zero, but still give them a low
        # weight.
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color

file_name=sys.argv[1]
print file_name
imq=Image.open(file_name)
imq1=imq.split()[2]
# lut = equalize(im.histogram())
# # 查表
# imq = im.point(lut)
# im.save("roi_equalized.png")
pix=imq1.load()
width = imq1.size[0]
print type(width)
height = imq1.size[1]
draw = ImageDraw.Draw(imq1)
x,y=0,0
while y<height:
    while x<width:
        b = pix[x, y]
        if(b<80):
            draw.point([(x,y)], fill = (255))
        x=x+1
    x=0
    y=y+1
    print y,height
imq1.save('ok%s'%file_name)

# a,c=12,30
# count_yellow=0
# while a<width:
# 	b,d=10,30
# 	while d<height:
# 		imq1=imq.crop((a,b,c,d))
# 		imq1.save("img%s%s.png"%(a,c))
# 		print get_dominant_color(imq1)
# 		if(get_dominant_color(imq1)[0]>120 and get_dominant_color(imq1)[1]>120 and get_dominant_color(imq1)[2]<100):
# 			count_yellow=count_yellow+1
# 			draw.rectangle((a,b,a+10,b+10), fill = (255,0,0))
# 		d=d+28
# 		b=b+28
# 	a=a+28
# 	c=c+28
# ddd=str(count_yellow)+"much"
# draw.text((width/2, 50), ddd, fill='#000000')
# print count_yellow,'much'
# imq.save('innw.png')




# im = imq.convert('RGB')
# pix = im.load()
# width = im.size[0]
# height = im.size[1]
# for_retangle=[]
# for_start=0
# for x in range(width):
# 	for y in range(height):
# 		r, g, b = pix[x, y]
# 		if(r>200 and g>200 and b<120):
# 			draw.point([(x,y)], fill = (0, 0, 0))
# 			for_start=1
# 		else:
# 			for_start=0
# imq.save('hhhh.png')