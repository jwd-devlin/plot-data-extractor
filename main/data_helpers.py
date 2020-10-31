import pytesseract
import tkinter
import numpy as np


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class BoundingBox:
    def __init__(self, point_one: Point, point_two: Point, canvas_id):
        self.points = [point_one, point_two]
        self.canvas_id = canvas_id
        self.delete_button_widget = None
        self.image_text_entry_field_widget = None
        self.converted_image_text = ""
        self.entry_converted_image_display_text = tkinter.StringVar()

    def publish(self):
        print(f"Rectangle Created Coordinates: ( {self.points[0].x} x, {self.points[0].y}  y) , "
              f"({self.points[1].x}  x, {self.points[1].y}  y)")

    def roi_subsection(self, image: np.ndarray) -> np.ndarray:
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        return image[min(y_values):max(y_values), min(x_values):max(x_values)]

    def extract_text(self, image: np.ndarray) -> str:
        self.converted_image_text = pytesseract.image_to_string(self.roi_subsection(image), config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        print("text found:  " + self.converted_image_text )
        return self.converted_image_text

    def set_delete_button_widget(self, delete_button: tkinter.Button):
        self.delete_button_widget = delete_button

    def set_text_entry_widget(self, image_text_entry_field_widget: tkinter.Entry):
        self.entry_converted_image_display_text.set(self.converted_image_text)
        self.image_text_entry_field_widget = image_text_entry_field_widget