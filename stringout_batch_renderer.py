import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout,
                             QLabel, QDialogButtonBox, QVBoxLayout, QDialog, QSpinBox, 
                             QFileDialog, QLineEdit)
from fbs_runtime.application_context.PyQt5 import ApplicationContext                             
from PyQt5.QtGui import QIcon
import os
import sys

# Initialize  additional Python scripts needed to run code.
# timecode.py is used to do any timecode conversions.
# python_get_resolve.py is script giving By BlackMagicDesign to load resolve python modules.
resolve_func_path = '/Users/schang/Google Drive/Editables/Python/Resolve/resolve_functions.py'
spec1 = importlib.util.spec_from_file_location('resolve', resolve_func_path)

resolve = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(resolve)

def batcher_render(user_input):
    resolve.add_stringout_batch_render_queue(user_input.timelines.currentIndex() + 1, user_input.presests.currentText(), user_input.render_folder)

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
        
        self.setWindowTitle('Timeline Batch Render')
        
    # Main user input form    
    def createFormGroupBox(self):
        self.presests = QComboBox(self)
        self.timelines = QComboBox(self)
        
        for preset in resolve.get_render_presets():
            self.presests.addItem(preset) # Add preset to our drop menu
        for timeline in resolve.get_timelines().values():
            self.timelines.addItem(timeline) # Add timeline names to our drop menu
            
        self.formGroupBox = QGroupBox('Batch Renderer')
        layout = QFormLayout()
        layout.addRow(QLabel('Select a render preset:'), self.presests)
        layout.addRow(QLabel('Select a timeline to render from:'), self.timelines)
        self.formGroupBox.setLayout(layout)
        self.show()
        
    # Get the file location from user 
    def showDialog(self):
        self.hide()
        self.render_folder = str(QFileDialog.getExistingDirectory(self, 'Select Render Directory', os.path.expanduser('~/Desktop')))
        batcher_render(self)


if __name__ == '__main__':
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    # # app = QApplication(sys.argv)
    marker_app = QApplication.instance() # checks if QApplication already exists
    if not marker_app: # create QApplication if it doesnt exist
        marker_app = QApplication(sys.argv)
        # marker_app = QWidget.QApplication(sys.argv)
    ex = User_Input()
    marker_app.exec_()
    # sys.exc_info(appctxt.app.exec_())