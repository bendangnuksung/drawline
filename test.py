import random
from glob import glob
import cv2
from drawline.draw_process import draw_poly, draw_rect, draw_labelme
import json
import os

from drawline.utils import display, get_biggest_contour, random_resize_and_crop, get_rect_from_poly
from drawline.utils import labelme_to_contours, labelme_to_rect_points, labelme_classify

poly_image_pth = 'test_images/polygon'
rect_image_pth = 'test_images/rectangle'

poly_jsons = glob(os.path.join(poly_image_pth, '*.json'))
rect_json = glob(os.path.join(rect_image_pth, '*.json'))

SHAPE_IMG_PTH = 'test_images/1.jpg'
image = cv2.imread(SHAPE_IMG_PTH)


def test_poly(n=5):
    print("*" * 20, "Test Polygon", "*" * 20)
    for i, pth in enumerate(poly_jsons):
        labelme_dict = json.load(open(pth))
        image_name = labelme_dict['imagePath']
        image_path = os.path.join(poly_image_pth, image_name)
        image = cv2.imread(image_path)
        # contours, labels = labelme_to_contours(labelme_dict)
        if i % 2 == 0:
            # draw_image = draw_poly(image, contours, labels=labels, graph_mode=True)
            draw_image = draw_labelme(image, pth, graph_mode=True)
        else:
            # draw_image = draw_poly(image, contours, labels=labels, graph_mode=True)
            draw_image = draw_labelme(image, pth, graph_mode=False)

        display(draw_image)

    image = cv2.imread(SHAPE_IMG_PTH)
    for i in range(n):
        test_image = image.copy()
        test_image = random_resize_and_crop(test_image)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rects = []
        for contour in contours:
            start_point, end_point = get_rect_from_poly(contour)
            rect = start_point + end_point
            rects.append(rect)

        labels = [f'Label_{i} {str(random.uniform(0, 1))[:4]}' for i in range(len(contours))]
        # test single points
        print(test_image.shape)
        print(len(contours))
        if i == 0:
            test_image = draw_poly(test_image, contours[0], labels=labels[0], graph_mode=True)
        else:
            test_image = draw_poly(test_image, contours, labels=labels, graph_mode=True)

        print(test_image.shape)
        print("*"*30)
        try:
            display(test_image)
        except:
            pass


def test_rect(n=5):
    print("*"*20, "Test Rectangle", "*"*20)

    for pth in rect_json:
        labelme_dict = json.load(open(pth))
        image_name = labelme_dict['imagePath']
        image_path = os.path.join(rect_image_pth, image_name)
        image = cv2.imread(image_path)
        points, labels = labelme_to_rect_points(labelme_dict)
        # draw_image = draw_rect(image, points, labels=labels)
        draw_image = draw_labelme(image, pth, graph_mode=False)
        display(draw_image)

    image = cv2.imread(SHAPE_IMG_PTH)
    for i in range(n):
        test_image = image.copy()
        test_image = random_resize_and_crop(test_image)
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        rects = []
        for contour in contours:
            start_point, end_point = get_rect_from_poly(contour)
            rect = start_point + end_point
            rects.append(rect)

        labels = [f'Label_{i}' for i in range(len(contours))]
        if i == 0:
            test_image = draw_rect(test_image, rects[0], labels=labels[0], graph_mode=True)
        else:
            test_image = draw_rect(test_image, rects, labels=labels, graph_mode=True)
        display(test_image)


if __name__ == '__main__':
    # test_rect()
    test_poly()
    test_rect()

