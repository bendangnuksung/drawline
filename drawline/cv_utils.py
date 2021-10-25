import numpy as np
import cv2
import matplotlib.pyplot as plt
from drawline.utils import get_best_font_thickness_line, get_best_font_size, is_color_light, split_label_and_non_label_text


def get_font_color(bg_color):
    light_color = is_color_light(bg_color)

    if light_color:
        return (0, 0, 0)
    else:
        return (255, 255, 255)


def display(img):
    plt.imshow(img)
    plt.show()


def get_border_image(image, percentage, rgb=(255, 255, 255)):
    height, width = image.shape[:2]
    # max_length = height if height > width else width
    # right_px = int(percentage * max_length)
    right_px = int(percentage * ((height + width)/2))
    # image = cv2.copyMakeBorder(image, 0, 0, 0, right_px, cv2.BORDER_CONSTANT, None, value=rgb)
    border_image = (np.ones((height, right_px, 3), dtype=np.uint8) * rgb).astype(np.uint8)
    return border_image


def make_color_palette_image(height, width, rgb, channel=3):
    img = np.ones((height, width, channel), dtype=np.uint8)
    img = (img * rgb).astype(np.uint8)
    return img


def extend_border_width(image, my_width, rgb=(255, 255, 255), extra_padding=0.02):
    height, width = image.shape[:2]
    if width <= my_width:
        width_needed = my_width - width + int(width * extra_padding)
        image = cv2.copyMakeBorder(image, 0, 0, 0, width_needed, cv2.BORDER_CONSTANT, None, value=rgb)
    return image


