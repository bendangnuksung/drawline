import math

import matplotlib.pyplot as plt
import random
import numpy as np
import cv2


def display(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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


def get_best_font_thickness_line(image):
    height, width = image.shape[:2]
    max_length = max([height, width])
    size = int(max_length / 500)

    off = 4
    if size > off:
        extra_offset = size - off
        size = off + (extra_offset // 3)

    return size


def get_best_font_size(font_thickness, r=0.5):
    font_size = r * font_thickness
    if font_size == 0:
        font_size = r
    return font_size


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

    end_x = random.randint((width // 2) + 10, width)
    end_y = random.randint((height // 2) + 10, height)
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
    new_height = max([new_height, 30])
    new_width = max([new_width, 30])
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


def get_contour_areas(contours):
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas


def sort_contours_by_area(contours, labels):
    temp = []
    for cnt, label in zip(contours, labels):
        cnt = cnt.astype(np.int)
        area = cv2.contourArea(cnt)
        temp.append([area, cnt, label])
    sorted_contours = sorted(temp, key=lambda x: x[0], reverse=True)
    sorted_contours = np.array(sorted_contours)
    sorted_labels = list(sorted_contours[:, 2])
    sorted_contours = list(sorted_contours[:, 1])
    return sorted_contours, sorted_labels


def prepare_val_contours(contours):
    if type(contours) in [list, tuple]:
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
    while True:
        tmp = random_crop(cimg)
        if tmp.shape[0] > 0 and tmp.shape[1] > 0:
            cimg = tmp
            break
    cimg = random_resize(cimg)
    return cimg


def get_rect_from_poly(contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    start_point = (x, y)
    end_point = (x + w, y + h)
    return start_point, end_point


def split_label_and_non_label_text(label):
    if label is None:
        return None, None
    label = label.strip()
    splitted = label.split()
    label = splitted[0]
    non_label = ' '.join(splitted[1:])
    return label, non_label


# https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


def is_coords_intersecting(new_coord, used_coords_list, max_threshold=0.6):
    for coords in used_coords_list:
        iou = bb_intersection_over_union(new_coord, coords)
        if iou > max_threshold:
            return True
    return False


# https://stackoverflow.com/questions/22603510/is-this-possible-to-detect-a-colour-is-a-light-or-dark-colour
def is_color_light(rgb):
    [r, g, b] = rgb
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if hsp > 127.5:
        return True
    else:
        return False


def labelme_classify(l_dict):
    l_type = l_dict['shapes'][0]['shape_type']
    if l_type is None:
        return 'empty'
    elif l_type == 'rectangle':
        return 'rectangle'
    elif l_type == 'polygon':
        return 'polygon'


def labelme_to_contours(l_dict):
    labels = []
    contours = []
    for s in l_dict['shapes']:
        label = s['label']
        contour = s['points']
        labels.append(label)
        contours.append(contour)
    return contours, labels


def labelme_to_rect_points(l_dict):
    labels = []
    points = []
    for s in l_dict['shapes']:
        label = s['label']
        point = [int(s['points'][0][0]), int(s['points'][0][1]), int(s['points'][1][0]), int(s['points'][1][1])]
        labels.append(label)
        points.append(point)
    return points, labels


if __name__ == '__main__':
    rgb = (152,251,152)

    print(is_color_light(rgb))