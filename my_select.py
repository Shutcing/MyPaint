import tkinter as tk
from PIL import ImageTk, Image
X, Y, W, H = 0, 0, 0, 0
coords = []
items = []
C = ""
I1 = ""
I2 = ""
angle = 0


def select(canvas, x, y, x1, y1, need_reflect):
    global C, X, Y, coords, W, H, I1, I2
    W = -x + x1
    H = -y + y1
    C = canvas
    coords = [x, y, x1, y1]
    left = min(x, x1)
    right = max(x, x1)
    bottom = max(y, y1)
    top = min(y, y1)
    I1 = canvas.pre_img[-1].crop((left, top, right, bottom))
    if need_reflect:
        I1 = I1.transpose(Image.FLIP_LEFT_RIGHT)
    I2=  ImageTk.PhotoImage(I1)

    canvas.canvas.create_rectangle(
                        left, top, right, bottom, fill="#FFFFFB", outline="#FFFFFB", tags="eraser_rect")
    im = canvas.canvas.create_image(
            left,
            top,
            anchor=tk.NW,
            image=I2,
        )
    items.append(im)
    lines = C.canvas.find_withtag("selection")
    for line in lines:
        if line not in items:
            items.append(line)
    C.canvas.bind("<Motion>", move_selection)


def move_selection(event):
    global C, X, Y, coords, items, W, H
    for item in items:
        if X != 0 and Y != 0:
            C.canvas.move(item, event.x - X, event.y - Y)
    X = event.x
    Y = event.y
    coords = [coords[0] + event.x - X, coords[1] + event.y - Y, coords[2] + event.x - X, coords[3] + event.y - Y]
    C.choose_select_place = [(event.x - W, event.y - H), (event.x, event.y)]


def choose_selection(event):
    global C
    if C != "":
        C.canvas.unbind("<Motion>")
        C.canvas.unbind("<Button-1>")
        C.canvas.bind("<Button-1>", C.fill)


def cancel_selection(event):
    global items, X, Y
    for line in C.canvas.find_withtag("selection"):
        C.canvas.delete(line)
    items = []
    X = 0
    Y = 0
    C.canvas.bind("<Motion>", C.stop_draw)
    C.canvas.bind("<Button-1>", C.fill)
    C.canvas.unbind("<Double-Button-1>")
    C.save(False)


def delete_selection(event):
    global C, X, Y, coords, items
    print(items)
    for item in items:
        C.canvas.delete(item)
    items = []
    C.canvas.unbind("<Motion>")
    C.canvas.bind("<Motion>", C.stop_draw)
    C.canvas.unbind("<Button-1>")
    C.canvas.bind("<Button-1>", C.fill)
    X = 0
    Y = 0


def rotate_selection(event):
    if (event.char in ["r", "к", "l", "д"]):
        global I1, I2, C, items, angle, coords
        
        angle = angle - 5 if event.char in ["l", "д"] else angle + 5
        angle = angle % 360

        left, top = C.choose_select_place[0]
        right, bottom = C.choose_select_place[1]
        center_x, center_y = (left + right) / 2, (top + bottom) / 2

        rotated_image = I1.rotate(angle, expand=True)
        I2 = ImageTk.PhotoImage(rotated_image)

        for item in items:
            C.canvas.delete(item)
        items.clear()

        im = C.canvas.create_image(center_x, center_y, anchor=tk.CENTER, image=I2)
        items.append(im)