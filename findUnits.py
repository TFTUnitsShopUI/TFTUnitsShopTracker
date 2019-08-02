# Order in which things are done: 
# Image Grab Screen ->
#  Isolate desired area (Champs shop) -> 
#  Determine Characters

# -> Register Clicks on shop -> Save characters bought
# -> Check against previously bought -> Notify of duplicates

# Determine if character is sold ->
# Remove from dictionary

import pyautogui
from PIL import ImageGrab
from PIL import Image
import math
import time
import resolutionInfo
from timeit import default_timer as timer

calcTime = False

#Divide by 40 since GCD_WIDTH of 2560,1440,1920,1080
#10 Units from the left, 9 units from the right, 6 units from the bottom
GCD = 40
UNITS_FROM_LEFT = 10
UNITS_FROM_RIGHT = 9
UNITS_FROM_BOTTOM = 6
UNITS_IN_SHOP = 5

def findShop(resolutionClass=None):
    """Returns an image of the entire shop, containing all champions that are available"""

    if resolutionClass:
        shopImage = pyautogui.screenshot(region=(
            resolutionClass.SHOP_X, resolutionClass.SHOP_Y,
            resolutionClass.CHAMPION_CARD*UNITS_IN_SHOP + sum(resolutionClass.SHOP_SPACING),
            resolutionClass.SHOP_HEIGHT))
        return shopImage, resolutionClass.SHOP_X, resolutionClass.SHOP_Y


    #Resolution Class should always be set for now since UI is inconsistent and
    #the following will have to ideally be fixed for any resolution support.
    if resolutionClass is None:
        return
    #Have to calculate relative to screen resolution.
    maxWidth, maxHeight = pyautogui.size()
    #Default if it's another resolution, setup OCR here.
    topShopBorder = maxHeight - ((maxHeight/GCD) * UNITS_FROM_BOTTOM) #y coordinate
    leftShopBorder = (maxWidth/GCD) * UNITS_FROM_LEFT
    rightShopBorder = maxWidth - ((maxWidth/GCD) * UNITS_FROM_RIGHT)

    #Just the image of the characters you can buy.
    shopImage = pyautogui.screenshot(region=(leftShopBorder, topShopBorder,
        rightShopBorder - leftShopBorder, maxHeight - topShopBorder))

    return shopImage, leftShopBorder, topShopBorder



def isolateShopUnitsSupported(resolutionClass):
    """Returns a list of image objects of the champions that are currently offered
    to be drafted by the player and saves the images to disk.

    Arguments:
    resolutionClass: Class of constants containing information of where the Shop is located.
    """

    if not resolutionClass:
        sys.exit("No Resolution Class given.")

    allUnits = []
    
    #TODO: Although there is an inconsistent UI, perhaps be able to find relative positions
    #instead of hard coded coordinates again with proper analysis of all resolutions.

    # for i in range (0, resolutionInfo.UNITS_IN_SHOP):
    #     leftBorder = resolutionClass.SHOP_X + (i*singleWidth) + sum(resolutionClass.SHOP_SPACING[:i+1])

    #     singleImage = pyautogui.screenshot(str(pyautogui.size().width)+"SHOP_SINGLE"+str(i)+".png", region=(
    #         leftBorder, resolutionClass.SHOP_Y, singleWidth, resolutionClass.SHOP_HEIGHT))

    #     allUnits.append(singleImage)

    for unitLocation in resolutionClass.CHAR_COORDS:
        singleImage = pyautogui.screenshot(str(pyautogui.size().width)+"SHOP_SINGLE"+str(unitLocation)+".png", region=(
            unitLocation[0][0], unitLocation[0][1], resolutionClass.CHAMPION_CARD, resolutionClass.SHOP_HEIGHT))

        allUnits.append(singleImage)

    return allUnits

