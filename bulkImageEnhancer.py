# https://superfastpython.com/multiprocessing-pool-for-loop/
# https://superfastpython.com/multiprocessing-pool-mutex-lock/
from PIL import Image
from PIL import ImageEnhance
import os
import multiprocessing
import time

def enhanceImage(uImg, terminate, shared_counter, semaphore, start, eTime, ePath, newBrightness, newSharpness, newContrast):
    semaphore.acquire()
    if terminate.value:
        semaphore.release()
        return

    currTime = time.time()
    if currTime - start > eTime:
        terminate.value = True
        print("Enhancing time reached, exiting...")
        semaphore.release()
        return
    semaphore.release()

    imgName = os.path.splitext(uImg[0])[0]
    fileExtension = os.path.splitext(uImg[0])[1]

    eImg = ImageEnhance.Brightness(uImg[1]).enhance(newBrightness)

    eImg = ImageEnhance.Sharpness(eImg).enhance(newSharpness)

    eImg = ImageEnhance.Contrast(eImg).enhance(newContrast)

    print("Enhancing " + imgName)

    newFileName = 'enhanced_' + imgName + fileExtension
    eImg.save(os.path.join(ePath, newFileName))

    semaphore.acquire()
    shared_counter.value += 1
    print("saved " + imgName)
    semaphore.release()


def getImages(uPath):
    uImages = []

    for images in os.listdir(uPath):
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".gif")):
            img = Image.open(os.path.join(uPath, images))
            uImages.append((str(images),img))
        
    return uImages

def bulkImageEnchancer(uPath, ePath, eTime, newBrightness, newSharpness, newContrast, numProcess):
    print("NUMBER OF PROCESSES: " + str(numProcess))
    
    eTimeS = eTime * 60

    uImages = getImages(uPath)

    with multiprocessing.Manager() as manager:
        shared_counter = manager.Value('i', 0)
        terminate = manager.Value('t', False)
        semaphore = manager.Semaphore(1)
        start = time.time()
        
        with multiprocessing.Pool(numProcess) as pool:
            items = [(img, terminate, shared_counter, semaphore, start, eTimeS, ePath, newBrightness, newSharpness, newContrast) for img in uImages]
            res = pool.starmap_async(enhanceImage, items)
            res.wait()
            end = time.time()
            elapsed_time = (end - start) / 60
            print("Finished enhancing images")
            # print("total enhanced = " + str(shared_counter.value))
            # print("total elapsed time = " + str(elapsed_time))
            f = open('results.txt', 'w')
            f.write("folder location: " + ePath +"\nnumber of images enhanced = " + str(shared_counter.value) + "\ntotal enhancing time = " + str(eTime) + "\ntotal elapsed time = " + str(elapsed_time))
            f.close()

    
if __name__ == '__main__':
    bulkImageEnchancer(r'..\BulkImageEnhancer\unenhanced', r'..\BulkImageEnhancer\enhanced', 0.25, 2, 3, 4, 10)

