import pytesseract
import tkinter


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class BoundingBox:
    def __init__(self, point_one: Point, point_two: Point, canvas_id):
        self.points = [point_one, point_two]
        self.canvas_id = canvas_id
        self.delete_button = None

    def publish(self):
        print(f"Rectangle Created Coordinates: ( {self.points[0].x} x, {self.points[0].y}  y) , "
              f"({self.points[1].x}  x, {self.points[1].y}  y)")
        print(type(self.canvas_id))

    def roi_subsection(self, image):
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        return image[min(y_values):max(y_values), min(x_values):max(x_values)]

    def extract_text(self, image):
        text = pytesseract.image_to_string(self.roi_subsection(image), config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
        print("text found:  " + text )
        print(type(text))

    def set_delete_button(self, delete_button: tkinter.Button):
        self.delete_button = delete_button