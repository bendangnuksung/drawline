import cv2
from drawline.draw_process import draw_poly, draw_rect


from drawline.utils import display, get_biggest_contour, random_resize_and_crop, get_rect_from_poly

pth = 'test_images/1.jpg'
image = cv2.imread(pth)

for i in range(10):
    print(i)
    test_image = image.copy()
    test_image = random_resize_and_crop(test_image)
    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    single_contour = get_biggest_contour(contours, reverse=False)
    try:
        index = contours.index(single_contour)
        del contours[index]
        single_contour = get_biggest_contour(contours)
    except:
        pass

    # cv2.drawContours(test_image, [single_contour], -1, (0, 255, 0), 3)
    # display(test_image)

    rects = []
    for contour in contours:
        start_point, end_point = get_rect_from_poly(contour)
        rect = start_point + end_point
        rects.append(rect)

    test_image = draw_rect(test_image, rects[0])

    # test_image = draw_rect(test_image, start_point, end_point, label='HELLO')
    # print("Contours: ", len(contours))
    tt = test_image.copy()
    # cv2.drawContours(tt, contours, -1, (0, 255, 0), 3)
    # display(tt)

    # for j, c in enumerate(contours):
    #     try:
    #         test_image = draw_poly(test_image, c, labels=f'contour {j}', show_rect=True)
    #     except Exception as e:
    #         print(e)
    #         continue

    # test_image = draw_poly(test_image, contours, labels=f'contour 1', show_rect=True)

    # if i not in [9]:
    #     continue
    # print(test_image.shape)
    display(test_image)

# print(test_image.shape)