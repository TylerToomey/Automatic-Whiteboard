from PIL import Image 
from PIL import ImageColor
from PIL import ImageFilter
from PIL import ImageDraw

import math
import sys
import os
import piexif

my_path = os.path.dirname(__file__)

BLUR_AMMOUNT = 4
THRESHOLD = 240
IMAGE_SIZE_MAX = 1500
IMAGE_SCALE = 1
GAMMA = 1

MAX_BRUSH = 15
MIN_BRUSH = 1

SPACING = 20
BRUSH_SIZE = 1

width = 0
height = 0
outPoints = []

def processImage(inputImg):
    img = Image.open(my_path+"/"+inputImg).convert('LA').filter(ImageFilter.GaussianBlur(BLUR_AMMOUNT)).convert('L')
    
    ## ACCOUNT FOR AND REMOVE EXIF ORIENTATION DATA 
    ### JESUS CHRIST FUCK THIS PART
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    ################################################
    
    widthOld, heightOld = img.size

    print("ORIGINAL DIMENSIONS: ", widthOld, ", ", heightOld)
    
    width = widthOld
    height = heightOld
    ratio = 0

    ## Resize based on maximum size
    if widthOld > heightOld:
        ratio = IMAGE_SIZE_MAX/widthOld
        width = IMAGE_SIZE_MAX
        height = heightOld * ratio

    elif widthOld < heightOld:
        ratio = IMAGE_SIZE_MAX/heightOld
        height = IMAGE_SIZE_MAX
        width = widthOld * ratio

    width = width * IMAGE_SCALE
    height = height * IMAGE_SCALE
    print("RESIZING TO ", int(width), ", ", int(height))

    canvas = Image.new('1',(int(width),int(height)),'white')
    sample = img.resize((int(width),int(height)),resample=Image.BICUBIC) ## Resize the original without interpolation data loss
    painter = ImageDraw.Draw(canvas)

    numDots = (width / SPACING) * (height / SPACING)
    print("DRAWING ", int(numDots), " dots")

    flipTable = 0
    stack = []
    for i in range(1, round(width / SPACING)):
        for k in range(1,round(height / SPACING)):
            x = math.floor(i*SPACING)
            y = math.floor(k*SPACING)
            pixel = sample.getpixel((x,y))
            if pixel < THRESHOLD:
                BRUSH_SIZE = ((sample.getpixel((x,y)) - 1) / (255 - 1)) * (MAX_BRUSH - MIN_BRUSH) + MIN_BRUSH
                BRUSH_SIZE = math.ceil(MAX_BRUSH-BRUSH_SIZE) * GAMMA
                stack.append((x,y,BRUSH_SIZE))
            else:
                 BRUSH_SIZE = 0
            painter.ellipse((x-BRUSH_SIZE,y-BRUSH_SIZE,x+BRUSH_SIZE,y+BRUSH_SIZE),ImageColor.getcolor('black','1'))
        
        if flipTable == 0:
            stack.reverse()
        outPoints.append(stack.copy())
        flipTable = 1 - flipTable
        stack.clear()

    canvas.save(my_path+"/output.png")
    print("FINISHED. Saved to ", my_path, "/output.png")

    return canvas

def getPoints():
    return outPoints

def main():
    myImg = processImage(sys.argv[1])
    output = open("output.txt","w+")
    getPoints()
    toWrite = ""
    for i in outPoints:
        for k in i:
            toWrite += str(k[0]) + "," + str(k[1]) + "," + str(k[2]) + "/"
    toWrite+="<"
    output.write(toWrite)
    output.close()

if __name__ == "__main__":
    main()
    

    

        



    