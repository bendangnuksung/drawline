import matplotlib.pyplot as plt
import random
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


def random_resize_and_crop(image):
    cimg = image.copy()
    cimg = random_crop(cimg)
    cimg = random_resize(cimg)
    return cimg


def get_rect_from_poly(contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    start_point = (x, y)
    end_point = (x + w, y + h)
    return start_point, end_point