import glob
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import pandas as pd


def calculate_angle(x, y):
    return math.degrees(math.atan2(y, x))


filenames = [os.path.basename(x) for x in glob.glob("*dane*.csv")]
for filename in filenames:
    padding, scale, point_size = 100, 2, 3
    data = pd.read_csv(filename)
    dtype = [('angle', 'f4'), ('x', 'f4'), ('y', 'f4')]
    data_list = []

    min_x = data.iloc[:, 0].min()
    max_x = data.iloc[:, 0].max()
    min_y = data.iloc[:, 1].min()
    max_y = data.iloc[:, 1].max()
    x_range = max_x - min_x
    y_range = max_y - min_y

    img_width = int(x_range / scale + (padding * 2))
    img_height = int(y_range / scale + (padding * 2))
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)

    origin_x = img_width / 2
    origin_y = img_height / 2

    for _, row in data.iterrows():
        x, y = row[0], row[1]
        angle = calculate_angle(x, y)
        data_list.append((angle, x, y))

    data_array = np.array(data_list, dtype=dtype)
    data_array.sort(order='angle')
    last_x = int((data_array[-1][1] - min_x) / scale)
    last_y = int((data_array[-1][2] - min_y) / scale)

    for angle, x, y in data_array:

        pixel_x = int((x - min_x) / scale)
        pixel_y = int((y - min_y) / scale)
        draw.line([(last_x + padding, last_y + padding),
                   (pixel_x + padding, pixel_y + padding)], fill="red", width=4)
        # draw.line([(origin_x, origin_y),
        #            (pixel_x + padding, pixel_y + padding)], fill="green", width=2)

        draw.rectangle([pixel_x - point_size + padding,
                        pixel_y - point_size + padding,
                        pixel_x + point_size + padding,
                        pixel_y + point_size + padding], fill='black')
        last_x, last_y = pixel_x, pixel_y

    draw.point((origin_x, origin_y), fill="red")
    draw.line([(padding * 0.25, 0), (padding * 0.25, img_height)], fill="black", width=3)
    draw.line([(0, img_height - padding * 0.25),
               (img_width, img_height - padding * 0.25)], fill="black", width=3)

    distance_width = 0
    distance_height = 0
    font = ImageFont.truetype("arial.ttf", size=26)
    while origin_x + (distance_width / scale) < img_width:
        draw.line([(origin_x + (distance_width / scale), img_height - padding * 0.25),
                   (origin_x + (distance_width / scale), img_height - padding * 0.5)], fill="black", width=2)
        draw.text(xy=(origin_x + (distance_width / scale) - padding * 0.16,
                      img_height - padding * 0.25), text=f"{distance_width / 1000}m", fill="black", font=font)

        draw.line([(origin_x - (distance_width / scale), img_height - padding * 0.25),
                   (origin_x - (distance_width / scale), img_height - padding * 0.5)], fill="black", width=2)
        draw.text(xy=(origin_x - (distance_width / scale) - padding * 0.16,
                      img_height - padding * 0.25), text=f"{distance_width / 1000}m", fill="black", font=font)
        distance_width += 500

    while origin_y + (distance_height / scale) < img_height:
        draw.line([(padding * 0.25, origin_y + (distance_height / scale)),
                   (padding * 0.5, origin_y + (distance_height / scale))], fill="black", width=2)
        draw.text(xy=(padding * 0.3, origin_y + (distance_height / scale)),
                  text=f"{distance_height / 1000}m", fill="black", font=font)

        draw.line([(padding * 0.25, origin_y - (distance_height / scale)),
                   (padding * 0.5, origin_y - (distance_height / scale))], fill="black", width=2)
        draw.text(xy=(padding * 0.3, origin_y - (distance_height / scale)),
                  text=f"{distance_height / 1000}m", fill="black", font=font)
        distance_height += 500

    img.save("output_" + os.path.splitext(filename)[0] + ".png")
    img.show()
