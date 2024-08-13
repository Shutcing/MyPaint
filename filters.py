import tkinter as tk
from PIL import Image
from my_select import select


ALREADY_DONE_IMGS = []
IMAGES = []
COUNT = -1


def find_rectangles_intersection(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    all_x = sorted([x1, x2, x3, x4])
    all_y = sorted([y1, y2, y3, y4])
    return [all_x[1] - x3, all_y[1] - y3, all_x[2] - x3, all_y[2] - y3]


def bright(color, factor):
    if color == "black":
        color = (0, 0, 0)
    else:
        color = hex_to_rgb(color)
    if factor < 0 or factor > 2:
        raise ValueError("Коэффициент яркости должен быть в диапазоне от 0 до 2.")

    new_color = [int(channel * factor) for channel in color]

    new_color = [max(0, min(255, channel)) for channel in new_color]

    return rgb_to_hex(new_color)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    for component in rgb:
        if not 0 <= component <= 255:
            raise ValueError("Компоненты RGB должны быть в диапазоне [0, 255].")

    hex_components = [hex(component)[2:].zfill(2) for component in rgb]

    hex_color = "#%s%s%s" % tuple(hex_components)

    return hex_color


def convert_to_black_or_white(color_string):
    if color_string == "black":
        return rgb_to_hex((0, 0, 0))
    hex_value = color_string.lstrip("#")
    rgb_value = [int(hex_value[i : i + 2], 16) for i in range(0, len(hex_value), 2)]
    grayscale_value = tuple(
        int((rgb_value[0] + rgb_value[1] + rgb_value[2]) / 3) for _ in range(3)
    )
    return rgb_to_hex(grayscale_value)


def filt(canvas, filter_name, bright_index):
    global ALREADY_DONE_IMGS, COUNT
    
    ALREADY_DONE_IMGS = []
    COUNT += 1
    min_x = min([item[0] for item in canvas.choose_select_place])
    max_x = max([item[0] for item in canvas.choose_select_place])
    min_y = min([item[1] for item in canvas.choose_select_place])
    max_y = max([item[1] for item in canvas.choose_select_place])

    img = Image.open("myimage.png")
    bbox = canvas.canvas.bbox(canvas.canvas.find_withtag("imge")[0])
    area = find_rectangles_intersection(
                        (min_x, min_y),
                        (max_x, max_y),
                        (bbox[0], bbox[1]),
                        (bbox[2], bbox[3]),
                    )
    area = [min_x, min_y, max_x, max_y]
    img = filt_img(img, area, bright_index, filter_name, canvas)
    if img is None:
        return
    img.save("myimage.png")
    canvas.img_to_insert.append(
                        [
                            tk.PhotoImage(
                                file="myimage.png"
                            ),
                            "imge",
                        ]
                    )
    canvas.change_img(canvas.canvas.find_withtag("imge")[0], "myimage.png")


def filt_img(img, area, bright_index, filter_name, canvas):
    img = img.convert("RGBA")
    if filter_name == "reflection":
        select(canvas, area[0]-2, area[1]-2, area[2], area[3], True)
        return
    for x in range(area[0], area[2]- 1):
        for y in range(area[1], area[3] - 1):
            r, g, b, a = img.getpixel((x, y))
            if a != 0:
                color = rgb_to_hex((int(r), int(g), int(b)))
                if filter_name == "black-white":
                    color = convert_to_black_or_white(color)
                else:
                    color = bright(color, bright_index)
                img.putpixel((x, y), hex_to_rgb(color))
    return img