def write_header_on_border(image, border_image, labels_and_colors, height_percen=0.25):
    font_thickness = get_best_font_thickness_line(image)
    font_scale = max([(get_best_font_size(font_thickness) - 0.2), 0.4])

    text_size, _ = cv2.getTextSize(' ', cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    text_w, text_h = text_size
    one_letter_space = text_w

    new_height = int(border_image.shape[0] * height_percen)
    cropped_image = border_image[:new_height, :]

    cropped_image_height, cropped_image_width = cropped_image.shape[:2]

    color_palette_size = (int(text_h/1), int(text_h/1))

    start_x = 0 + int(border_image.shape[1] * 0.1)
    start_y = 0 + int(border_image.shape[1] * 0.15)

    last_x = start_x
    last_y = start_y

    col_offset = 0
    row_offset = text_h // 2

    for label, rgb in labels_and_colors.items():
        palette_image = make_color_palette_image(color_palette_size[0], color_palette_size[1], rgb)
        label = '  ' + label
        text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_w, text_h = text_size
        single_text_w = text_w / len(label)

        last_y = last_y + text_h
        text_coords_pos = (last_x, last_y)
        # print(text_coords_pos, text_h, font_scale, font_thickness)
        cropped_image = extend_border_width(cropped_image, last_x + text_w + int(single_text_w * 2))

        cv2.putText(cropped_image, label, text_coords_pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness)
        palette_xmin = last_x
        palette_ymin = last_y - text_h
        palette_xmax = last_x + color_palette_size[0]
        palette_ymax = last_y - text_h + color_palette_size[1]

        cs = cropped_image[palette_ymin: palette_ymax, palette_xmin: palette_xmax].shape[:2]
        if palette_image.shape[:2] != cs:
            palette_image = cv2.resize(palette_image, (cs[1], cs[0]))

        cropped_image[palette_ymin: palette_ymax, palette_xmin: palette_xmax] = palette_image
        # display(cropped_image)
        last_y += row_offset + text_h

        if text_w > col_offset:
            col_offset = text_w

        if (last_y + text_h) > cropped_image_height:
            last_y = start_y
            last_x = last_x + col_offset + one_letter_space
            col_offset = 0

        # break
    border_image = extend_border_width(border_image, cropped_image.shape[1], extra_padding=0)

    # cropped_image =

    border_image[:new_height, :] = cropped_image
    return border_image


def write_body_on_border(image, border_image, labels_and_colors, text_info, body_percen):
    font_thickness = get_best_font_thickness_line(image)
    font_scale = max([(get_best_font_size(font_thickness) - 0.2), 0.4])

    text_size, _ = cv2.getTextSize(' ', cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    text_w, text_h = text_size
    one_letter_space = text_w

    new_height = border_image.shape[0] - int(border_image.shape[0] * body_percen)
    cropped_image = border_image[new_height:, :]

    cropped_image_height, cropped_image_width = cropped_image.shape[:2]

    start_x = text_h #int(border_image.shape[1] * 0.07)
    start_y = text_h #int(border_image.shape[0] * 0.1)

    last_x = start_x
    last_y = start_y

    col_offset = 0
    row_offset = text_h // 2

    len_str_items = len(str(len(text_info))) + 2

    for number, text in text_info.items():
        org_text = text
        label_name, _ = split_label_and_non_label_text(text)
        rgb = labels_and_colors[label_name]
        str_number = str(number)
        number_string = str_number + ' '*(len_str_items - len(str_number))
        text = ' '*len(number_string) + text
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_w, text_h = text_size
        single_text_w = text_w / len(text)
        last_y = last_y + text_h
        text_coords_pos = (last_x, last_y)

        color_coords_pos = (last_x + int(len(number_string) * single_text_w), last_y)
        # print(text_coords_pos, text_h, font_scale, font_thickness)
        cropped_image = extend_border_width(cropped_image, last_x + text_w + int(single_text_w*2))

        color_rect_xmin = color_coords_pos[0]
        color_rect_ymin = color_coords_pos[1] - text_h
        color_rect_xmax = color_coords_pos[0] + (single_text_w * len(org_text))
        color_rect_ymax = color_coords_pos[1]

        try:
            padded_xmin = int(color_rect_xmin - (text_w * 0.025))
            padded_ymin = int(color_rect_ymin - (text_h * 0.25))
            padded_xmax = int(color_rect_xmax + (text_w * 0.025))
            padded_ymax = int(color_rect_ymax + (text_h * 0.25))
            cropped_image = cv2.rectangle(cropped_image, (padded_xmin, padded_ymin), (padded_xmax, padded_ymax), rgb, -1)

        except Exception as e:
            print(e)
            cropped_image = cv2.rectangle(cropped_image, (color_rect_xmin, color_rect_ymin), (color_rect_xmax, color_rect_ymax), rgb, -1)

        font_color = get_font_color(rgb)
        cv2.putText(cropped_image, text, text_coords_pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_color, font_thickness)
        cv2.putText(cropped_image, number_string, text_coords_pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0),
                    font_thickness)

        last_y += row_offset + text_h

        if text_w > col_offset:
            col_offset = text_w

        if (last_y + text_h) > cropped_image_height:
            last_y = start_y
            last_x = last_x + col_offset + (one_letter_space * 3)
            col_offset = 0

    border_image = extend_border_width(border_image, cropped_image.shape[1], extra_padding=0)
    cropped_image = cv2.rectangle(cropped_image, (2, 0), (cropped_image.shape[1]-2, cropped_image.shape[0]), (0, 0, 0),
                                  thickness=font_thickness*2)
    border_image[new_height:, :] = cropped_image
    border_image = cv2.rectangle(border_image, (2, 0), (border_image.shape[1] - 2, border_image.shape[0]), (0, 0, 0),
                                 thickness=font_thickness * 2)

    return border_image


def add_padding(image):
    height, width = image.shape[:2]
    if height == width:
        return image

    elif height > width:
        to_add = (height - width) // 2
        width_padding = np.ones([height, to_add, 3], dtype=np.uint8) * 255
        image = np.concatenate([width_padding, image, width_padding], axis=1)

    else:
        to_add = (width - height) // 2
        height_padding = np.ones([to_add, width, 3], dtype=np.uint8) * 255
        image = np.concatenate([height_padding, image, height_padding], axis=0)
    return image


def write_info_to_border(image, labels_and_colors, text_info, border_percen=0.2, header_percen=0.3):
    image = add_padding(image)
    border_image = get_border_image(image, border_percen)
    body_percen = 1 - header_percen
    border_image = write_header_on_border(image, border_image, labels_and_colors, height_percen=header_percen)
    border_image = write_body_on_border(image, border_image, labels_and_colors, text_info, body_percen=body_percen)

    full_image = np.concatenate([image, border_image], axis=1)
    return full_image


if __name__ == '__main__':
    from drawline.utils import random_resize_and_crop
    import random

    image_org = cv2.imread('../test_images/1.jpg')
    for i in range(10):
        image = image_org.copy()
        image = random_resize_and_crop(image)
        # image = cv2.imread('/home/ben/Downloads/damage_car_image/1.jpg')
        labels_and_colors = {'label1': (0, 255, 0), 'label2': (255,0,0), 'label3': (0,0,255),
                             'label4': (0, 255, 255), 'label5': (255,0,255), 'label6': (0,128,255),
                             'label7': (128, 128, 255), 'label8': (128,0,0), 'label9': (100,128,100),
                             'label10': (0, 255, 100), 'label11': (60,120,180), 'label12': (50,100,50),
                             'label13': (0, 255, 100), 'label14': (60,120,180), 'label15': (50,100,50),}

        n = random.randint(10, 20)
        text_info = {}
        for j in range(n):
            label = 'label' + str(random.randint(1, 15)) + ' ' + str(random.uniform(0.01, 0.99))[:4]
            text_info[str(j)] = label
        # text_info = {'1': 'label1 0.01', '2': 'label3 0.2'}

        new_image = write_info_to_border(image, labels_and_colors, text_info)
        # display(new_image)
        pass


