import logging
import tkinter as tk
from tkinter import Menu, ttk
import os 

import SimpleITK as sitk

from .menu.fileMenu import FileMenu
from .menu.helpMenu import HelpMenu
from .menu.segmentationMenu import SegemntationMenu

from .topbar import Topbar
from .ImagesFrameManager import imagesFrameManager, example_dual_frame_list
from .DICOM_serie_manager import DICOM_serie_manager
from .segmentation_serie_manager import Segmentation_serie_manager
from .Annotation_manager import Annotation_manager
#import progressbar



logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


#https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/
import importlib
import pkgutil

discovered_plugins = {}

plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')

for finder, name, ispkg in pkgutil.iter_modules([plugin_path]):
    if name.startswith('itk_viewer_plugin_'):
        try:
            module = importlib.import_module(f".plugins.{name}", package="tkinter_itk")
            discovered_plugins[name[18:]] = module.main_class
        except ModuleNotFoundError as e:
            logging.error(f"Failed to import plugin: {e}")

logging.info(discovered_plugins)

class Colors:
    """ Colors to RGB value """
    Black   = [0, 0, 0, 125]
    White   = [255, 255, 255, 125]
    Red     = [255, 0, 0, 125]
    Lime    = [0, 255, 0, 125]
    Blue    = [0, 0, 255, 125]
    Yellow  = [255, 255, 0, 125]
    Cyan    = [0, 255, 255, 125]
    Magenta = [255, 0, 255, 125]
    Silver  = [192, 192, 192, 125]
    Gray    = [128, 128, 128, 125]
    Maroon  = [128, 0, 0, 125]
    Olive   = [128, 128, 0, 125]
    Green   = [0, 128, 0, 125]
    Purple  = [128, 0, 128, 125]
    Teal    = [0, 128, 128, 125]
    Navy    = [0, 0, 128, 125]



class MainWindow(ttk.Frame):
    """ Main window class """
    plugins = {}
    
    segmentation_modes = ["None"]
    current_segmentation_mode = segmentation_modes[0]

    def __init__(self, mainframe, threading = False):
        """ Initialize the main Frame """
        ttk.Frame.__init__(self, master=mainframe)
        self.load_plugins()
        self.mainframe = mainframe
        self.threading = threading
        self.master.title('ITK viewer')
        self.master.geometry('800x800')  # size of the main window
        self.current_segmentation_mode = tk.StringVar(self.master)
        self.current_segmentation_mode.set(self.segmentation_modes[0])
        #TO DO: https://stackoverflow.com/a/41679642
        self.menubar = Menu(self.master)
        
        self.filemenu = FileMenu(self, self.menubar)
        self.menubar.add_cascade(label="Dicom", menu=self.filemenu)

        self.segmentationmenu = SegemntationMenu(self, self.menubar)
        self.menubar.add_cascade(label="Segmentation", menu=self.segmentationmenu)

        self.menubar.add_separator()

        self.helpmenu = HelpMenu(self, self.menubar)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        self.master.config(menu = self.menubar)

        self.label1 = Topbar(self, self.master)
        self.label1.grid(row=0, column=0, columnspan = 3, pady=5, sticky = tk.W + tk.E)

        self.DICOM_serie_manager = DICOM_serie_manager(self.master, bg="blue")
        self.DICOM_serie_manager.grid(row=1, column=0, pady=1, sticky = tk.N + tk.S)
        
        self.annotation_manager = Annotation_manager(self, self.DICOM_serie_manager)
        self.segmentation_serie_manager = Segmentation_serie_manager(self, self.DICOM_serie_manager)

        self.ITKviewer = imagesFrameManager(self.mainframe, image_label_layout = example_dual_frame_list, bg = "yellow", parent=self, threading=threading) # create ITK Frame
        # self.ITKviewer = ITKviewerFrame(self.mainframe, bg = "red") # create ITK Frame
        # self.ITKviewer = ITKsegmentationFrame(self.mainframe, bg = "red") # create ITK Frame
        self.ITKviewer.grid(row=1, column=1, columnspan = 2, sticky= tk.N + tk.S + tk.E + tk.W)  # show ITK 
        
        self.ITKviewer.rowconfigure(0, weight=1)
        self.ITKviewer.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(1, weight=1)


        self.label3 = tk.Label(self.master, text="Placeholder bottom", bg="green")
        self.label3.grid(row=2, column=0, columnspan = 3, pady=1, sticky = tk.W + tk.E)

        self.np_CT_array = None

    def new_image_input(self, image: sitk.Image = None, image_name: str = None, add = False):
        """ Placeholder"""
        self.master.update_idletasks()
        logging.info('Importing patient data')
        if image is None:
            DICOM_DIR = self.filemenu.get_filename()
            logging.debug(f'Importing patient data: {DICOM_DIR}')
            if add:
                logging.warning(f'Adding not implemented yet for DICOM_DIR')
            self.DICOM_serie_manager.load_DICOM_serie(DICOM_DIR, image_name)
        else:
            logging.debug(f'Importing patient data: {image_name}')
            self.DICOM_serie_manager.load_image_serie(image, image_name, add = add)
        self.DICOM_serie_manager.reset_preview_frames()
        return image_name

    def load_segmentation(self, segmentation: sitk.Image = None, serie_id: str = None):
        """ Placeholder"""
        self.master.update_idletasks()
        logging.info('Importing segmentation')
        if serie_id is None:
            logging.error('No segmentation name given')
            return
        if segmentation is None:
            logging.error('No segmentation given')
            return
        logging.debug(f'Importing segmentation: {serie_id}')
        self.segmentation_serie_manager.load_segmentation(segmentation, serie_id)
        return serie_id

    def load_plugins(self):
        """ Placeholder"""
        logging.info('Loading plugins')
        for plugin in discovered_plugins:
            self.plugins[plugin] = discovered_plugins[plugin](self)
            self.plugins[plugin].load_plugin()
        logging.info(f'Loaded plugins: {self.plugins}')

    def segmentation_mode_changed(self, *args):
        """ Placeholder"""
        logging.info(f'Segmentation mode changed to: {self.current_segmentation_mode.get()}')
        

    def save_segmentations(self):
        """ Placeholder"""
        logging.info('Saving segmentations')
        self.segmentation_serie_manager.save_segmentations(location = self.segmentationmenu.segmentation_folder)

    def load_segmentations(self):
        """ Placeholder"""
        logging.info('Loading segmentations')
        self.segmentation_serie_manager.load_segmentations(location = self.segmentationmenu.segmentation_folder)
    
    async def update(self) -> None:
        
        await self.ITKviewer.update_image_if_needed()
        return super().update()

def donothing():
    """ Place holder callback"""


if __name__ == "__main__":        
    ITKapp = tk.Tk()
    app = MainWindow(ITKapp, threading=False)
    ITKapp.mainloop()
    # while True:
    #     try:
    #         app.update()
    #     except KeyboardInterrupt:
    #         break

