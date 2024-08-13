import customtkinter as ctk


class WeightChooser:
    def __init__(self, frame, width, weight, color):
        self.weight = weight
        self.scale_width = width
        self.slider_x = 0
        self.slider_y = 0
        self.scale_x = 0
        self.scale_y = 0
        self.scale = ctk.CTkFrame(frame, width=width, height=5, fg_color=color)
        self.slider = ctk.CTkButton(
            frame,
            width=weight * 2,
            height=weight * 2,
            text="",
            fg_color=color,
            corner_radius=0,
            command=self.change_weight,
        )

    def hide(self):
        self.scale.place_forget()
        self.slider.place_forget()

    def show(self, x, y, weight):
        self.weight = weight
        self.scale.place(x=x, y=y)
        self.scale_x = x
        self.scale_y = y
        self.slider_x = x
        self.slider_y = y - self.weight * 0.8
        self.slider.place(x=self.slider_x, y=self.slider_y)

    def change_weight(self):
        self.slider.bind("<B1-Motion>", self.update_slider)

    def update_slider(self, event):
        x = event.x
        self.slider_x = self.slider_x + x / 1000
        if self.slider_x > self.scale_x + self.scale_width:
            self.slider_x = self.scale_x + self.scale_width
        if self.slider_x < self.scale_x:
            self.slider_x = self.scale_x
        self.weight = (self.slider_x - self.scale_x) // 2 + 10
        self.slider.place(x=self.slider_x, y=self.slider_y - self.weight // 10)
        self.slider.configure(width=20 + self.weight // 5, height=20 + self.weight // 5)
