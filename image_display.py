import cv2
from matplotlib import pyplot as plt


def display_images(images):
    fig = plt.figure()

    for i in range(int(len(images1))):
        plt.imshow(images1[i], cmap='gray')
        plt.xticks([]), plt.yticks([])
        plt.show()


img1 = cv2.imread("Yellow.jpg")
img2 = cv2.imread("Yellow-Green.jpg")
img3 = cv2.imread("Yellow-Orange.jpg")

img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
img3_hsv = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)

img1_h, img1_s, img1_v = cv2.split(img1_hsv)
img2_h, img2_s, img2_v = cv2.split(img2_hsv)
img3_h, img3_s, img3_v = cv2.split(img3_hsv)

images1 = [img1, img1_h, img1_s, img1_v]
images2 = [img2, img2_h, img2_s, img2_v]
images3 = [img3, img3_h, img3_s, img3_v]


display_images(images1)
display_images(images2)
display_images(images3)
