import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from bounding_box_element import BoundingBoxElements
import cv2


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.frame = tk.Frame(master)
        # Initial Image
        self.__default_image_file = 'resources/default_graph.png'

        # Reference for Objects:
        self.x = self.y = 0
        self.bounding_boxes = {}


        self.canvas = tk.Canvas(self.master, width=1280, height=800, cursor="cross")





        self.canvas.pack()
        # Load Default Images
        self._initial_setup_image()


        # Button for Switching the Image
        self.button_switch_image = tk.Button(self.frame, text="Switch Image", command=self.update_setup_for_new_image)
        self.button_switch_image.pack(side="right")
        self.frame.pack()

    def _initial_setup_image(self):
        # Draw Default Image
        self.processing_image = cv2.imread(self.__default_image_file)
        self.load_image(self.__default_image_file)

        # Create image widget
        self.image_widget = self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
        # Add bounding box elemnt
        self.bounding_box_creator = self.initialise_bounding_box_creator()
        self.button_bounding_box = tk.Button(self.frame, text="Bounding Box",
                                             command=self.bounding_box_creator.bind_bounding_box_creation)
        self.button_bounding_box.pack(side="right")

    def load_image(self, filename):
        self.display_image = ImageTk.PhotoImage(Image.open(filename))


    def openfn(self):
        return filedialog.askopenfilename(title='open')

    def initialise_bounding_box_creator(self):
        # Refresh bounding boxes
        self.bounding_boxes = {}
        return BoundingBoxElements(self.canvas, self.bounding_boxes, self.processing_image, self.master)

    def update_setup_for_new_image(self, *args):
        file_name = self.openfn()
        if file_name:
            # Clear Bounding Boxes
            self.bounding_box_creator.clear_all_bounding_box_elements()
            # load Image
            self.load_image(file_name)
            self.processing_image = cv2.imread(file_name)
            self.canvas.itemconfig(self.image_widget, image=self.display_image)
            self.bounding_box_creator = self.initialise_bounding_box_creator()
            # Recreate button
            self.button_bounding_box.configure( text="Bounding Box",
                                                 command=self.bounding_box_creator.bind_bounding_box_creation)


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()