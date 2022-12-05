# https://superfastpython.com/multiprocessing-pool-for-loop/
# https://superfastpython.com/multiprocessing-pool-mutex-lock/
from PIL import Image
from PIL import ImageEnhance
import os
import multiprocessing
import time

# enhances an image with the passed values
def enhanceImage(uImg, terminate, shared_counter, semaphore, start, eTime, ePath, newBrightness, newSharpness, newContrast):
    # acquires semaphore to check whether or not the current elapsed time is already greater than the time requirement
    # terminates if current elapsed time is greater than the time req
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

    # enhances image
    imgName = os.path.splitext(uImg[0])[0]
    fileExtension = os.path.splitext(uImg[0])[1]

    eImg = ImageEnhance.Brightness(uImg[1]).enhance(newBrightness)

    eImg = ImageEnhance.Sharpness(eImg).enhance(newSharpness)

    eImg = ImageEnhance.Contrast(eImg).enhance(newContrast)

    print("Enhancing " + imgName)

    newFileName = 'enhanced_' + imgName + fileExtension
    eImg.save(os.path.join(ePath, newFileName))

    # acquires semaphore to increase the counter of saved enhanced images
    semaphore.acquire()
    shared_counter.value += 1
    print("saved " + imgName)
    semaphore.release()

# gets the images and places it into an array [(name of img, img)]
def getImages(uPath):
    uImages = []

    for images in os.listdir(uPath):
        if (images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".gif")):
            img = Image.open(os.path.join(uPath, images))
            uImages.append((str(images),img))
        
    return uImages

# creates manager and pool for multiprocessing
def bulkImageEnchancer(uPath, ePath, eTime, newBrightness, newSharpness, newContrast, numProcess):
    print("NUMBER OF PROCESSES: " + str(numProcess))
    
    # get time in seconds
    eTimeS = eTime * 60

    # get images from unenhanced folder
    uImages = getImages(uPath)

    # create manager
    with multiprocessing.Manager() as manager:
        # create shared variables
        shared_counter = manager.Value('i', 0)
        terminate = manager.Value('t', False)
        # create semaphore for accessing shared variables
        semaphore = manager.Semaphore(1)

        start = time.time()
        
        # create pool with numProcess
        with multiprocessing.Pool(numProcess) as pool:
            items = [(img, terminate, shared_counter, semaphore, start, eTimeS, ePath, newBrightness, newSharpness, newContrast) for img in uImages]

            # map all the items to the enhanceImage function and wait until it finishes
            res = pool.starmap_async(enhanceImage, items)
            res.wait()

            # get elapsed time after all has finished or terminated early
            end = time.time()
            elapsed_time = (end - start) / 60
            print("Finished enhancing images")
            # print("total enhanced = " + str(shared_counter.value))
            # print("total elapsed time = " + str(elapsed_time))

            # save information to text file
            f = open('results.txt', 'w')
            f.write("folder location: " + ePath +"\nnumber of images enhanced = " + str(shared_counter.value) + "\ntotal enhancing time = " + str(eTime) + "\ntotal elapsed time = " + str(elapsed_time))
            f.close()

    
if __name__ == '__main__':
    bulkImageEnchancer(r'..\BulkImageEnhancer\unenhanced', r'..\BulkImageEnhancer\enhanced', 0.25, 2, 3, 4, 6)

