import customtkinter as ctk


class Panel:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master)
        self.buttons = []
        self.figure_bar = []
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.color = ""
        self.label = ""

    def hide(self):
        self.frame.place_forget()

    def show(self, width, height, color, bg_color, x, y, corner_r):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.frame.configure(
            width=width,
            height=height,
            corner_radius=corner_r,
            fg_color=color,
            bg_color=bg_color,
        )
        self.frame.place(x=x, y=y)
