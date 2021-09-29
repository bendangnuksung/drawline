## Drawline

If you are tired to always search how to overlay box/polygons into the images and have to trial-and-error to get the right Font size, thickness or lines and what not.
Then this is for people like us. 

Drawline overlays polygon contours and rectangle on images with minimum effort.
It auto handles color picking for labels, font size, line thickness. (User has option to override it too) 

### install
```bash
pip install drawline
```

### How to use
```python
from drawline import draw_poly, draw_rect
import cv2

img_pth = '/PATH/TO/IMAGE.jpg'
image = cv2.imread(img_pth)

# Single  Rectangle example
result_image = draw_rect(image, [XMIN, YMIN, XMAX, YMAX], labels='label_1')

# Multiple Rectangles example
result_image = draw_rect(image,
                         [[XMIN_1, YMIN_1, XMAX_1, YMAX_1],
                          [XMIN_2, YMIN_2, XMAX_2, YMAX_2]],
                         labels=['Label_1', 'Label_2'])


# Single Contours Polygon example 
result_image = draw_poly(image, CONTOUR, label='label_1')

# Multiple Contours Polygon points
result_image = draw_poly(image, CONTOURS, label=['label_1', 'label_2', ...])

# Assigning Labels is optional, if not given no label name will be displayed
```

### Default options

```python
def draw_rect(image, points, rgb=None, thickness=None,
              labels=None, label_rgb=(255, 255, 255), label_bg_rgb=None, label_font_size=None,
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
    
    
def draw_poly(image, contours, fill_in=True, transparency=0.4, rgb=None, thickness=None, 
              show_rect=True, labels=None, label_rgb=(255, 255, 255),
              label_bg_rgb=None, label_font_size=None, random_color=True):
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
```

