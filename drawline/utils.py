import matplotlib.pyplot as plt
import random
import numpy as np
import cv2


def display(img):
    plt.imshow(img)
    plt.show()


def get_biggest_contour(contours, reverse=False):
    biggest_contour = None
    for cnt in contours:
        if biggest_contour is None:
            biggest_contour = cnt
        else:
            if reverse:
                if cnt.shape[0] < biggest_contour.shape[0]:
                    biggest_contour = cnt
            else:
                if cnt.shape[0] > biggest_contour.shape[0]:
                    biggest_contour = cnt
    return biggest_contour


def get_best_line_size(image):
    height, width = image.shape[:2]
    min_length = min([height, width])
    # area = height * width
    area = min_length ** 2
    size = int(((area * 2) / 1000000))
    # print(area)
    return size


def random_crop(image):
    height, width = image.shape[:2]
    start_x = random.randint(0, width // 1.8)
    start_y = random.randint(0, height // 1.8)

    end_x = random.randint(width // 2, width)
    end_y = random.randint(height // 2, height)
    image = image[start_y:end_y, start_x: end_x]
    return image


def random_resize(cimg):
    pos_neg = -1 if random.randint(0, 1) else 1
    if pos_neg < 0:
        r = random.uniform(0.5, 0.85)
        r = pos_neg * r
    else:
        r = random.uniform(0.5, 1.25)
        r = pos_neg * r

    height, width = cimg.shape[:2]
    new_height = int(height * (1 + r))
    new_width = int(width * (1 + r))
    cimg = cv2.resize(cimg, (new_width, new_height))
    return cimg


def prepare_points(points):
    new_points = []
    points = np.array(points)
    points = np.squeeze(points)
    if len(points.shape) > 1:
        for p in points:
            new_points.append(p)
    else:
        new_points.append(points)
    return new_points


def prepare_val_contours(contours):
    if type(contours) == list:
        contours = np.array(contours)

    new_contours = []

    if len(contours.shape) == 1:
        for contour in contours:
            contour = np.squeeze(contour)
            new_contours.append(contour)
    else:
        contours = np.squeeze(contours)
        try:
            assert len(contours.shape) == 2
        except:
            print("Contour shape not proper: ", contours.shape)
        new_contours.append(contours)

    return new_contours


def prepare_labels(contours, labels):
    new_labels = []
    for i in range(len(contours)):
        if type(labels) == list:
            new_labels.append(labels[i])
        elif type(labels) == str:
            new_labels.append(labels)
        else:
            new_labels.append(None)
    return new_labels


def random_resize_and_crop(image):
    cimg = image.copy()
    cimg = random_crop(cimg)
    cimg = random_resize(cimg)
    return cimg


def get_rect_from_poly(contour):
    try:
        (x, y, w, h) = cv2.boundingRect(contour)
    except Exception as e:
        pass
    start_point = (x, y)
    end_point = (x + w, y + h)
    return start_point, end_point