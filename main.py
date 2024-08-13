import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, EpsImagePlugin, ImageTk
from tkinter import colorchooser
import numpy as np
import fill
import my_select
import filters
from panel import Panel
from weight_chooser import WeightChooser

EpsImagePlugin.gs_windows_binary = r'C:\Program Files (x86)\gs\gs10.03.1\bin\gswin32c.exe'

WIDTH = 900
HEIGHT = 600
Color = "white"
TOOL_PANEL_BUTTONS = ["pen", "eraser", "figure", "size", "text"]
UP_PANEL_BUTTONS = ["save", "image"]
BOTTOM_PANEL_BUTTONS = ["palette", "fill", "selection", "filtrs"]
FIGUREBAR_PANEL_BUTTONS = ["square", "circle", "triangle", "line"]
FILTRS_PANEL_BUTTONS = ["black-white", "bright", "reflection"]

ALL_BUTTONS = dict()


def pixels_to_dots(pixels):
    return (96 / 72) * pixels


class App:
    def __init__(
        self,
    ):
        self.app = ctk.CTk(fg_color="white")
        self.app.geometry(f"{WIDTH}x{HEIGHT}")
        self.app.minsize(width=900, height=600)
        self.app.title("Paint")


app = App()


class Canvas:
    def __init__(self, pen_weight, pen_color, bg_color):
        self.pen_weight = pen_weight
        self.pen_color = pen_color
        self.bg_color = bg_color
        self.x = 0
        self.y = 0
        self.x1 = 0
        self.y1 = 0
        self.canvas = tk.Canvas(app.app)
        self.img_to_insert = []
        self.selection = False
        self.choose_select_place = []
        my_select.C = self
        self.image = []
        self.pre_img = []
        self.opacity = None
        self.text_id = 0

    def show(self):
        self.canvas.configure(
            background=self.bg_color,
            width=pixels_to_dots(WIDTH),
            height=pixels_to_dots(HEIGHT),
        )
        self.canvas.place(x=0, y=0)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Motion>", self.stop_draw)
        self.canvas.bind("<Button-1>", self.fill)
        app.app.bind("<Double-Button-1>", self.write)
        self.choose_select_place = [
            (0, 0),
            (int(self.canvas.cget("width")), int(self.canvas.cget("height"))),
        ]
        self.save(False)


    def merge_images(self, image1, image2):
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))

        merged_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
        
        merged_image.paste(image1, (0, 0))
        merged_image.paste(image2, (0, 0), image2)
        
        return merged_image

    def save(self, bg):
        canvas_width, canvas_height = int(self.canvas.cget("width")), int(self.canvas.cget("height"))

        self.canvas.delete(self.canvas.find_withtag("imge"))
        
        self.canvas.postscript(file="myimage.ps", colormode='color', width=canvas_width, height=canvas_height, pagewidth=canvas_width-1, pageheight=canvas_height-1)
        
        self.canvas.delete("all")

        im = Image.open('myimage.ps').convert('RGBA')
        new_img = ""

        data = np.array(im)
        white = (data[:, :, :3] == [255, 255, 255]).all(axis=-1)
        data[white] = [155, 155, 155, 0]

        im = Image.fromarray(data, 'RGBA')

        if (len(self.pre_img) > 0):
            new_img = self.merge_images(self.pre_img[-1], im)
        else:
            new_img = im

        data = np.array(new_img)
        white = (data[:, :, :3] == [255, 255, 251]).all(axis=-1)
        data[white] = [155, 155, 155, 0]

        new_img= Image.fromarray(data, 'RGBA')

        new_img.save("myimage.png")

        self.image.append(ImageTk.PhotoImage(new_img))

        self.canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.image[-1],
            tags="myimage.png"
                + "$"
                + str(len(self.image)) + " imge"
        )

        self.pre_img.append(new_img)
        if bg:
            new = Image.new("RGB", new_img.size, bg)
            new.paste(new_img, (0, 0), new_img)
            return new



    def fill(self, event):
        if app.app.cget("cursor") == "@paint_img/fill.cur":
            fill.fill(self.canvas, self.pre_img[-1], event.x, event.y, self.pen_color)

    def write(self, event):
        x, y = event.x, event.y
        if "text" in app.app.cget("cursor"):
            app.app.bind("<Key>", self.key_press)
            self.text_id = self.canvas.create_text(x, y, text="|", font=("Montserat", 50), fill=self.pen_color)

    def stop_draw(self, event):
        if app.app.cget("cursor") in ["sb_h_double_arrow", "sb_v_double_arrow"]:
            self.save(False)
        if (set(self.canvas.find_all()) - set(self.canvas.find_withtag("imge")) != set() and not self.selection):
            self.save(False)
        if (
            app.app.cget("cursor") == "arrow"
            and self.selection
            and self.canvas.find_withtag("selection")
        ):
            self.choose_select_place = [(self.x, self.y), (self.x1, self.y1)]
            my_select.select(app.canvas, self.x, self.y, self.x1, self.y1, False)
            app.app.bind("<Key>", my_select.rotate_selection)
            app.app.bind("<BackSpace>", my_select.delete_selection)
        if (len(app.tools_panel.buttons) > 3
            and app.tools_panel.buttons[3].button.cget("fg_color") == "#67770A"
        ):
            if event.y > int(self.canvas.cget("height")) / 2:
                app.app.config(cursor="sb_v_double_arrow")
            if event.x > int(self.canvas.cget("width")) / 2:
                app.app.config(cursor="sb_h_double_arrow")
        self.canvas.delete("figure")
        if (
            app.app.cget("cursor") == "@paint_img/square.cur"
            and self.x != 0
            and self.y != 0
        ):
            self.canvas.create_rectangle(
                self.x,
                self.y,
                self.x1,
                self.y1,
                fill=self.pen_color,
                tags="final_figure", 
                outline=self.pen_color
            )
        if (
            app.app.cget("cursor") == "@paint_img/circle.cur"
            and self.x != 0
            and self.y != 0
        ):
            self.canvas.create_oval(
                self.x,
                self.y,
                self.x1,
                self.y1,
                fill=self.pen_color,
                tags="final_figure",
                outline=self.pen_color
            )
        if (
            app.app.cget("cursor") == "@paint_img/triangle.cur"
            and self.x != 0
            and self.y != 0
        ):
            self.canvas.create_polygon(
                self.x,
                self.y1,
                self.x1,
                self.y1,
                (self.x1 - self.x) / abs(self.x1 - self.x) * abs((self.x1 - self.x) / 2)
                + self.x,
                self.y,
                fill=self.pen_color,
                tags="final_figure",
                outline=self.pen_color
            )
        if (
            app.app.cget("cursor") == "@paint_img/line.cur"
            and self.x != 0
            and self.y != 0
        ):
            self.canvas.create_line(
                self.x + 10,
                self.y + 10,
                self.x1 + 10,
                self.y1 + 10,
                capstyle="round",
                joinstyle="round",
                smooth="false",
                fill=self.pen_color,
                width=self.pen_weight,
                tags="final_figure",
            )

        if (
            app.app.cget("cursor") == "@paint_img/image.cur"
            and self.x != 0
            and self.y != 0
        ):
            self.canvas.create_image(
                self.x1,
                self.y1,
                anchor=tk.NW,
                image=self.img_to_insert[-1][0],
                tags=self.img_to_insert[-1][1].replace(" ", "@")
                + "$"
                + str(len(self.img_to_insert)),
            )
            app.app.config(cursor="arrow")

        self.x = 0
        self.y = 0

    def change_img(self, id, tag):
        self.canvas.itemconfig(id, image=self.img_to_insert[-1][0], tag=tag)
    
    def key_press(self, event):
        current_text = self.canvas.itemcget(self.text_id, "text")
        if "|" in current_text:
            self.canvas.itemconfig(self.text_id, text="")
            return
        if event.keysym == "BackSpace":
            current_text = current_text[:-1]
        elif event.keysym == "Return":
            current_text += "\n"
        else:
            current_text += event.char        
        self.canvas.itemconfig(self.text_id, text=current_text)

    def draw(self, event):
        x, y = event.x, event.y
        self.pen_weight = app.weight_chooser.weight

        if app.app.cget("cursor") == "@paint_img/pen.cur":
            if self.x != 0 and self.y != 0:
                self.canvas.create_line(
                    self.x,
                    self.y + 20,
                    x,
                    y + 20,
                    capstyle="round",
                    joinstyle="round",
                    smooth="false",
                    fill=self.pen_color,
                    width=self.pen_weight,
                    tags="line",
                    stipple=self.opacity
                )
            self.x = x
            self.y = y

        if app.app.cget("cursor") == "@paint_img/eraser.cur":
            if self.x != 0 and self.y != 0:
                self.canvas.create_line(
                    self.x,
                    self.y + 20,
                    x,
                    y + 20,
                    capstyle="round",
                    joinstyle="round",
                    smooth="false",
                    fill="#FFFFFB",
                    width=self.pen_weight,
                    tags="eraser",
                    stipple=self.opacity
                )
            self.x = x
            self.y = y

        if app.app.cget("cursor").split(".")[0] in [
            "@paint_img/square",
            "@paint_img/circle",
            "@paint_img/triangle",
            "@paint_img/image",
            "@paint_img/line",
        ]:

            self.canvas.delete("figure")
            if self.x != 0 and self.y != 0:
                if "square" in app.app.cget("cursor"):
                    self.canvas.create_rectangle(
                        self.x, self.y, x, y, fill=self.pen_color, tags="figure", outline=self.pen_color
                    )
                elif "circle" in app.app.cget("cursor"):
                    self.canvas.create_oval(
                        self.x, self.y, x, y, fill=self.pen_color, tags="figure", outline=self.pen_color
                    )
                elif "triangle" in app.app.cget("cursor"):

                    self.canvas.create_polygon(
                        self.x,
                        y,
                        x,
                        y,
                        (x - self.x) / abs(x - self.x) * abs((x - self.x) / 2) + self.x,
                        self.y,
                        fill=self.pen_color,
                        tags="figure", outline=self.pen_color
                    )
                elif "image" in app.app.cget("cursor"):
                    self.canvas.create_image(
                        x,
                        y,
                        anchor=tk.NW,
                        image=self.img_to_insert[-1][0],
                        tags="figure",
                    )
                elif "line" in app.app.cget("cursor"):
                    self.canvas.create_line(
                        self.x + 10,
                        self.y + 10,
                        x + 10,
                        y + 10,
                        capstyle="round",
                        joinstyle="round",
                        smooth="false",
                        fill=self.pen_color,
                        width=self.pen_weight,
                        tags="figure",
                    )
                self.x1 = x
                self.y1 = y
            else:
                self.x = x
                self.y = y

        if app.app.cget("cursor") in ["sb_h_double_arrow", "sb_v_double_arrow"]:
            if "h" in app.app.cget("cursor"):
                self.canvas.configure(width=x)
            else:
                self.canvas.configure(height=y)
            self.choose_select_place = [
                (0, 0),
                (int(self.canvas.cget("width")), int(self.canvas.cget("height"))),
            ]

        if app.app.cget("cursor") == "arrow" and self.selection:
            self.canvas.bind("<Button-1>", my_select.choose_selection)
            self.canvas.bind("<Double-Button-1>", my_select.cancel_selection)
            self.choose_select_place = [(self.x, self.y), (x, y)]
            self.canvas.delete("selection")
            if self.x != 0 and self.y != 0:
                sign_x = -1 if x < self.x else 1
                sign_y = -1 if y < self.y else 1
                self.canvas.create_line(
                    self.x,
                    self.y,
                    self.x + abs(self.x - x) * sign_x,
                    self.y,
                    tags="selection",
                    dash=10,
                )
                self.canvas.create_line(
                    self.x,
                    self.y,
                    self.x,
                    self.y + abs(self.y - y) * sign_y,
                    tags="selection",
                    dash=10,
                )
                self.canvas.create_line(
                    self.x,
                    self.y + abs(self.y - y) * sign_y,
                    self.x + abs(self.x - x) * sign_x,
                    self.y + abs(self.y - y) * sign_y,
                    tags="selection",
                    dash=10,
                )
                self.canvas.create_line(
                    self.x + abs(self.x - x) * sign_x,
                    self.y,
                    self.x + abs(self.x - x) * sign_x,
                    self.y + abs(self.y - y) * sign_y,
                    tags="selection",
                    dash=10,
                )
                self.x1 = x
                self.y1 = y
            else:
                self.x = x
                self.y = y


