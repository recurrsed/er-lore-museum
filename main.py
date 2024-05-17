import os
import cv2
import math
import pyautogui
import numpy as np
from mss import mss
from threading import Thread

from ui import setupUI

shouldRun = True
images = []
checkIdx = 0
foundImgIdx = None
boundingBox = {'top': 0, 'left': 0, 'width': 2560, 'height': 1440}
LORE_INFO = {
    "caelid": "This is some lore about Caelid",
    "limgrave": "This is some lore about Limgrave",
    "forge-of-giants": "This is some lore about forge-of-giants",
    "liurnia": "This is some lore about liurnia",
    "lyndell": "This is some lore about lyndell",
    "margit": "This is some lore about margit",
    "moghwyn-palace": "This is some lore about moghwyn-palace",
    "morgott": "This is some lore about morgott",
    "radhan": "This is some lore about radhan",
    "renala": "This is some lore about renala",
    "roundtable-hold": "This is some lore about roundtable-hold",
}

# Load up images
def loadImages():
    fileNames = next(os.walk("./images"), (None, None, []))[2]  # [] if no file
    
    for name in fileNames:
        img = cv2.imread(f'./images/{name}')
        images.append({ "image": img, "name": name })

def onWindowClose():
    global shouldRun
    
    shouldRun = False

def watchScreen():
    global checkIdx, boundingBox, shouldRun

    with mss() as sct:
        while True:
            if shouldRun == False:
                break

            sct_img = sct.grab(boundingBox)
            imgArr = np.array(sct_img)
            baseImage = images[checkIdx]

            # Source: https://medium.com/scrapehero/exploring-image-similarity-approaches-in-python-b8ca0a3ed5a3
            hist_img1 = cv2.calcHist([baseImage["image"]], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
            hist_img1[255, 255, 255] = 0 #ignore all white pixels
            cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            
            hist_img2 = cv2.calcHist([imgArr], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
            hist_img2[255, 255, 255] = 0  #ignore all white pixels
            cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            
            # Find the metric value
            metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
            roundedVal = round(metric_val, 2)

            # Detect region name
            if "-title" in baseImage["name"]:
                try:
                    pyautogui.locateOnScreen(baseImage["image"], confidence=.6)
                    print("Found by title", baseImage["name"])
                except pyautogui.ImageNotFoundException:
                    pass

            if roundedVal < 0.35 or math.isnan(roundedVal):
                if (checkIdx + 1 == len(images)): # Start over if end reached
                    checkIdx = 0
                else:
                    checkIdx+= 1 # Check next img
            else:
                print(f"Found image {baseImage["name"]} with score:", roundedVal)


if __name__ == "__main__":
    loadImages()

    thread = Thread(target=watchScreen)
    thread.start()

    setupUI(onWindowClose)

