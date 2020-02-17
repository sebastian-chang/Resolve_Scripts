import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QComboBox, QGroupBox, QFormLayout, QPushButton,
                             QLabel, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QDialog, QSpinBox, 
                             QFileDialog, QLineEdit, QCheckBox, QRadioButton)
from fbs_runtime.application_context.PyQt5 import ApplicationContext                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
import os
import sys

import resolve_functions as my_resolve
from vfx_shot_list import VFX_Report_Input

# Create the PyQt5 class object for user input.
class Main_Input(QDialog):
    def __init__(self):
        super(Main_Input, self).__init__()
        self.createFormGroupBox()
        
        # Create our buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
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
        
        self.preset_row = QHBoxLayout()
        self.timeline_row = QHBoxLayout()

        self.presets = QComboBox(self)
        self.timelines = QComboBox(self)
        self.timelines.addItem('------------')
        
        for preset in my_resolve.get_render_presets():
            self.presets.addItem(preset) # Add preset to our drop menu
        for timeline in my_resolve.get_timelines().values():
            self.timelines.addItem(timeline) # Add timeline names to our drop menu
        self.timelines.currentIndexChanged.connect(self.selected_timeline)
            
        self.preset_row.addWidget(QLabel('Select a render preset:'))
        self.preset_row.addWidget(self.presets)
        self.layout.addRow(self.preset_row)

        self.timeline_row.addWidget(QLabel('Select a timeline to render from:'))
        self.timeline_row.addWidget(self.timelines)
        self.layout.addRow(self.timeline_row)
        
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
            self.clip_color_row = QHBoxLayout()
            self.clip_colors = QComboBox(self)
            self.clip_colors.clear()
            self.clip_colors.addItem('------------')
            for clip_color in my_resolve.get_clip_colors(value):
                self.clip_colors.addItem(clip_color) # Add clip color to our drop down menu
            self.clip_colors.currentIndexChanged.connect(self.selected_clip_color)
                        
            self.clip_color_row.addWidget(QLabel('Select a clip color to render:'))
            self.clip_color_row.addWidget(self.clip_colors)
            self.layout.addRow(self.clip_color_row)
        
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
            self.filename_prefix_textbox = QLineEdit(self)
            self.filename_prefix_textbox.setPlaceholderText('VFX')
            self.render_location = QLineEdit()
            self.browse_button = QPushButton('...')
            self.browse_button.clicked.connect(self.get_render_location)
            
            prefix_layout = QHBoxLayout()
            render_loc_layout = QHBoxLayout()
            
            prefix_layout.addWidget(QLabel('Custom filename prefix:'))
            prefix_layout.addWidget(self.filename_prefix_textbox)
            render_loc_layout.addWidget(QLabel('Render location:'))
            render_loc_layout.addWidget(self.render_location)
            render_loc_layout.addWidget(self.browse_button)
            
            user_file_layout = QVBoxLayout()
            user_file_layout.addLayout(prefix_layout)
            user_file_layout.addLayout(render_loc_layout)
            
            self.layout.addRow(user_file_layout)
            
        elif value == 0:
            self.layout.removeRow(3)
            QTimer.singleShot(1, self.resize_layout)
    
    # Function to resize window geomerty.
    def resize_layout(self):
        self.updateGeometry()
    
    # Get the file location from user 
    def get_render_location(self):
        folder_location = QFileDialog.getExistingDirectory(self, 'Select Render Directory', os.path.expanduser('~/Desktop'))
        
        if folder_location:
            self.render_location.setText(folder_location)

    def accept(self):
        self.report_ui = VFX_Report_Input()
        self.report_ui.createFormGroupBox(self)
        self.hide()
        self.report_ui.show()
        
if __name__ == '__main__':
#     appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    clip_color_app = QApplication.instance() # checks if QApplication already exists
    if not clip_color_app: # create QApplication if it doesnt exist
        clip_color_app = QApplication(sys.argv)

    ex = Main_Input()
    clip_color_app.exec_()
#     sys.exit(clip_color_app.exec_())