class ToolsPanel(Panel):
    def __init__(self, master):
        super().__init__(master)
        self.figure_bar = Bar(master, FIGUREBAR_PANEL_BUTTONS)
        self.figure_bar.buttons = [
            MyButton(self.figure_bar, type) for type in FIGUREBAR_PANEL_BUTTONS
        ]


class MyButton:
    def __init__(self, frame, type):
        self.frame = frame
        self.button = ctk.CTkButton(frame.frame)
        self.type = type
        self.x = 0
        self.y = 0
        self.width = 0
        self.color = ""

    def show(
        self, width, height, color, bg, text, img, x, y, img_width, img_height, type
    ):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.width = width
        self.button.configure(
            width=width,
            height=height,
            corner_radius=10,
            fg_color=color,
            bg_color=bg,
            text=text,
            hover_color="#67770A",
            image=ctk.CTkImage(
                dark_image=img, light_image=img, size=[img_width, img_height]
            ),
            command=self.choose_tool,
        )
        self.button.place(x=x, y=y)

    def hide(self):
        self.button.destroy()

    def change_cursor(self):
        if self.type in ["figure", "selection", "filtrs"]:
            app.app.config(cursor="arrow")
        elif self.type == "size":
            app.app.config(cursor="sb_h_double_arrow")
        else:
            app.app.config(cursor=f"@paint_img/{self.type}.cur")

    @staticmethod
    def change_buttons(
        frame,
        width,
        height,
        color,
        bg,
        y,
        x,
        margin_x,
        margin_y,
        types,
        img_width,
        img_height,
    ):
        i = 0
        for button in frame.buttons:
            button.show(
                width,
                height,
                color,
                bg,
                "",
                Image.open(f"paint_img/{types[i]}.png"),
                x + margin_x * i,
                y + margin_y * i,
                img_width=img_width,
                img_height=img_height,
                type=types[i],
            )
            i += 1

    def choose_tool(self):
        global FILTRS_PANEL_BUTTONS
        app.canvas.x, app.canvas.y, app.canvas.x1, app.canvas.y1 = 0, 0, 0, 0

        if self.type == "selection":
            app.canvas.selection = not app.canvas.selection
        else:
            if app.canvas.selection and self.type != "filtrs":
                my_select.cancel_selection(None)
                app.canvas.selection = False
        
        if "opacity" in self.type:
            if "100" in self.type:
                app.canvas.opacity = None
            else:
                app.canvas.opacity = f"gray{self.type[-2:]}"
            return

        if self.type == "black-white":
            filters.filt(app.canvas, "black-white", 0)
            my_select.choose_selection("")
            app.canvas.choose_select_place = [
                (0, 0),
                (int(app.canvas.canvas.cget("width")), int(app.canvas.canvas.cget("height"))),
            ]
            app.canvas.canvas.bind("<Motion>", app.canvas.stop_draw)
            app.canvas.save(False)
            return
        if self.type == "reflection":
            filters.filt(app.canvas, "reflection", 0)
            my_select.choose_selection("")
            app.canvas.choose_select_place = [
                (0, 0),
                (int(app.canvas.canvas.cget("width")), int(app.canvas.canvas.cget("height"))),
            ]
            app.canvas.canvas.bind("<Motion>", app.canvas.stop_draw)
            app.canvas.save(False)
            return
        if self.type == "bright":
            FILTRS_PANEL_BUTTONS = app.bottom_panel.figure_bar.change_buttons(
                ["minus", "plus", "ok"]
            )
            app.bottom_panel.buttons[-1].button.invoke()

            app.bottom_panel.bright_level = Panel(app.app)
            app.bottom_panel.bright_level.show(
                WIDTH / 10,
                app.bottom_panel.figure_bar.height,
                "black",
                Color,
                app.bottom_panel.figure_bar.x + app.bottom_panel.figure_bar.width,
                app.bottom_panel.figure_bar.y,
                0,
            )
            app.bottom_panel.bright_level.label = ctk.CTkLabel(
                master=app.bottom_panel.bright_level.frame,
                text="1.0",
                text_color="white",
                font=("Montserrat", 25),
            )
            app.bottom_panel.bright_level.label.place(
                x=app.bottom_panel.bright_level.width / 4,
                y=app.bottom_panel.bright_level.height / 4,
            )
            app.canvas.canvas.bind("<Motion>", app.canvas.stop_draw)
            app.canvas.save(False)
            return
        if self.type == "ok":
            filters.filt(
                app.canvas,
                "bright",
                float(app.bottom_panel.bright_level.label.cget("text")),
            )
            my_select.choose_selection("")
            app.bottom_panel.bright_level.frame.destroy()
            FILTRS_PANEL_BUTTONS = app.bottom_panel.figure_bar.change_buttons(
                ["black-white", "bright", "reflection"]
            )
            return
        if self.type == "plus":
            new_label = (
                round(float(app.bottom_panel.bright_level.label.cget("text")) + 0.1, 1)
                % 2.1
            )
            app.bottom_panel.bright_level.label.configure(text=f"{new_label}")
            return
        if self.type == "minus":
            new_label = (
                round(float(app.bottom_panel.bright_level.label.cget("text")) - 0.1, 1)
                % 2.1
            )
            app.bottom_panel.bright_level.label.configure(text=f"{new_label}")
            return

        if self.type == "palette":
            choosecolor = colorchooser.askcolor(
                title="Choose Color", initialcolor="#F0E68C", parent=app.app
            )
            if choosecolor[1] is not None:
                app.canvas.pen_color = choosecolor[1]
                self.button.configure(fg_color=choosecolor[1])
            return
        if self.type == "image":
            file_path = filedialog.askopenfilename(
                title="Выберите фото",
                filetypes=(
                    ("PNG", ".png"),
                    ("JPEG", ".jpg"),
                    ("BMP", ".bmp"),
                    ("Все файлы", "*.*"),
                ),
            )
            file_path = file_path.replace("С", "C")
            app.canvas.img_to_insert.append([tk.PhotoImage(file=file_path), file_path])
            self.change_cursor()
            return
        if self.type == "save":
            image = app.canvas.save((255, 255, 255))
            file_path = filedialog.asksaveasfilename(
            title="Сохранить скриншот",
                filetypes=(
                    ("PNG", ".png"),
                    ("JPEG", ".jpg"),
                    ("BMP", ".bmp"),
                    ("Все файлы", "*.*"),
                ),
                initialfile="image.png",
                )
            if file_path:
                image.save(file_path)
            return

        if self.type in ["filtrs", "figure"] and not self.frame.figure_bar.is_bar_show:
            if self.type == "figure":
                self.try_to_change_buttons()
                app.bottom_panel.figure_bar.hide()
                app.tools_panel.figure_bar.show(
                    2 * self.x + self.frame.x + self.width,
                    self.y + self.frame.y,
                    300,
                    self.width * 1.5,
                    "#DF9A70",
                    "black"
                )
            elif self.type == "filtrs":
                app.bottom_panel.figure_bar.show(
                    2 * self.x + self.frame.x + self.width,
                    self.y + self.frame.y,
                    200,
                    self.width * 1.5,
                    "#67770A",
                    "black"
                )
                app.tools_panel.figure_bar.hide()
            else:
                app.tools_panel.figure_bar.hide()
                self.try_to_change_buttons()
                app.bottom_panel.figure_bar.hide()
        else:
            self.try_to_change_buttons()
            app.tools_panel.figure_bar.hide()
            app.bottom_panel.figure_bar.hide()

        if self.button.cget("fg_color") == "#67770A":
            self.button._fg_color = self.color
            app.app.config(cursor="arrow")
        else:
            for key in ALL_BUTTONS.keys():
                for c in ALL_BUTTONS[key]:
                    if c.type != "palette":
                        c.button.configure(fg_color=key)
            self.button._fg_color = "#67770A"
            self.change_cursor()

    def try_to_change_buttons(self):
        global FILTRS_PANEL_BUTTONS
        app.bottom_panel.bright_level.frame.destroy()
        FILTRS_PANEL_BUTTONS = app.bottom_panel.figure_bar.change_buttons(
                ["black-white", "bright", "reflection"]
            )


