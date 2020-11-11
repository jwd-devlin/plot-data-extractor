import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from main.bounding_box_element import BoundingBoxElements
import cv2
from axis_marker import AxisMarkerController


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Initial Image
        self.__default_image_file = '../resources/default_graph.png'

        # Set up Frames
        self._initial_setup_frames()

        # Reference for Objects:
        self.bounding_boxes_cache = {}

        # Set canvas fo images
        self.canvas = tk.Canvas(self.frame_canvas, width=1280, height=800, cursor="cross")
        self.canvas.pack()

        # Load Default Images
        self._initial_setup_image()


        # Button for Switching the Image
        self.button_switch_image = tk.Button(self.frame_buttons_static, text="Switch Image",
                                             command=self.update_setup_for_new_image)
        self.button_switch_image.pack(side=tk.LEFT)

    def _initial_setup_frames(self):
        self.frame_canvas = tk.Frame(self.master, bg="yellow")
        self.frame_buttons_static = tk.Frame(self.master, bg="blue")
        self.frame_input_info = tk.Frame(self.master, bg="green")
        self.frame_canvas.grid(row=0, column=0, rowspan=4, columnspan=6, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame_buttons_static.grid(row=0, column=8, rowspan=1, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame_input_info.grid(row=1, column=8, rowspan=3, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))

    def _initial_setup_image(self):
        # Draw Default Image
        self.processing_image = cv2.imread(self.__default_image_file)
        self.load_image(self.__default_image_file)

        # Create image widget
        self.image_widget = self.canvas.create_image(0, 0, anchor="nw", image=self.display_image)
        # Add bounding box elemnt
        self.initialise_bounding_box_creator()
        self.button_bounding_box = tk.Button(self.frame_buttons_static, text="Bounding Box",
                                             command=self.bounding_box_creator.bind_bounding_box_creation)
        self.button_bounding_box.pack(side=tk.LEFT)
        # Add axis marker
        AxisMarkerController(self.canvas, self.frame_buttons_static).create_axis_marker_enable_button()

    def load_image(self, filename: str):
        self.display_image = ImageTk.PhotoImage(Image.open(filename))

    @staticmethod
    def __select_file_name():
        return filedialog.askopenfilename(title='open')

    def initialise_bounding_box_creator(self):
        # Refresh bounding boxes
        self.bounding_boxes_cache = {}
        self.bounding_box_creator = BoundingBoxElements(self.canvas, self.bounding_boxes_cache, self.processing_image,
                                                        self.frame_input_info)

    def update_setup_for_new_image(self):
        file_name = self.__select_file_name()
        if file_name:
            # Clear Bounding Boxes
            self.bounding_box_creator.clear_all_bounding_box_elements()
            # load Image
            self.load_image(file_name)
            self.processing_image = cv2.imread(file_name)
            self.canvas.itemconfig(self.image_widget, image=self.display_image)

            self.initialise_bounding_box_creator()
            # Recreate button
            self.button_bounding_box.configure(text="Bounding Box",
                                               command=self.bounding_box_creator.bind_bounding_box_creation)


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()