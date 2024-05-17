import os
import cv2
import math
import pyautogui
import numpy as np
from mss import mss

sct = mss()
checkIdx = 0
foundImgIdx = None
bounding_box = {'top': 0, 'left': 0, 'width': 2560, 'height': 1440}
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
fileNames = next(os.walk("./images"), (None, None, []))[2]  # [] if no file
images = []
for name in fileNames:
    img = cv2.imread(f'./images/{name}')
    images.append({ "image": img, "name": name })

while True:
    sct_img = sct.grab(bounding_box)
    imgArr = np.array(sct_img)
    # liveImgGray = cv2.cvtColor(imgArr, cv2.COLOR_BGR2RGB)
    # liveImage = Image.fromarray(imgArr)

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

    # Could be one approach to detect region name
    if "-title" in baseImage["name"]:
        try:
            res = pyautogui.locateOnScreen(baseImage["image"], confidence=.6)
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
