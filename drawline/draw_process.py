import cv2
from drawline.color_process import get_color
from drawline.utils import get_best_line_size, get_rect_from_poly, prepare_val_contours, prepare_labels, prepare_points
from drawline.utils import split_label_and_non_label_text, get_best_font_thickness_line, get_best_font_size
import numpy as np


def draw_text(img, text, pos, pos_end, text_color=(255, 255, 255), text_color_bg=(0, 0, 0), font_scale=None, s=400,
              font=cv2.FONT_HERSHEY_SIMPLEX, min_font_scale=0.35):
    h_s = img.shape[0] / s
    w_s = img.shape[1] / s
    line_size = int((h_s + w_s) / 3)
    line_size = max([line_size, 1])

    font_thickness = int(get_best_font_thickness_line(img) / 1)
    if font_scale is None:
        font_scale = get_best_font_size(font_thickness)
        # highest_length = max(img.shape[:2])
        # font_scale = highest_length / int(450 * 5)
        # font_scale = max([font_scale, min_font_scale])
        # font_scale = font_scale * 1.35

    # print("thickenss: ", font_thickness, ", size: ", font_scale, ", line size: ", line_size, ', img size: ', img.shape[:2], ' ', sum(img.shape[:2]))

    # https://stackoverflow.com/questions/60674501/how-to-make-black-background-in-cv2-puttext-with-python-opencv
    # Customization of the top answer
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    org = (int(x), int(y + font_scale - 1))
    start_rect_point = (x, y - text_h)
    end_rect_point = (x + text_w, y)

    # Label on top
    if org[1] > 0:
        cv2.rectangle(img, start_rect_point, end_rect_point, text_color_bg, -line_size)
        cv2.putText(img, text, org, font, font_scale, text_color, font_thickness)

    # label on bottom
    else:
        new_pos = (pos[0], pos_end[1])
        x, y = new_pos
        text_w, text_h = text_size
        cv2.rectangle(img, new_pos, (x + text_w, y + text_h), text_color_bg, -line_size)
        org = (x, int(y + text_h + font_scale - 1))
        cv2.putText(img, text, org, font, font_scale, text_color, font_thickness)

    return


def draw_rect(image, points, rgb=None, thickness=None, labels=None,
              label_rgb=(255, 255, 255), label_bg_rgb=None, label_font_size=None,
              random_color=True):
    """
    Draws rectangle from given coordinates
    :param image: (Numpy) numpy matrix image
    :param points: (List) List of rectangle coordinates: [[xmin, ymin, xmax, ymax]]
    :param rgb: (Tuple) RGB values: (R, G, B)
    :param thickness: (Integer) of line in px: eg: 2
    :param labels: (List) list of strings: []
    :param label_rgb: (Tuple) RGB text color for labels: (R,G,B)
    :param label_bg_rgb: (Tuple) RGB label background color: (R,G,B)
    :param label_font_size: (Integer) Font size of label in px: 2
    :param random_color: (Boolean) pick random colors for lines.
    :return: (numpy) image with rectangles
    """
    points = prepare_points(points)
    labels = prepare_labels(points, labels)
    copy_image = image.copy()

    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True

    for point, label in zip(points, labels):
        xmin, ymin, xmax, ymax = point
        start_point = (xmin, ymin)
        end_point = (xmax, ymax)
        label, non_label = split_label_and_non_label_text(label)
        if label is None:
            label_non_label_combined = None
        else:
            non_label = non_label if non_label != '' else ' ' + non_label
            label_non_label_combined = label + non_label

        if not rgb_flag:
            rgb = get_color(label, 'draw_rect', is_random=random_color)
        if not thickness_flag:
            thickness = get_best_line_size(copy_image)

        cv2.rectangle(copy_image, start_point, end_point, rgb, thickness)
        if label is not None:
            if not label_bg_rgb_flag:
                label_bg_rgb = rgb
            draw_text(copy_image, label_non_label_combined, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb, font_scale=label_font_size)
    return copy_image


def fill_in_poly(contour, image, rgb, alpha=0.4):
    overlay = image.copy()
    cv2.fillPoly(overlay, pts=[contour], color=rgb)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image_new


def draw_poly(image, contours, fill_in=True, transparency=0.4, rgb=None, thickness=None, show_rect=True, labels=None,
              label_rgb=(255, 255, 255), label_bg_rgb=None, label_font_size=None, random_color=True):
    """
    Draws polygon and fills in color from given contours
    :param image: (Numpy) numpy matrix image
    :param contours: (List) of contours
    :param fill_in: (Boolean) fill color inside the polygon.
    :param transparency: (Float) transparency of fill_in color.
    :param rgb: RGB values: (Tuple) rgb color of line and polyfgon (R, G, B)
    :param thickness: (Int) Thickness of line
    :param show_rect: (Boolean) Show rectangle
    :param labels: (List of strings) List of label names
    :param label_rgb: (Tuple) RGB color of labels
    :param label_bg_rgb: (Tuple) RGB color of Label background
    :param label_font_size: (Int) Label font size
    :param random_color: (Boolean) Randomize RGB color
    :return:
    """

    contours = prepare_val_contours(contours)
    labels = prepare_labels(contours, labels)
    copy_image = image.copy()
    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True

    for label, contour in zip(labels, contours):
        if len(contour.shape) == 1:
            continue

        label, non_label = split_label_and_non_label_text(label)
        if label is None:
            label_non_label_combined = None
        else:
            non_label = non_label if non_label != '' else ' ' + non_label
            label_non_label_combined = label + non_label

        start_point, end_point = get_rect_from_poly(contour)

        if not rgb_flag:
            rgb = get_color(label, 'draw_rect', is_random=random_color)
        if not thickness_flag:
            thickness = get_best_line_size(copy_image)

        if show_rect:
            cv2.rectangle(copy_image, start_point, end_point, rgb, thickness)

        if label is not None:
            if not label_bg_rgb_flag:
                label_bg_rgb = rgb
            draw_text(copy_image, label_non_label_combined, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb,
                      font_scale=label_font_size)

        cv2.drawContours(copy_image, [contour], -1, rgb, thickness)
        if fill_in:
            copy_image = fill_in_poly(contour, copy_image, rgb, alpha=transparency)

    return copy_image

