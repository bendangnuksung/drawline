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

# for rectangles
result_image = draw_rect(image, (XMIN, YMIN), (XMAX, YMAX), label='labelname')

# for polygons
result_image = draw_poly(image, CONTOURS, label='labelname', show_rect=True) 
```

### Default options
`draw_poly(image, contour, fill_in=True, transparency=0.4, rgb=None, thickness=None, show_rect=True, label=None, label_rgb=(255, 255, 255),
              label_bg_rgb=None, label_font_size=None, random_color=True)`

`draw_rect(image, start_point, end_point, rgb=None, thickness=None,
              label=None, label_rgb=(255, 255, 255), label_bg_rgb=None, label_font_size=None,
              random_color=True)`


