import cv2
from drawline.color_process import get_color
from drawline.utils import get_best_line_size, get_rect_from_poly, prepare_val_contours, prepare_labels, prepare_points
from drawline.utils import split_label_and_non_label_text, get_best_font_thickness_line, get_best_font_size
from drawline.utils import is_coords_intersecting, sort_contours_by_area
from drawline.cv_utils import get_font_color, write_info_to_border
from drawline.utils import labelme_to_contours, labelme_to_rect_points
import json
import numpy as np

COORDS_USED = []


def reset_variables():
    global COORDS_USED
    COORDS_USED = []


def get_coords_for_labels(pos, pos_end, img, text, font, font_scale, font_thickness):
    global COORDS_USED
    height, width = img.shape[:2]
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    backup_result = None

    # top left position
    x, y = pos
    text_pos = (int(x), int(y + font_scale - 1))
    xmin = x
    ymin = y - text_h
    xmax = x + text_w
    ymax = y
    intersecting = is_coords_intersecting([xmin, ymin, xmax, ymax], COORDS_USED)
    if not intersecting and text_pos[1] > 0:
        COORDS_USED.append([xmin, ymin, xmax, ymax])
        return [xmin, ymin, xmax, ymax], text_pos

    if not intersecting:
        backup_result = [xmin, ymin, xmax, ymax], text_pos

    # top right position
    x = pos_end[0] - text_w
    y = pos[1]
    text_pos = (int(x), int(y + font_scale - 1))
    xmin = x
    ymin = y - text_h
    xmax = x + text_w
    ymax = y
    intersecting = is_coords_intersecting([xmin, ymin, xmax, ymax], COORDS_USED)
    if not intersecting:
        backup_result = [xmin, ymin, xmax, ymax], text_pos
    if not intersecting and text_pos[1] > 0:
        COORDS_USED.append([xmin, ymin, xmax, ymax])
        return [xmin, ymin, xmax, ymax], text_pos

    # bot left position
    xmin = pos[0]
    ymin = pos_end[1]
    xmax = pos[0] + text_w
    ymax = pos_end[1] + text_h
    text_pos = (xmin, int(ymin + text_h + font_scale - 1))
    intersecting = is_coords_intersecting([xmin, ymin, xmax, ymax], COORDS_USED)
    if not intersecting and text_pos[1] < height:
        COORDS_USED.append([xmin, ymin, xmax, ymax])
        return [xmin, ymin, xmax, ymax], text_pos

    if not intersecting:
        backup_result = [xmin, ymin, xmax, ymax], text_pos

    # bot right position
    xmin = pos_end[0] - text_w
    ymin = pos_end[1]
    xmax = xmin + text_w
    ymax = ymin + text_h
    text_pos = (xmin, int(ymin + text_h + font_scale - 1))
    intersecting = is_coords_intersecting([xmin, ymin, xmax, ymax], COORDS_USED)
    if not intersecting and text_pos[1] < height:
        COORDS_USED.append([xmin, ymin, xmax, ymax])
        return [xmin, ymin, xmax, ymax], text_pos

    if not intersecting:
        backup_result = [xmin, ymin, xmax, ymax], text_pos

    return backup_result


def draw_text(img, text, pos, pos_end, label_transparency=0.4, text_color=(255, 255, 255), text_color_bg=(0, 0, 0),
              font_scale=None, s=400, font=cv2.FONT_HERSHEY_SIMPLEX):
    overlay = img.copy()
    h_s = img.shape[0] / s
    w_s = img.shape[1] / s
    line_size = int((h_s + w_s) / 3)
    line_size = max([line_size, 1])

    font_thickness = get_best_font_thickness_line(img)
    if font_scale is None:
        font_scale = get_best_font_size(font_thickness)

    # print("thickenss: ", font_thickness, ", size: ", font_scale, ", line size: ", line_size, ', img size: ', img.shape[:2], ' ', sum(img.shape[:2]))

    rect_coords, text_coords_pos = get_coords_for_labels(pos, pos_end, img, text, font, font_scale, font_thickness)
    cv2.rectangle(img, (rect_coords[0], rect_coords[1]), (rect_coords[2], rect_coords[3]), text_color_bg, -line_size)
    cv2.putText(img, text, text_coords_pos, font, font_scale, text_color, font_thickness)

    img = cv2.addWeighted(overlay, label_transparency, img, 1 - label_transparency, 0)

    return img


