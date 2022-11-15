# https://superfastpython.com/multiprocessing-pool-for-loop/
# https://superfastpython.com/multiprocessing-pool-mutex-lock/
from PIL import Image
from PIL import ImageEnhance
import os
import multiprocessing

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
    count = 0
    for images in os.listdir(uPath):
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".gif")):
            img = Image.open(os.path.join(uPath, images))
            uImages.append((str(images),img))
            count += 1
    return uImages, count

def bulkImageEnchancer(uPath, ePath, eTime, newBrightness, newSharpness, newContrast, numProcess):
    pool = multiprocessing.Pool(numProcess)

    uImages, count = getImages(uPath)

    ePath = [ePath] * count
    newBrightness = [newBrightness] * count
    newSharpness = [newSharpness] * count
    newContrast = [newContrast] * count

    with multiprocessing.Pool() as pool:
        pool.starmap(enhanceImage, zip(uImages, ePath, newBrightness, newSharpness, newContrast))
    

if __name__ == '__main__':
    bulkImageEnchancer(r'..\BulkImageEnhancer\unenhanced', r'..\BulkImageEnhancer\enhanced', 10, 2, 3, 4, 5)

