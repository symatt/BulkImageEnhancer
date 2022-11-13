from PIL import Image
from PIL import ImageEnhance
import os

def enhanceImage(uImg, ePath, newBrightness, newSharpness, newContrast):
    imgName = os.path.splitext(uImg[0])[0]
    fileExtension = os.path.splitext(uImg[0])[1]

    eImg = ImageEnhance.Brightness(uImg[1]).enhance(newBrightness)

    eImg = ImageEnhance.Sharpness(eImg).enhance(newSharpness)

    eImg = ImageEnhance.Contrast(eImg).enhance(newContrast)

    newFileName = 'enhanced_' + imgName + fileExtension
    eImg.save(os.path.join(ePath, newFileName))


def getImages(uPath):
    uImages = []
    for images in os.listdir(uPath):
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg")):
            img = Image.open(os.path.join(uPath, images))
            uImages.append((str(images),img))
    return uImages

def bulkImageEnchancer(uPath, ePath, eTime, newBrightness, newSharpness, newContrast):
    uImages = getImages(uPath)

    for img in uImages:
        enhanceImage(img, ePath, newBrightness, newSharpness, newContrast)

bulkImageEnchancer(r'..\BulkImageEnhancer\unenhanced', r'..\BulkImageEnhancer\enhanced', 10, 10, 10, 10)

