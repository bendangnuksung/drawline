import random

random.seed(77)

D = [(26, 147, 52), (255, 157, 151), (255, 55, 199), (132, 56, 255), (0, 194, 255), (100, 115, 255), (0, 24, 236),
     (255, 178, 29), (255, 56, 56), (255, 149, 200), (207, 210, 49), (52, 69, 147),
     (72, 249, 10), (61, 219, 134), (0, 212, 187), (146, 204, 23), (82, 0, 133), (255, 112, 31), (44, 153, 168), (203, 56, 255)]

DISTINGUISHABLE_COLORS = D + [(100, 255, 100), (255, 225, 25), (0, 0, 117), (70, 153, 144), (230, 25, 75),
                              (128, 128, 0), (66, 212, 244), (128, 0, 0), (60, 180, 75), (145, 30, 180),
                              (169, 169, 169), (250, 190, 212), (255, 216, 177), (170, 255, 195), (220, 190, 255)]

RGB_COLLECTION_ADDONS = [(0, 255, 127), (250, 128, 114), (25, 25, 112), (60, 179, 113), (216, 191, 216), (211, 211, 211),
                  (255, 127, 80), (169, 169, 169), (238, 130, 238), (70, 130, 180), (255, 240, 245), (85, 107, 47),
                  (224, 255, 255), (64, 224, 208), (0, 0, 255), (47, 79, 79), (245, 222, 179), (255, 255, 240),
                  (112, 128, 144), (138, 43, 226), (176, 224, 230), (255, 192, 203), (255, 127, 0), (230, 230, 250),
                  (65, 105, 225), (135, 206, 235), (128, 0, 0), (255, 182, 193), (240, 230, 140), (244, 164, 96),
                  (255, 99, 71), (255, 20, 147), (240, 255, 240), (255, 69, 0), (34, 139, 34), (0, 206, 209),
                  (178, 34, 34), (205, 92, 92), (107, 142, 35), (0, 0, 139), (255, 218, 185), (0, 255, 0),
                  (245, 255, 250), (50, 205, 50), (255, 105, 180), (123, 104, 238), (255, 228, 181), (189, 183, 107),
                  (255, 255, 224), (154, 205, 50), (255, 165, 0), (255, 0, 255), (218, 112, 214), (75, 0, 130),
                  (255, 228, 225), (255, 222, 173), (250, 250, 210), (0, 0, 205), (250, 240, 230), (127, 255, 212),
                  (219, 112, 147), (199, 21, 133), (46, 139, 87), (0, 139, 139), (255, 160, 122), (102, 205, 170),
                  (255, 215, 0), (255, 228, 196), (240, 255, 255), (128, 128, 128), (128, 128, 0), (30, 144, 255),
                  (135, 206, 250), (147, 112, 219), (210, 180, 140), (255, 255, 0), (153, 50, 204), (160, 82, 45),
                  (148, 0, 211), (128, 0, 128), (188, 143, 143), (245, 245, 245), (0, 127, 255), (119, 136, 153),
                  (192, 192, 192), (255, 245, 238), (255, 255, 255), (173, 216, 230), (240, 128, 128), (144, 238, 144),
                  (139, 0, 139), (152, 251, 152), (255, 248, 220), (72, 61, 139), (255, 250, 240), (124, 252, 0),
                  (205, 133, 63), (218, 165, 32), (255, 235, 205), (0, 128, 0), (238, 232, 170), (0, 250, 154),
                  (245, 245, 220), (127, 255, 0), (240, 248, 255), (222, 184, 135), (176, 196, 222), (255, 0, 0),
                  (173, 255, 47), (0, 255, 255), (255, 140, 0), (255, 250, 205), (106, 90, 205),
                  (220, 20, 60), (255, 250, 250), (184, 134, 11), (210, 105, 30), (127, 127, 127), (100, 149, 237),
                  (221, 160, 221), (186, 85, 211), (233, 150, 122), (255, 239, 213), (248, 248, 255), (165, 42, 42),
                  (250, 235, 215), (0, 191, 255), (143, 188, 143), (32, 178, 170), (139, 0, 0), (0, 100, 0),
                  (105, 105, 105), (0, 128, 128), (253, 245, 230), (95, 158, 160), (220, 220, 220), (0, 0, 128),
                  (72, 209, 204), (139, 69, 19), (175, 238, 238)]


RGB_COLLECTION = DISTINGUISHABLE_COLORS

for rgb in RGB_COLLECTION_ADDONS:
    if rgb not in RGB_COLLECTION:
        RGB_COLLECTION.append(rgb)


def get_random_color(dont_use_colors=None):
    global RGB_COLLECTION
    if dont_use_colors is None:
        dont_use_colors = RGB_COLLECTION

    while True:
        B = random.randint(0, 255)
        G = random.randint(0, 255)
        R = random.randint(0, 255)
        if (B,G,R) not in dont_use_colors:
            return (B,G,R)


LABELS = {}
ALL_RGB_COLORS_TAKEN = 'ALL_RGB_COLORS_TAKEN'
LABELS_KEY = 'LABELS_KEY'


def select_color_based_on_labels(label_name, draw_type, is_random):
    rgb = None
    used_colors = LABELS[draw_type][ALL_RGB_COLORS_TAKEN]
    if is_random:
        if len(used_colors) < len(RGB_COLLECTION):
            while True:
                rgb = random.choice(RGB_COLLECTION)
                if rgb in used_colors:
                    continue
                LABELS[draw_type][LABELS_KEY][label_name] = rgb
                LABELS[draw_type][ALL_RGB_COLORS_TAKEN].append(rgb)
                break
        else:
            rgb = random.choice(RGB_COLLECTION)
            LABELS[draw_type][LABELS_KEY][label_name] = rgb
            LABELS[draw_type][ALL_RGB_COLORS_TAKEN].append(rgb)

    else:
        if len(used_colors) < len(RGB_COLLECTION):
            for temp_rgb in RGB_COLLECTION:
                if temp_rgb not in used_colors:
                    rgb = temp_rgb
                    LABELS[draw_type][LABELS_KEY][label_name] = rgb
                    LABELS[draw_type][ALL_RGB_COLORS_TAKEN].append(rgb)
                    break
        else:
            rgb = random.choice(RGB_COLLECTION)
            LABELS[draw_type][LABELS_KEY][label_name] = rgb
            LABELS[draw_type][ALL_RGB_COLORS_TAKEN].append(rgb)

    return rgb


def get_color(label_name, draw_type, is_random=False):
    global RGB_COLLECTION, LABELS

    if draw_type not in LABELS:
        LABELS[draw_type] = {ALL_RGB_COLORS_TAKEN: [], LABELS_KEY: {}}

    if label_name is None:
        return RGB_COLLECTION[0][::-1]

    if label_name not in LABELS[draw_type][LABELS_KEY]:
        rgb = select_color_based_on_labels(label_name, draw_type, is_random)
    else:
        rgb = LABELS[draw_type][LABELS_KEY][label_name]

    return rgb


if __name__ == '__main__':
    for i in range(10):
        # rgb = get_color(str(i), 'rect', is_random=False)
        rgb = get_color('car', 'rect', is_random=False)
        print(rgb)
