import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout,
                             QLabel, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QDialog, QSpinBox, 
                             QFileDialog, QLineEdit, QCheckBox, QRadioButton)
from fbs_runtime.application_context.PyQt5 import ApplicationContext                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
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
    if user_input.exclude_header_yes.isChecked():
        header_time = int(user_input.header_time.currentText())
        header_time *= round(fps)
    elif user_input.exclude_header_no.isChecked():
        header_time = 0
    for index, timeline in enumerate(user_input.timeline_list, start = 1):
        if timeline.isChecked():
            my_resolve.add_sequence_batch_render_queue(index, user_input.presets.currentText(), user_input.render_folder, header_time)

class User_Input(QDialog):
    def __init__(self):
        super(User_Input, self).__init__()
        self.createFormGroupBox()

        # Create our buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.show_dialog)
        buttonBox.rejected.connect(self.reject)

        # Set our widget layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setGeometry(50, 50, 0, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle('Sequence Batch Render')
    
    # Main user input form
    def createFormGroupBox(self):
        self.presets = QComboBox(self)
        self.header_time = QComboBox(self)
        self.exclude_widget = QWidget()
        self.header_widget = QWidget()
        
        self.formGroupBox = QGroupBox('Batch Renderer')
        # Create layout boxes for user inputs
        self.layout = QFormLayout()
        exclude_hbox = QHBoxLayout(self.exclude_widget)
        header_hbox = QHBoxLayout(self.header_widget)
        
        for preset in my_resolve.get_render_presets():
            self.presets.addItem(preset) # Add preset to our drop menu
        self.layout.addRow(QLabel('Select a render preset:'), self.presets)
        
        self.timeline_list = []
        for x in range(1, int(my_resolve.project.GetTimelineCount()) + 1):
            self.timeline_list.append(my_resolve.project.GetTimelineByIndex(x).GetName())
        
        # Add our timelines to possible render list
        for num, timeline in enumerate(self.timeline_list):
            self.timeline_list[num] = QCheckBox(timeline)
            self.timeline_list[num].stateChanged.connect(self.show_exclude_header)
            self.layout.addRow(self.timeline_list[num])
            
        exclude_header_label = QLabel('Exclude header?')
        header_time_label = QLabel('Number of seconds to exclude from render:')
        self.exclude_header_yes = QRadioButton('Yes')
        self.exclude_header_no = QRadioButton('No')
        self.exclude_header_yes.toggled.connect(self.show_header_time)
        self.exclude_header_no.toggled.connect(self.hide_header_time)
        self.exclude_header_no.setChecked(True)
        
        for x in range(1, 31):
            self.header_time.addItem(str(x))

        exclude_hbox.addWidget(exclude_header_label)
        exclude_hbox.addWidget(self.exclude_header_yes)
        exclude_hbox.addWidget(self.exclude_header_no)
        
        header_hbox.addWidget(header_time_label)
        header_hbox.addWidget(self.header_time)
        
        self.exclude_widget.hide()
        self.header_widget.hide()
        self.layout.addRow(self.exclude_widget)
        self.layout.addRow(self.header_widget)

        self.formGroupBox.setLayout(self.layout)
        self.show()
        
    # Get the file location from user 
    def show_dialog(self):
        self.hide()
        self.render_folder = str(QFileDialog.getExistingDirectory(self, 'Select Render Directory', os.path.expanduser('~/Desktop')))
        batch_render(self)
        
    # Change the state of QCheckBox
    def show_exclude_header(self, state):
        for timeline in self.timeline_list:
            if timeline.isChecked():
                self.exclude_widget.show()
                break
        else:
            self.exclude_widget.hide()
            self.exclude_header_no.setChecked(True)
            self.header_widget.hide()
            self.header_time.setCurrentIndex(0)
        QTimer.singleShot(1, self.resize_layout)
    
    def show_header_time(self, state):
        if state:
            self.header_widget.show()
        
    def hide_header_time(self, state):
        if state:
            self.header_widget.hide()
        QTimer.singleShot(1, self.resize_layout)
            
    def resize_layout(self):
        self.setGeometry(50, 50, 0, 0)
        
if __name__ == '__main__':
#     appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    marker_app = QApplication.instance() # checks if QApplication already exists
    if not marker_app: # create QApplication if it doesnt exist
        marker_app = QApplication(sys.argv)

    ex = User_Input()
    marker_app.exec_()
#     sys.exit(marker_app.exec_())