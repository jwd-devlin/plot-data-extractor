import tkinter as tk


class BoundingBoxFieldExtractionTable:
    def __init__(self, canvas, master_frame, bounding_boxes_cache: dict):
        self.master_frame = master_frame
        self.bounding_boxes_cache = bounding_boxes_cache
        self.canvas = canvas

    def create_remove_button(self, current_box):
        text_box_remove_id = "X:" + current_box.canvas_id
        remove_bounding = tk.Button(self.master_frame, text=text_box_remove_id, bg="red",
                                    command=lambda: self.clear_bounding_box_element(current_box.canvas_id))
        remove_bounding.grid(row=current_box.index, column=0)
        current_box.set_delete_button_widget(remove_bounding)

    def create_text_entry(self, current_box):
        entry_field = tk.Entry(self.master_frame, textvariable=current_box.entry_converted_image_display_text)
        entry_field.grid(row=current_box.index, column=1)
        current_box.set_text_entry_widget(entry_field)

    def clear_bounding_box_element(self, selected_box_id: str):
        selected_bounding_box = self.bounding_boxes_cache[selected_box_id]
        # Button delete
        button = selected_bounding_box.delete_button_widget
        button.destroy()

        # Remove text entry
        entry_field = selected_bounding_box.image_text_entry_field_widget
        entry_field.destroy()

        # Bounding Box Delete
        self.canvas.delete(selected_box_id)

        # Cached Bounding Box data
        del self.bounding_boxes_cache[selected_box_id]
        print(" Removed " + selected_box_id)

    def clear_all_bounding_box_elements(self):
        for selected_box_id in list(self.bounding_boxes_cache):
            self.clear_bounding_box_element(selected_box_id)

    def setup_bounding_box_interaction_table_row_widgets(self, selected_box_id):
        """

        Creates:
         - a remove button for the bounding box
         - text field entry for the converted text from the image.


        """
        current_box = self.bounding_boxes_cache[selected_box_id]
        self.create_text_entry(current_box)
        self.create_remove_button(current_box)
