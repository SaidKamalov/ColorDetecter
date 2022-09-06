import argparse
import pandas as pd
import cv2

# get image path from console input.
def get_image():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=False, help="image path")
    args = vars(parser.parse_args())
    img_path = args["image"]
    return img_path


# read csv of colors dataset.
def get_csv():
    column_names = ["color_alias", "color_name", "hex", "R", "G", "B"]
    color_inf = pd.read_csv(filepath_or_buffer="colors.csv", names=column_names)
    return color_inf


# get r g b and x,y coordinates when double-click on the left button.
def pick_color(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, clicked, posx, posy
        posx, posy = x, y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        clicked = True


# color search.
def get_color_name(r, g, b):
    minimum = 100000
    index = 0
    for i in range(len(my_csv)):
        dist = (
            abs(r - int(my_csv.loc[i, "R"]))
            + abs(g - int(my_csv.loc[i, "G"]))
            + abs(b - int(my_csv.loc[i, "B"]))
        )
        if dist < minimum:
            minimum = dist
            index = i
    return my_csv.loc[index, "color_name"]


clicked = False
img = cv2.imread(get_image())
my_csv = get_csv()
cv2.namedWindow("image")
cv2.setMouseCallback("image", pick_color)
while True:
    cv2.imshow("image", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = (
            get_color_name(r, g, b)
            + " R = "
            + str(r)
            + " G = "
            + str(g)
            + " B = "
            + str(b)
        )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
