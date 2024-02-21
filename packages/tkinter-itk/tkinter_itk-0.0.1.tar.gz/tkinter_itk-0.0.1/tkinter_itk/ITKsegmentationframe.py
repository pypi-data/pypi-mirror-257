from PIL import Image, ImageTk
import SimpleITK as sitk
import numpy as np
import logging

from .ITKviewerframe import ITKviewerFrame

def set_mask_value(image, mask, value):
    msk32 = sitk.Cast(mask, sitk.sitkFloat32)
    msk32.CopyInformation(image)
    return sitk.Cast(sitk.Cast(image, sitk.sitkFloat32) *
                     sitk.InvertIntensity(msk32, maximum=1.0) + 
                     msk32*value, image.GetPixelID())

class ITKsegmentationFrame(ITKviewerFrame):
    def __init__(self, parent, **kwargs):
        """ Initialize the ITK viewer Frame """
        self.max_layers = 255
        self.seg_image_needs_update = True
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.seg_image = ImageTk.PhotoImage(self.get_image_from_seg_array())

    def initialize(self):
        self.segmentation_serie_manager = self.FrameManager.parent.segmentation_serie_manager

        if self.serie_ID is None:
            self.ITK_seg_image = sitk.Image(self.ITK_image.GetSize(), sitk.sitkUInt8)
            self.ITK_seg_image.CopyInformation(self.ITK_image)
        else:
            self.ITK_seg_image = self.segmentation_serie_manager.get_image(self.serie_ID, add_if_not_exist=True)
        
        super().initialize()
    
    def load_new_CT(self, window: int = None, level: int = None, ITK_image: sitk.Image = None,**kwargs):
        """placeholder"""
        super().load_new_CT(window, level, ITK_image= ITK_image, update_image = False, **kwargs)
        self.seg_image_needs_update = True
        if self.serie_ID is None:
            self.ITK_seg_image = sitk.Image(ITK_image.GetSize(), sitk.sitkUInt8)
            self.ITK_seg_image.CopyInformation(ITK_image)
        else:
            self.ITK_seg_image = self.segmentation_serie_manager.get_image(self.serie_ID, add_if_not_exist=True)
        self.update_image()
    
    def get_image_from_seg_array(self):
        """placeholder"""
        image_segmentation_array = sitk.GetArrayFromImage(sitk.LabelToRGB(self.ITK_seg_image[:,:, self.slice_index]))

        return Image.fromarray(image_segmentation_array, "RGB")

    
    def zoom_itk(self, *args, **kwargs):
        """ Zoom at x,y location"""
        
        # loading the preview image if it exists
        if self.segmentation_serie_manager.get_preview(self.serie_ID) is not None:
            self.ITK_seg_image = self.segmentation_serie_manager.get_preview(self.serie_ID)
        else:
            self.ITK_seg_image = self.segmentation_serie_manager.get_image(self.serie_ID, add_if_not_exist=True) # fix for when segementation is replaced by another image instance 
            #TODO: find a better fix
                                       
        NP_seg_slice = self.ITK_seg_image[:,:, self.slice_index]
        if NP_seg_slice.GetSize() != self.slice_gray_ITK_image.GetSize():
            logging.warning("Segmentation image size does not match image size")
            self.ITK_seg_image = sitk.Image(self.slice_gray_ITK_image.GetSize(), sitk.sitkUInt8)
            self.ITK_seg_image.CopyInformation(self.slice_gray_ITK_image)
            return
        NP_seg_slice.CopyInformation(self.slice_gray_ITK_image)

        pixel_type = self.slice_gray_ITK_image.GetPixelID()
        if pixel_type != sitk.sitkVectorUInt8 and pixel_type != sitk.sitkVectorUInt16 and pixel_type != sitk.sitkVectorUInt32 and pixel_type != sitk.sitkVectorUInt64:
            self.slice_ITK_image = sitk.LabelOverlay(self.slice_gray_ITK_image, NP_seg_slice, opacity=0.8)
        return super().zoom_itk(*args, **kwargs)        


    def set_segmentation_point_current_slice(self, x, y, layer_height):
        self.ITK_seg_image[x, y, self.slice_index] = layer_height
        self.seg_image_needs_update = True
        self.update_image()

    def set_segmentation_mask_current_slice(self, layer_height: int, mask: np.ndarray):
        
        self.ITK_seg_image[:, :, self.slice_index] = set_mask_value(self.ITK_seg_image[:, :, self.slice_index], mask, layer_height) 
        self.seg_image_needs_update = True
        self.update_image()
    
    def set_segmentation_preview_mask_current_slice(self, layer_height: int, mask: np.ndarray):
        preview_image = self.segmentation_serie_manager.get_segmentation(self.serie_ID, add_if_not_exist=True).__copy__()
        preview_image[:, :, self.slice_index] = set_mask_value(preview_image[:, :, self.slice_index], mask, layer_height)
        self.segmentation_serie_manager.set_preview(self.serie_ID, preview_image)
        self.seg_image_needs_update = True
        self.update_image()

    def clear_segmentation_mask_current_slice(self, layer_height: int = None):
        if layer_height is None:
            self.ITK_seg_image[:, :, self.slice_index] = 0
        else:
            self.ITK_seg_image[:, :, self.slice_index] = set_mask_value(self.ITK_seg_image[:, :, self.slice_index], self.ITK_seg_image[:, :, self.slice_index] == layer_height, 0)
        self.seg_image_needs_update = True
        self.update_image()

    def next_slice(self):
        self.seg_image_needs_update = True
        return super().next_slice()
    
    def previous_slice(self):
        self.seg_image_needs_update = True
        return super().previous_slice()

    def get_NP_seg_slice(self):
        return sitk.GetArrayFromImage(self.ITK_seg_image[:,:, self.slice_index])
    
    def accept_preview(self):
        self.segmentation_serie_manager.accept_preview(self.serie_ID)