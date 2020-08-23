import cv2
import numpy as np
import os
import DetectChars
import DetectPlates
import PossiblePlate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import pandas as pd
import sys
import formatter

class Bot:
    def __init__(self, number):
        self.number = number
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get('https://rtovehicle.info/index.php')
        time.sleep(2)
        
        search = bot.find_element_by_id('vehiclenum')
        search.send_keys(self.number)
       
        clicker = bot.find_element_by_id('searchB')
        clicker.click()
     
        time.sleep(3)
        bot.execute_script("window.scrollTo(0, 400)")
        bot.save_screenshot("rto.png")
        
    def img_text(self):
        pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"    
        image = Image.open('rto.png')
        image_to_text = pytesseract.image_to_string(image, lang='eng')
        text = []
        text.append(image_to_text)
        formatter.ToFormat(text[0])
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    
    if blnKNNTrainingSuccessful == False:
        print("\nerror: KNN training was not successful\n")
        return
    
    imgOriginalScene= cv2.imread("6.jpg")

    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:
        print("\nno license plates were detected\n")
    else:

        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0]

        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return

        #print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        #print("----------------------------------------")
        return licPlate.strChars
    

    return



if __name__ == "__main__":
    s=main()
    print("\nlicense plate read from image = " + s + "\n")
    print("----------------------------------------")
    cv2.waitKey(0)
    quantin = Bot(s)
    quantin.login()
    key = Keys()
    quantin.img_text()
















