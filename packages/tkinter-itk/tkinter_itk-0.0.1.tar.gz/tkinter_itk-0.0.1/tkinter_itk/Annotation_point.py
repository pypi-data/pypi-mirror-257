import tkinter as tk  
from .Utils import  PatchedCanvas


class Annotation_point():
    def __init__(self, unique_id, serie_ID, coords: list = [], **kwargs) -> None:
        super().__init__()
        self.ITK_coords = coords
        self.serie_ID = serie_ID
        self.unique_id = unique_id
        self.kwargs = kwargs
        if "color" not in kwargs:
            self.kwargs["fill"] = "red"
        else:
            self.kwargs["fill"] = kwargs["color"]
            self.kwargs.pop("color")
        if "size" not in kwargs:
            self.size = 5
        else:
            self.size = kwargs["size"]   
            self.kwargs.pop("size")     

    def get_ITK_coords(self):
        return self.ITK_coords
        
    def get_serie_ID(self):
        return self.serie_ID
    
    def get_unique_id(self):
        return self.unique_id
    
    def set_ITK_coords(self, ITK_coords):
        self.ITK_coords = ITK_coords

    def place_annotation_on_canvas(self, canvas: PatchedCanvas| tk.Canvas, canvas_X: int, canvas_Y: int, size: int = 5, **kwargs):
        for key in kwargs:
            self.kwargs[key] = kwargs[key]
        if "outline" not in kwargs:
            self.kwargs["outline"] = "black"
        if "width" not in kwargs:
            self.kwargs["width"] = 1
        # if "activefill" not in kwargs:
        #     self.kwargs["activefill"] = "blue"
        self.size = size
        
        canvas_id = canvas.create_rectangle(canvas_X - self.size, canvas_Y - self.size, canvas_X + self.size, canvas_Y + self.size, **self.kwargs)
        return [canvas_id]
    
    def move_annotation_on_canvas(self, canvas: PatchedCanvas| tk.Canvas, canvas_X: int, canvas_Y: int, canvas_ids: int, **kwargs):
        canvas.coords(canvas_ids[0], canvas_X - self.size, canvas_Y - self.size, canvas_X + self.size, canvas_Y + self.size)
        return canvas_ids
    
    