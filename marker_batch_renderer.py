import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout, QGridLayout,
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

# Add all marker sections of user's choosing from given sequence to given folder location for all clips. 
def batch_render(user_input):
    my_resolve.add_marker_stringout_batch_render_queue(user_input.timelines.currentIndex(), user_input.presets.currentText(), user_input.marker_colors.currentText(), user_input.filename_suffix_textbox.text(), user_input.render_folder)

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
        
        self.setWindowTitle('Marker Batch Render')
        
    # Main user input form    
    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox('Marker Batch Renderer')
        self.layout = QFormLayout()
        
        # Create our widgets
        self.render_color_widget = QWidget()
        self.filename_suffix_widget = QWidget()
        
        # Create our layout boxes
        self.render_color_hbox = QHBoxLayout(self.render_color_widget)
        self.filename_suffix_hbox = QHBoxLayout(self.filename_suffix_widget)
        
        # Create our drop down items.  Fill first tiem of timelines with a null answer.
        self.presets = QComboBox(self)
        self.timelines = QComboBox(self)
        self.timelines.addItem('------------')
        
        for preset in my_resolve.get_render_presets():
            self.presets.addItem(preset) # Add preset to our drop menu
        for timeline in my_resolve.get_timelines().values():
            self.timelines.addItem(timeline) # Add timeline names to our drop menu
        self.timelines.currentIndexChanged.connect(self.selected_timeline)
            
        # Add our first two drop downs to our main layout.
        self.layout.addRow(QLabel('Select a render preset:'), self.presets)
        self.layout.addRow(QLabel('Select a timeline to render from:'), self.timelines)
        
        self.formGroupBox.setLayout(self.layout)
        self.show()
        
    # When a timeline is selected add a drop down menu full of marker colors.
    def selected_timeline(self, value):
        # Check to see if user went back to default null option.  Remove/reset unneeded rows.
        if value != 0:
            self.layout.removeRow(3)
            self.layout.removeRow(2)
            QTimer.singleShot(1, self.resize_layout)
            # Create new dropdown menu full of marker clip colors.  Add null option first.
            self.marker_colors = QComboBox(self)
            self.marker_colors.clear()
            self.marker_colors.addItem('------------')
            for marker_color in my_resolve.get_marker_colors(value):
                self.marker_colors.addItem(marker_color) # Add clip color to our drop down menu
            self.marker_colors.currentIndexChanged.connect(self.selected_color_marker)
            
            self.layout.addRow(QLabel('Select a marker color to render:'), self.marker_colors)
        
        elif value == 0:
            self.layout.removeRow(3)
            self.layout.removeRow(2)
            QTimer.singleShot(1, self.resize_layout)
    
    # When a marker color has been selected ask if user would like to add a filename suffix.
    def selected_color_marker(self, value):
        # Check to see if user has selected default null option.  Remove/reset unneeded rows.
        if value != 0:
            self.layout.removeRow(3)
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
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    marker_app = QApplication.instance() # checks if QApplication already exists
    if not marker_app: # create QApplication if it doesnt exist
        marker_app = QApplication(sys.argv)

    ex = User_Input()
    marker_app.exec_()
    # sys.exit(appctxt.app.exec_())