class Bar(Panel):
    def __init__(self, master, figurebar_panel_buttons):
        self.is_bar_show = False
        self.options = figurebar_panel_buttons.copy()
        super().__init__(master)

    def show(self, x, y, width, height, fg_color, button_color):
        super().show(width, height, fg_color, Color, x, y, 0)
        self.is_bar_show = True
        MyButton.change_buttons(
            self,
            self.height / 1.5,
            self.height / 1.5,
            button_color,
            self.color,
            (self.height - self.height / 1.5) / 2,
            self.height / 6,
            self.height,
            0,
            self.options,
            20,
            20,
        )

    def hide(self):
        super().hide()
        self.is_bar_show = False

    def destroy_buttons(
        self,
    ):
        for button in self.buttons:
            button.button.destroy()

    def change_buttons(self, new_options_set):
        self.destroy_buttons()
        self.options = new_options_set
        self.buttons = [MyButton(self, type) for type in new_options_set]
        update_window()
        self.hide()
        return new_options_set.copy()


def update_window():
    app.tools_panel.figure_bar.hide()
    app.app.config(cursor="arrow")
    app.up_panel.show(WIDTH * 141 / 1280, HEIGHT * 277 / 832, "#D2D05F", Color, 0, 0, 0)
    MyButton.change_buttons(
        app.up_panel,
        WIDTH / 18,
        WIDTH / 18,
        app.up_panel.color,
        app.up_panel.color,
        HEIGHT / 20,
        (app.up_panel.width - WIDTH / 18) / 4,
        0,
        app.up_panel.height - 2 * HEIGHT / 20 - WIDTH / 18,
        UP_PANEL_BUTTONS,
        WIDTH / 18,
        WIDTH / 18,
    )
    app.bottom_panel.show(
        WIDTH * 141 / 1280,
        HEIGHT * 555 / 832,
        "#67770A",
        Color,
        0,
        HEIGHT * 277 / 832,
        0,
    )
    MyButton.change_buttons(
        app.bottom_panel,
        40,
        40,
        app.up_panel.color,
        app.bottom_panel.color,
        30,
        (app.bottom_panel.width - 50) / 4,
        0,
        (50 + app.bottom_panel.height - 160) / 3,
        BOTTOM_PANEL_BUTTONS,
        40,
        40,
    )
    app.tools_panel.show(
        WIDTH * 10 / 128,
        HEIGHT * 600 / 832,
        "#DF9A70",
        Color,
        WIDTH * 170 / 1280,
        HEIGHT * 170 / 832,
        10,
    )
    MyButton.change_buttons(
        app.tools_panel,
        app.tools_panel.width * 60 / 84,
        app.tools_panel.width * 60 / 84,
        "black",
        app.tools_panel.color,
        app.tools_panel.height * 40 / 492,
        (app.tools_panel.width - WIDTH / 45) / 4,
        0,
        1.6 * app.tools_panel.width * 60 / 84,
        TOOL_PANEL_BUTTONS,
        WIDTH / 45,
        WIDTH / 45,
    )


