import cv2
from drawline.draw_process import draw_poly, draw_rect


from drawline.utils import display, get_biggest_contour, random_resize_and_crop, get_rect_from_poly

pth = 'test_images/1.jpg'
image = cv2.imread(pth)


def test_poly(n=5):
    print("*" * 20, "Test Polygon", "*" * 20)
    image = cv2.imread(pth)
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
        # test single points
        if i == 0:
            test_image = draw_poly(test_image, contours[0], labels=labels[0])
        else:
            test_image = draw_poly(test_image, contours, labels=labels)

        display(test_image)


def test_rect(n=5):
    image = cv2.imread(pth)
    print("*"*20, "Test Rectangle", "*"*20)
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
            test_image = draw_rect(test_image, rects[0], labels=labels[0])
        else:
            test_image = draw_rect(test_image, rects, labels=labels)
        display(test_image)


if __name__ == '__main__':
    test_poly()
    test_rect()