def draw_rect(image, points, rgb=None, label_transparency=0.1, thickness=None, labels=None,
              label_rgb=None, label_bg_rgb=None, label_font_size=None,
              random_color=False, graph_mode=False):
    """
    Draws rectangle from given coordinates
    :param image: (Numpy) numpy matrix image
    :param points: (List) List of rectangle coordinates: [[xmin, ymin, xmax, ymax]]
    :param rgb: (Tuple) RGB values: (R, G, B)
    :param label_transparency: (float) transparency for the labels
    :param thickness: (Integer) of line in px: eg: 2
    :param labels: (List) list of strings: []
    :param label_rgb: (Tuple) RGB text color for labels: (R,G,B)
    :param label_bg_rgb: (Tuple) RGB label background color: (R,G,B)
    :param label_font_size: (Integer) Font size of label in px: 2
    :param random_color: (Boolean) pick random colors for lines.
    :param graph_mode: (Boolean) Writes labels to a border instead in the image itself (Good to use when to many boxes obstructing the view)

    :return: (numpy) drawn rectangles on image
    """

    reset_variables()
    points = prepare_points(points)
    labels = prepare_labels(points, labels)
    copy_image = image.copy()

    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True
    label_bg_flag = False if label_rgb is None else True

    graph_labels_and_colors = {}
    graph_text_labels = {}

    # if rgb is not None:
    #     # cvt RGB to BGR as cv2 uses BGR format
    #     rgb = rgb[::-1]

    for i, (point, label) in enumerate(zip(points, labels), 1):
        xmin, ymin, xmax, ymax = point
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin

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

            if not label_bg_flag:
                label_rgb = get_font_color(label_bg_rgb)

            if graph_mode:
                graph_labels_and_colors[label] = label_bg_rgb
                graph_text_labels[i] = label + ' ' + non_label
                label_non_label_combined = str(i)

            copy_image = draw_text(copy_image, label_non_label_combined, start_point, end_point,
                                   label_transparency=label_transparency, text_color=label_rgb,
                                   text_color_bg=label_bg_rgb, font_scale=label_font_size)

    if graph_mode:
        copy_image = write_info_to_border(copy_image, graph_labels_and_colors, graph_text_labels)

    return copy_image


def fill_in_poly(contour, image, rgb, alpha=0.4):
    overlay = image.copy()
    cv2.fillPoly(overlay, pts=[contour], color=rgb)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image_new


def draw_poly(image, contours, fill_in=True, label_transparency=0.1, fill_transparency=0.4, rgb=None, thickness=None,
              show_rect=True, labels=None, label_rgb=None, label_bg_rgb=None, label_font_size=None, random_color=False,
              graph_mode=False):
    """
    Draws polygon and fills in color from given contours
    :param image: (Numpy) numpy matrix image
    :param contours: (List) of contours
    :param fill_in: (Boolean) fill color inside the polygon.
    :param label_transparency: (float) transparency for the labels
    :param fill_transparency: (Float) transparency of fill_in color.
    :param rgb: RGB values: (Tuple) rgb color of line and polyfgon (R, G, B)
    :param thickness: (Int) Thickness of line
    :param show_rect: (Boolean) Show rectangle
    :param labels: (List of strings) List of label names
    :param label_rgb: (Tuple) RGB color of labels
    :param label_bg_rgb: (Tuple) RGB color of Label background
    :param label_font_size: (Int) Label font size
    :param random_color: (Boolean) Randomize RGB color
    :param graph_mode: (Boolean) Writes labels to a border instead in the image itself (Good to use when to many boxes obstructing the view)

    :return: (Numpy) drawn polygon on image
    """
    reset_variables()
    contours = prepare_val_contours(contours)
    labels = prepare_labels(contours, labels)
    contours, labels = sort_contours_by_area(contours, labels)
    copy_image = image.copy()
    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True
    label_bg_flag = False if label_rgb is None else True

    graph_labels_and_colors = {}
    graph_text_labels = {}

    # if rgb is not None:
    #     # cvt RGB to BGR as cv2 uses BGR format
    #     rgb = rgb[::-1]

    for i, (label, contour) in enumerate(zip(labels, contours), 1):
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

            if not label_bg_flag:
                label_rgb = get_font_color(label_bg_rgb)

            if graph_mode:
                graph_labels_and_colors[label] = label_bg_rgb
                graph_text_labels[i] = label + ' ' + non_label
                label_non_label_combined = str(i)

            if not show_rect:
                all_x, all_y = contour[:, 0], contour[:, 1]
                min_y_index = np.where(all_y == (min(all_y)))[0][0]
                max_y_index = np.where(all_y == (max(all_y)))[0][0]
                start_point = contour[min_y_index]
                end_point = contour[max_y_index]

            copy_image = draw_text(copy_image, label_non_label_combined, start_point, end_point,
                                   label_transparency=label_transparency, text_color=label_rgb,
                                   text_color_bg=label_bg_rgb, font_scale=label_font_size)

        cv2.drawContours(copy_image, [contour], -1, rgb, thickness)
        if fill_in:
            copy_image = fill_in_poly(contour, copy_image, rgb, alpha=fill_transparency)

    if graph_mode:
        copy_image = write_info_to_border(copy_image, graph_labels_and_colors, graph_text_labels)

    return copy_image


