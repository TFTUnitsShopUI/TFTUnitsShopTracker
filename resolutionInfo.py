import pyautogui

"""
    !!!PIXELS BETWEEN CHAMPION CARDS!!!:
    ON 1440P: 11, 13, 13, 13, 13
    ON 1080P: 8, 8, 8, 9, 8
    Have not tested other resolutions but this indicates that either hard coding of the
    locations are necessary or use OCR method as default for other resolutions.
"""

SUPPORTED_RESOLUTIONS = [(2560,1440),(1920,1080)]
UNITS_IN_SHOP = 5

def calculateCoordinates(SHOP_X, SHOP_Y, SHOP_HEIGHT, CHAMPION_CARD, SHOP_SPACING):
    CHAR_COORDS = []

    for i in range(0, UNITS_IN_SHOP):
        leftCoord = SHOP_X + (i*CHAMPION_CARD) + sum(SHOP_SPACING[:i+1])
        rightCoord = leftCoord + CHAMPION_CARD
        CHAR_COORDS.append(((leftCoord, SHOP_Y), (rightCoord, SHOP_Y + SHOP_HEIGHT)))

    return CHAR_COORDS

#Shop location based on resolution:
class res1440p:
    SHOP_X = 641
    SHOP_Y = 1238
    SHOP_HEIGHT = 190 + 1
    CHAMPION_CARD = 255 + 1
    SHOP_SPACING = [0, 11, 13, 13, 13]
    START_TIMER_PIXEL = (1259, 194)
    END_TIMER_PIXEL = (1290, 199)

    REFRESH_BUTTON = ((365, 1238), (620, 1327))


    CHAR_COORDS = calculateCoordinates(SHOP_X, SHOP_Y, SHOP_HEIGHT, CHAMPION_CARD, SHOP_SPACING)

class res1080p:
    SHOP_X = 480
    SHOP_Y = 928
    SHOP_HEIGHT = 143 + 1
    CHAMPION_CARD = 192 + 1
    SHOP_SPACING = [0, 8, 8, 9, 8]
    START_TIMER_PIXEL = (939,139)
    END_TIMER_PIXEL = (963, 150)

    REFRESH_BUTTON = ((273, 928), (464, 995))

    CHAR_COORDS =  calculateCoordinates(SHOP_X, SHOP_Y, SHOP_HEIGHT, CHAMPION_CARD, SHOP_SPACING)

#To be changed, if needed, when different resolutions are actually added.
maxWidth, maxHeight = pyautogui.size()
resolutionClass = res1440p if maxWidth == 2560 and maxHeight == 1440 else res1080p


if __name__ == "__main__":
    print(resolutionClass.CHAR_COORDS)