def set_all_buttons(all_buttons):
    all_buttons[app.up_panel.color] = app.up_panel.buttons + app.bottom_panel.buttons
    all_buttons["black"] = app.tools_panel.buttons + app.tools_panel.figure_bar.buttons
    return all_buttons.copy()


def change_size_check(event):
    global HEIGHT
    if app.app.winfo_height() * 0.8 != HEIGHT:
        HEIGHT = app.app.winfo_height() * 0.8
        update_window()


def on_closing():
    import os

    files = os.listdir(".")
    for file in files:
        if "image__" in file and "$" in file:
            os.remove(file)
        if "myimage" in file:
            os.remove(file)
    app.app.destroy()


app.canvas = Canvas(10, "black", Color)
app.canvas.show()

app.up_panel = Panel(app.app)
app.up_panel.buttons = [MyButton(app.up_panel, type) for type in UP_PANEL_BUTTONS]

app.bottom_panel = Panel(app.app)
app.bottom_panel.bright_level = Panel(app.app)
app.bottom_panel.buttons = [
    MyButton(app.bottom_panel, type) for type in BOTTOM_PANEL_BUTTONS
]

app.tools_panel = ToolsPanel(app.app)
app.tools_panel.buttons = [
    MyButton(app.tools_panel, type) for type in TOOL_PANEL_BUTTONS
]

