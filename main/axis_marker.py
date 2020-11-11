import tkinter as tk


class AxisMarker:

    def __init__(self, x_coord: int, y_coord: int, canvas_id: str):
        self.y_coord = y_coord
        self.x_coord = x_coord
        self.canvas_id = canvas_id


class AxisMarkerController:

    def __init__(self, canvas, master):
        self.master = master
        self.canvas = canvas
        self.axis_marker_cache = {}
        self.axis_marker_count = 0

    def create_axis_marker_enable_button(self):
        axis_marker_creator_trigger = tk.Button(self.master, text="Axis Marker", bg="green",
                                                command=lambda: self.create_axis_marker())
        axis_marker_creator_trigger.pack(side=tk.LEFT)

    def create_axis_marker(self):
        self.canvas.press_dot = self.canvas.bind("<ButtonPress-1>", self.create_dot_on_press)

    def __axis_marker_id(self):
        return "Axis_marker_" + (str(self.axis_marker_count))

    def create_dot_on_press(self, event: tk.Event):
        axis_marker_id = self.__axis_marker_id()
        self.axis_marker_cache[axis_marker_id] = AxisMarker(event.x, event.y, axis_marker_id)
        self.canvas.create_oval(event.x + 2, event.y + 2, event.x - 2, event.y - 2, fill='red', tags=axis_marker_id)
