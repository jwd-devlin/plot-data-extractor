from main.data_helpers import Point, BoundingBox
from main.bounding_box_field_extraction_table import BoundingBoxFieldExtractionTable
import tkinter as tk


class BoundingBoxElements:
    def __init__(self, canvas, bounding_boxes_cache, image, master):
        self.master = master
        self.canvas = canvas
        self.rect = None
        self.start_x = None
        self.bounding_boxes_cache = bounding_boxes_cache
        self.x = self.y = 0
        self.image_y, self.image_x, channels = image.shape
        self.box_count = 0
        self.image = image

    def bind_bounding_box_creation(self, *args):
        print("Current Image "+str(self.image_x) + "  " + str(self.image_y))
        self.canvas.press_bbox = self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.motion_bbox = self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.release_bbox = self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def __box_ids(self):
        return "bb_" + str(self.box_count)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', tags=self.__box_ids())

    def on_move_press(self, event: tk.Event):
        # Draw the rectangle:
        cur_x, cur_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def clear_all_bounding_box_elements(self):
        BoundingBoxFieldExtractionTable(self.canvas, self.master,
                                        self.bounding_boxes_cache
                                        ).clear_all_bounding_box_elements()

    def update_bounding_box_cache(self, event: tk.Event, box_id:str):
        # Store Rectangle
        cur_x, cur_y = (event.x, event.y)
        new_bounding_box = BoundingBox(Point(self.start_x, self.start_y), Point(cur_x, cur_y), box_id)
        # Publish position
        new_bounding_box.publish()

        # extract text:
        new_bounding_box.extract_text(self.image)
        self.bounding_boxes_cache[box_id] = new_bounding_box

    def unbind_mouse_events(self):
        self.canvas.unbind("<ButtonPress-1>", self.canvas.press_bbox)
        self.canvas.unbind("<B1-Motion>", self.canvas.motion_bbox)
        self.canvas.unbind("<ButtonRelease-1>", self.canvas.release_bbox)

    def on_button_release(self, event: tk.Event):
        box_id = self.__box_ids()
        self.update_bounding_box_cache(event, box_id)
        # unbind the mouse events
        self.unbind_mouse_events()
        # increment cached box_count
        self.box_count += 1
        # Create bounding box field extraction table row
        BoundingBoxFieldExtractionTable(self.canvas, self.master,
                                        self.bounding_boxes_cache
                                        ).setup_bounding_box_interaction_table_row_widgets(box_id)

        pass