app.bottom_panel.figure_bar = Bar(app.app, FILTRS_PANEL_BUTTONS)
app.bottom_panel.figure_bar.options = FILTRS_PANEL_BUTTONS
app.bottom_panel.figure_bar.buttons = [
    MyButton(app.bottom_panel.figure_bar, type) for type in FILTRS_PANEL_BUTTONS
]

update_window()

app.weight_chooser = WeightChooser(app.app, 200, 10, "black")
app.weight_chooser.show(HEIGHT * 170 / 832, 25, 10)

app.opacity_chooser = Bar(app.app, ["opacity12", "opacity25", "opacity50", "opacity75", "opacity100"])
app.opacity_chooser.options = ["opacity12", "opacity25", "opacity50", "opacity75", "opacity100"]
app.opacity_chooser.buttons = [
    MyButton(app.opacity_chooser, type) for type in ["opacity12", "opacity25", "opacity50", "opacity75", "opacity100"]
]
app.opacity_chooser.show(HEIGHT * 170 / 832, 60, 250, 50, "white", "white")

ALL_BUTTONS = set_all_buttons(ALL_BUTTONS)


if __name__ == "__main__":
    app.app.protocol("WM_DELETE_WINDOW", on_closing)
    app.app.after(2000, lambda: app.app.bind("<Motion>", change_size_check))
    mainloop = app.app.mainloop()
