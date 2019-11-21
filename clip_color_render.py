import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout,
                             QLabel, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QDialog, QSpinBox, 
                             QFileDialog, QLineEdit, QCheckBox, QRadioButton)
from fbs_runtime.application_context.PyQt5 import ApplicationContext                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
import os
import sys

# Initialize  additional Python scripts needed to run code.
# timecode.py is used to do any timecode conversions.
# python_get_resolve.py is script giving By BlackMagicDesign to load resolve python modules.
resolve_func_path = '/Users/schang/Google Drive/Editables/Python/Resolve/resolve_functions.py'
spec1 = importlib.util.spec_from_file_location('resolve', resolve_func_path)

my_resolve = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(my_resolve)

def batch_render(user_input):
    my_resolve.add_clip_color_to_render_queue(user_input.timelines.currentIndex(), user_input.presets.currentText(), user_input.clip_colors.currentText(), user_input.filename_suffix_textbox.text(), user_input.render_folder)

# Create the PyQt5 class object for user input.
class User_Input(QDialog):
    def __init__(self):
        super(User_Input, self).__init__()
        self.createFormGroupBox()
        
        # Create our buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.showDialog)
        buttonBox.rejected.connect(self.reject)
        
        # Set our widget layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setGeometry(50, 50, 0, 0)
        self.setLayout(mainLayout)
        
        self.setWindowTitle('Clip Color Batch Render')
        
    # Main user input form    
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox('Clip Color Batch Renderer')
        self.layout = QFormLayout()

        self.render_color_widget = QWidget()
        self.filename_suffix_widget = QWidget()
        
        
        self.presets = QComboBox(self)
        self.timelines = QComboBox(self)
        self.timelines.addItem('------------')
        
        for preset in my_resolve.get_render_presets():
            self.presets.addItem(preset) # Add preset to our drop menu
        for timeline in my_resolve.get_timelines().values():
            self.timelines.addItem(timeline) # Add timeline names to our drop menu
        self.timelines.currentIndexChanged.connect(self.selected_timeline)
            
        self.layout.addRow(QLabel('Select a render preset:'), self.presets)
        self.layout.addRow(QLabel('Select a timeline to render from:'), self.timelines)
        
        self.formGroupBox.setLayout(self.layout)
        self.show()
        
    def selected_timeline(self, value):           
        if value != 0:
            if self.layout.rowCount() == 4:
                self.layout.removeRow(3)
            if self.layout.rowCount() == 3:
                self.layout.removeRow(2)
                QTimer.singleShot(1, self.resize_layout)
            # Create dropdown menu for clip colors.
            self.clip_colors = QComboBox(self)
            self.clip_colors.clear()
            self.clip_colors.addItem('------------')
            for clip_color in my_resolve.get_clip_colors(value):
                self.clip_colors.addItem(clip_color) # Add clip color to our drop down menu
            self.clip_colors.currentIndexChanged.connect(self.selected_clip_color)
            
            self.layout.addRow(QLabel('Select a clip color to render:'), self.clip_colors)
        
        elif value == 0:
            if self.layout.rowCount() == 4:
                self.layout.removeRow(3)
            if self.layout.rowCount() == 3:
                self.layout.removeRow(2)
            QTimer.singleShot(1, self.resize_layout)
    
    def selected_clip_color(self, value):
        if value != 0:
            if self.layout.rowCount() == 4:
                self.layout.removeRow(3)
                QTimer.singleShot(1, self.resize_layout)
            self.filename_suffix_textbox = QLineEdit(self)
            self.layout.addRow(QLabel('Custom filename suffix:'), self.filename_suffix_textbox)
        elif value == 0:
            self.layout.removeRow(3)
            QTimer.singleShot(1, self.resize_layout)
    
    # Function to resize window geomerty.
    def resize_layout(self):
        self.updateGeometry()
    
    # Get the file location from user 
    def showDialog(self):
        self.hide()
        self.render_folder = str(QFileDialog.getExistingDirectory(self, 'Select Render Directory', os.path.expanduser('~/Desktop')))
        batch_render(self)
        
if __name__ == '__main__':
#     appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    marker_app = QApplication.instance() # checks if QApplication already exists
    if not marker_app: # create QApplication if it doesnt exist
        marker_app = QApplication(sys.argv)

    ex = User_Input()
    marker_app.exec_()
#     sys.exit(marker_app.exec_())