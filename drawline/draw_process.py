import cv2
from drawline.color_process import get_color
from drawline.utils import get_best_line_size, get_rect_from_poly
import numpy as np


def draw_text(img, text, pos, pos_end, text_color=(255, 255, 255), text_color_bg=(0, 0, 0), font_scale=None, s=400, font=cv2.FONT_HERSHEY_SIMPLEX, min_font_scale=0.35):
    h_s = img.shape[0] / s
    w_s = img.shape[1] / s
    line_size = int((h_s + w_s) / 3)
    line_size = max([line_size, 1])

    if font_scale is None:
        highest_length = max(img.shape[:2])
        font_scale = highest_length / int(450 * 5)
        font_scale = max([font_scale, min_font_scale])

    font_thickness = int(get_best_line_size(img) / 1.3)
    print("thickenss: ", font_thickness, ", size: ", font_scale, ", line size: ", line_size)

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
        # print(org, start_rect_point, end_rect_point)
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


def draw_rect(image, start_point, end_point, rgb=None, thickness=None,
              label=None, label_rgb=(255, 255, 255), label_bg_rgb=None, label_font_size=None,
              random_color=True):
    copy_image = image.copy()
    if rgb is None:
        rgb = get_color(label, 'draw_rect', is_random=random_color)
    if thickness is None:
        thickness = get_best_line_size(copy_image)

    cv2.rectangle(copy_image, start_point, end_point, rgb, thickness)
    if label is not None:
        if label_bg_rgb is None:
            label_bg_rgb = rgb
        draw_text(copy_image, label, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb, font_scale=label_font_size)
    return copy_image


def fill_in_poly(contour, image, rgb, alpha=0.4):
    overlay = image.copy()
    cv2.fillPoly(overlay, pts=[contour], color=rgb)
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
    return image_new


def draw_poly(image, contour, fill_in=True, transparency=0.4, rgb=None, thickness=None, show_rect=True, label=None, label_rgb=(255, 255, 255),
              label_bg_rgb=None, label_font_size=None, random_color=True):
    copy_image = image.copy()
    if type(contour) == list:
        contour = np.array(contour)
    start_point, end_point = get_rect_from_poly(contour)

    if rgb is None:
        rgb = get_color(label, 'draw_rect', is_random=random_color)
    if thickness is None:
        thickness = get_best_line_size(copy_image)

    if show_rect:
        cv2.rectangle(copy_image, start_point, end_point, rgb, thickness)
    if label is not None:
        if label_bg_rgb is None:
            label_bg_rgb = rgb
        draw_text(copy_image, label, start_point, end_point, text_color=label_rgb, text_color_bg=label_bg_rgb,
                  font_scale=label_font_size)

    contour = np.squeeze(contour)
    if fill_in:
        copy_image = fill_in_poly(contour, copy_image, rgb, alpha=transparency)

    else:
        cv2.drawContours(copy_image, [contour], -1, rgb, thickness)

    return copy_image

