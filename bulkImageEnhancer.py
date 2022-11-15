# https://superfastpython.com/multiprocessing-pool-for-loop/
# https://superfastpython.com/multiprocessing-pool-mutex-lock/
from PIL import Image
from PIL import ImageEnhance
import os
import multiprocessing
from multiprocessing import Manager

def enhanceImage(processID, semaphore, index, count, uImg, ePath, newBrightness, newSharpness, newContrast):
    
        semaphore.acquire()
        if index.value < count:
            imgName = os.path.splitext(uImg[index.value][0])[0]
            fileExtension = os.path.splitext(uImg[index.value][0])[1]

            print("Process " + str(processID) + " is enhancing image " + imgName)
            
            eImg = ImageEnhance.Brightness(uImg[index.value][1]).enhance(newBrightness)

            eImg = ImageEnhance.Sharpness(eImg).enhance(newSharpness)

            eImg = ImageEnhance.Contrast(eImg).enhance(newContrast)

            newFileName = 'enhanced_' + imgName + fileExtension
            eImg.save(os.path.join(ePath, newFileName))

            index.value += 1
            print("Total images finished enhancing: " + str(index.value))
        semaphore.release()
    

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
    uImages, count = getImages(uPath)
    manager = Manager()
    shared_counter_with_lock = manager.Value('i', 0)
    shared_resource_lock = multiprocessing.Semaphore(1)

    processes = []

    while shared_counter_with_lock.value < count:
        for i in range(numProcess):
            p = multiprocessing.Process(target=enhanceImage, args=(i, shared_resource_lock, shared_counter_with_lock, count, uImages, ePath, newBrightness, newSharpness, newContrast))
            processes.append(p)
            p.start()
    
    for p in processes:
        p.join()
    


if __name__ == '__main__':
    bulkImageEnchancer(r'..\BulkImageEnhancer\unenhanced', r'..\BulkImageEnhancer\enhanced', 10, 2, 3, 4, 3)

