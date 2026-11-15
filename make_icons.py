"""Draw the PNG app icons (192 and 512) matching icon.svg, with OpenCV."""
import pathlib

import cv2
import numpy as np

here = pathlib.Path(__file__).parent
for size in (192, 512):
    k = size / 512
    img = np.zeros((size, size, 4), np.uint8)
    green, cream, gold = (85, 122, 31, 255), (181, 227, 244, 255), (74, 162, 201, 255)
    cv2.rectangle(img, (0, 0), (size - 1, size - 1), green, -1)
    cv2.ellipse(img, (int(256 * k), int(262 * k)), (int(118 * k), int(140 * k)), 0, 0, 360, cream, -1, cv2.LINE_AA)
    cv2.circle(img, (int(256 * k), int(254 * k)), int(58 * k), green, -1, cv2.LINE_AA)
    cv2.circle(img, (int(282 * k), int(250 * k)), int(48 * k), cream, -1, cv2.LINE_AA)
    cv2.rectangle(img, (int(150 * k), int(372 * k)), (int(362 * k), int(416 * k)), gold, -1)
    cv2.imwrite(str(here / f"icon-{size}.png"), img)
print("icons done")
