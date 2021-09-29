import cv2
from drawline.color_process import get_color
from drawline.utils import get_best_line_size, get_rect_from_poly, prepare_val_contours, prepare_labels, prepare_points
from drawline.utils import split_label_and_non_label_text, get_best_font_thickness_line, get_best_font_size
from drawline.utils import is_coords_intersecting, get_font_color

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


def draw_text(img, text, pos, pos_end, text_color=(255, 255, 255), text_color_bg=(0, 0, 0), font_scale=None, s=400,
              font=cv2.FONT_HERSHEY_SIMPLEX):

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

    return


def draw_rect(image, points, rgb=None, thickness=None, labels=None,
              label_rgb=None, label_bg_rgb=None, label_font_size=None,
              random_color=False):
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

    reset_variables()
    points = prepare_points(points)
    labels = prepare_labels(points, labels)
    copy_image = image.copy()

    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True
    label_bg_flag = False if label_rgb is None else True

    if rgb is not None:
        # cvt RGB to BGR as cv2 uses BGR format
        rgb = rgb[::-1]

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

            if not label_bg_flag:
                label_rgb = get_font_color(label_bg_rgb)

            draw_text(copy_image, label_non_label_combined, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb, font_scale=label_font_size)
    return copy_image


def fill_in_poly(contour, image, rgb, alpha=0.4):
    overlay = image.copy()
    cv2.fillPoly(overlay, pts=[contour], color=rgb)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image_new


def draw_poly(image, contours, fill_in=True, transparency=0.4, rgb=None, thickness=None, show_rect=True, labels=None,
              label_rgb=None, label_bg_rgb=None, label_font_size=None, random_color=False):
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
    reset_variables()
    contours = prepare_val_contours(contours)
    labels = prepare_labels(contours, labels)
    copy_image = image.copy()
    rgb_flag = False if rgb is None else True
    thickness_flag = False if thickness is None else True
    label_bg_rgb_flag = False if label_bg_rgb is None else True
    label_bg_flag = False if label_rgb is None else True

    if rgb is not None:
        # cvt RGB to BGR as cv2 uses BGR format
        rgb = rgb[::-1]

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

            if not label_bg_flag:
                label_rgb = get_font_color(label_bg_rgb)

            draw_text(copy_image, label_non_label_combined, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb,
                      font_scale=label_font_size)

        cv2.drawContours(copy_image, [contour], -1, rgb, thickness)
        if fill_in:
            copy_image = fill_in_poly(contour, copy_image, rgb, alpha=transparency)

    return copy_image