def draw_labelme(image, labelme_dict, fill_in=True, label_transparency=0.1, fill_transparency=0.4, rgb=None, thickness=None,
              show_rect=True, labels=None, label_rgb=None, label_bg_rgb=None, label_font_size=None, random_color=False,
              graph_mode=False):
    """
    Draws polygon or rectangle from the LabelMe annotation file
    :param image: (Numpy) numpy matrix image
    :param labelme_dict: (str or dict) path to the LabelMe json file path or dictionary
    :param fill_in: (Boolean) fill color inside the polygon.
    :param label_transparency: (float) transparency for the labels
    :param fill_transparency: (Float) transparency of fill_in color.
    :param rgb: RGB values: (Tuple) rgb color of line and polyfgon (R, G, B)
    :param thickness: (Int) Thickness of line
    :param show_rect: (Boolean) Show rectangle
    :param labels: (List of strings) List of label names
    :param label_rgb: (Tuple) RGB color of labels
    :param label_bg_rgb: (Tuple) RGB color of Label background
    :param label_font_size: (Int) Label font size
    :param random_color: (Boolean) Randomize RGB color
    :param graph_mode: (Boolean) Writes labels to a border instead in the image itself (Good to use when to many boxes obstructing the view)

    :return: (Numpy) drawn polygon on image
    """

    assert type(labelme_dict) in [dict, str], "labelme_dict type should be either 1. (str) Path of the json file or 2. (dict) Json loaded"

    if type(labelme_dict) == str:
        with open(labelme_dict) as f:
            labelme_dict = json.load(f)
        # labelme_dict = json.load(open(labelme_dict))

    try:
        shape_type = labelme_dict["shapes"][0]["shape_type"]
    except Exception as e:
        shape_type = None

    if shape_type == "polygon":
        contours, labels_text = labelme_to_contours(labelme_dict)
        draw_image = draw_poly(image, contours, fill_in=fill_in, label_transparency=label_transparency,
                               fill_transparency=fill_transparency, rgb=rgb, thickness=thickness, show_rect=show_rect,
                               labels=labels_text, label_rgb=label_rgb, label_bg_rgb=label_bg_rgb,
                               label_font_size=label_font_size, random_color=random_color, graph_mode=graph_mode)

    elif shape_type == "rectangle":
        points, labels_text = labelme_to_rect_points(labelme_dict)
        draw_image = draw_rect(image, points, labels=labels_text, rgb=rgb, label_transparency=label_transparency,
                               thickness=thickness, label_rgb=label_rgb, label_bg_rgb=label_bg_rgb,
                               label_font_size=label_font_size,random_color=random_color, graph_mode=graph_mode)

    else:
        draw_image = image

    return draw_image