def fingerprintCharacters(resolutionClass, delay=0):
    """Returns a list of fingerprints of all the champions currently offered in the shop.
    Delay is required when you manually refresh the shop as it takes a moment for the UI
    to update.

    Arguments:
    resolutionClass: Class of constants containing screen/UI information
    delay: Time given for the UI in game to update
    """

    if calcTime:
        start = timer()

    currentlyOfferedCharacters = []

    if delay > 0:
        time.sleep(delay)
    """ Original method of taking a screenshot of the whole screen.
    # image = pyautogui.screenshot()
    # #Arbitrary two points really
    # for unit in resolutionClass.CHAR_COORDS:
    #     pixel1 = (unit[0][0] + math.floor(resolutionClass.CHAMPION_CARD/2), unit[0][1] + math.floor(resolutionClass.SHOP_HEIGHT/4))
    #     pixel2 = (unit[0][0] + math.floor(resolutionClass.CHAMPION_CARD*3/4), unit[0][1] + math.floor(resolutionClass.SHOP_HEIGHT/4))
    #     currentlyOfferedCharacters.append(
    #         (image.getpixel(pixel1), image.getpixel(pixel2)))
    """

    """ THIS WAY IS SLOWER (separating into 5 small images)
    # #Isolating Units first
    # pixel1 = (math.floor(resolutionClass.CHAMPION_CARD/2), math.floor(resolutionClass.SHOP_HEIGHT/4))
    # pixel2 = (math.floor(resolutionClass.CHAMPION_CARD*3/4), math.floor(resolutionClass.SHOP_HEIGHT/4))

    # for unitImage in isolateShopUnitsSupported(resolutionClass):
    #     currentlyOfferedCharacters.append(
    #         (unitImage.getpixel(pixel1), unitImage.getpixel(pixel2)))
    """

    #Very slightly faster? Very similar times by like 0.01 difference
    # #Just get image of the shop
    image, _, _, = findShop(resolutionClass)
    #Arbitrary two points really
    for unit in resolutionClass.CHAR_COORDS:
        pixel1 = (unit[0][0] - resolutionClass.SHOP_X + math.floor(resolutionClass.CHAMPION_CARD/2),
            unit[0][1] - resolutionClass.SHOP_Y + math.floor(resolutionClass.SHOP_HEIGHT/4))
        pixel2 = (unit[0][0] - resolutionClass.SHOP_X + math.floor(resolutionClass.CHAMPION_CARD*3/4),
            unit[0][1] - resolutionClass.SHOP_Y + math.floor(resolutionClass.SHOP_HEIGHT/4))
        pixel3 = (unit[0][0] - resolutionClass.SHOP_X + math.floor(resolutionClass.CHAMPION_CARD*3/4),
            unit[0][1] - resolutionClass.SHOP_Y + math.floor(resolutionClass.SHOP_HEIGHT/2))
        currentlyOfferedCharacters.append(
            (image.getpixel(pixel1), image.getpixel(pixel2), image.getpixel(pixel3)))

    if calcTime:
        end = timer()
        print(end-start)

    return currentlyOfferedCharacters

def checkUnitClick(resolutionClass, mouseX, mouseY):
    """To be called after the mouse has been clicked and determines which unit
    in the shop was clicked on.
    """
    COORDS = resolutionClass.CHAR_COORDS
    #Determine which unit was clicked on
    if mouseY > resolutionClass.SHOP_Y and mouseY < resolutionClass.SHOP_Y + resolutionClass.SHOP_HEIGHT:
        for i in range(0, UNITS_IN_SHOP):
            if mouseX > COORDS[i][0][0] and mouseX < COORDS[i][1][0]:
                return i
    return None


if __name__ == "__main__":
    #TODO: PyAutoGUI only screenshots the main monitor. Changes needed for multiple monitor support.
    #Fullscreen/?Borderless? only

    """The following is just the timer leftover from experimenting with different ways
    to read the information, could be useful later if another method is attempted."""

    #shopImage, leftShopBorder, topShopBorder = findShop(resolutionClass)
    #isolateShopUnitsSupported(resolutionClass)

    #fingerprintCharacters(resolutionInfo.resolutionClass)
    start = timer()

    
    #im = ImageGrab.grab
    #for i in range(0,100):
        #image = ImageGrab.grab()
        #vs.
        #pixelRGB = im()

        #pixelRGB = ImageGrab.grab().getpixel((1278, 200))

        #image = pyautogui.screenshot(region=(1281, 200, 1, 1))
        #image.getpixel((0,0))

        #r,g,b = pyautogui.screenshot().getpixel((1278,200))

        #pyautogui.pixelMatchesColor(1278, 200, (233,187,27))

    end = timer()
    print(end-start)

    isolateShopUnitsSupported(resolutionInfo.resolutionClass)

    #     print(image.getpixel((image.width/2, image.height/2)))
    #Fingerprint the data by selecting 3 specific points of the image. 
    #TODO: May not be enough, add option to change.
