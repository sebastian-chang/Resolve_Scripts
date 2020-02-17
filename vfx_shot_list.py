import importlib.util
from PyQt5.QtWidgets import (QApplication, QWidget, QFormLayout, QLabel, QHBoxLayout, QVBoxLayout, QDialog,
                            QGroupBox, QFileDialog, QLineEdit, QPushButton, QDialogButtonBox, QMessageBox)
from fbs_runtime.application_context.PyQt5 import ApplicationContext                             
from PyQt5.QtCore import Qt, QTimer
import os
import sys

import pandas as pd
import sys
import os

import batch_render as br

# Create the PyQt5 class object for user input.
class VFX_Report_Input(QDialog):
    def __init__(self):
        super(VFX_Report_Input, self).__init__()
        self.createFormGroupBox()
        
        # Create our buttons
        buttonBox = QDialogButtonBox()
        buttonBox.addButton('Accept', QDialogButtonBox.YesRole)
        buttonBox.addButton('Skip', QDialogButtonBox.YesRole)
        buttonBox.addButton(QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.send_to_render_queue)
        buttonBox.rejected.connect(self.reject)
        
        # Set our widget layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setGeometry(50, 50, 400, 50)
        self.setLayout(mainLayout)
        
        self.setWindowTitle('Clip Color Batch Render')
        
    # Main user input form    
    def createFormGroupBox(self, *user_input):
        if user_input:
            self.user_input = user_input[0]
            
        self.formGroupBox = QGroupBox('Would you like to add a Visual effects list?')
        self.layout = QFormLayout()        
        
        self.browse_button = QPushButton()
        self.browse_button.setText('Browse')
        self.browse_button.clicked.connect(self.find_file_location)
        self.vfx_report_loc = QLineEdit()
        self.vfx_report_loc.setFixedWidth(300)
        
        file_input_layout = QHBoxLayout()
        file_input_layout.addWidget(QLabel('VFX list file location:'))
        file_input_layout.addWidget(self.vfx_report_loc)
        file_input_layout.addWidget(self.browse_button)
        self.layout.addRow(file_input_layout)
        
        self.formGroupBox.setLayout(self.layout)
        self.show()
        
    def find_file_location(self):
        filename, filter = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~/Desktop'), filter = '*.csv; *.gsheet')
        
        if filename:
            self.vfx_report_loc.setText(filename)
            if self.check_vfx_list():
                return True
            else:
                QMessageBox.about(self, 'Error', "Please make sure the file you are selecting has columns with the following names: \
                                'SHOT NUMBER', 'TIMECODE IN', 'FILE NAME', 'SCENE'")
        
    def get_vfx_list(self):
        # Check to see if a link to a Google sheet was selected
        if self.vfx_report_loc.text().endswith('.gsheet'):
            # Get the document ID and append to the Google sheet URL formating we need in order to import to a Pandas data frame.
            temp_df = pd.read_csv(self.vfx_report_loc.text())
            doc_id = temp_df.columns[1]
            doc_id = doc_id.replace('"', '')[len("'doc_id':"):]
            google_sheet_url = 'https://docs.google.com/spreadsheets/d/' + doc_id + '/export?format=csv&gid=0'
            vfx_clip_df = pd.read_csv(google_sheet_url)
        else:
            vfx_clip_df = pd.read_csv(self.vfx_report_loc.text())
        
        return vfx_clip_df
        
    def check_vfx_list(self):
        self.vfx_df = self.get_vfx_list()
        
        if all(item in self.vfx_df.columns for item in  ['SHOT NUMBER', 'TIMECODE IN', 'FILE NAME', 'SCENE']):
            # Clean our data frame to only contain the data we can use.
            # Format data to fit our filenaming conventions 
            self.vfx_df = self.vfx_df.loc[:, ['SHOT NUMBER', 'TIMECODE IN', 'FILE NAME', 'SCENE']].dropna()
            self.vfx_df.loc[:, 'SHOT NUMBER'] = self.vfx_df.loc[:, 'SHOT NUMBER'].apply(lambda x: x.zfill(4))
            return True
        else:
            print('error')        
            return False
    
    def send_to_render_queue(self):
        try:
            br.clip_color_render(self.user_input, self.vfx_df)
        except AttributeError:
            br.clip_color_render(self.user_input)
        self.close()

if __name__ == '__main__':
    vfx_report_app = QApplication.instance()
    if not vfx_report_app:
        vfx_report_app = QApplication(sys.argv)
        
    vfx_ex = VFX_Report_Input()
    vfx_report_app.exec()