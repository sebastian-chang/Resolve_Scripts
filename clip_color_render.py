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
        self.clip_colors = QComboBox(self)
        self.suffix_widget = QWidget()
        self.suffix_filename_widget = QWidget()
        
        self.formGroupBox = QGroupBox('Batch Renderer')
        # Create layout boxes for user inputs
        self.layout = QFormLayout()
        suffix_hbox = QHBoxLayout(self.suffix_widget)
        suffix_filename_hbox = QHBoxLayout(self.suffix_filename_widget)
        
        # Add our presets to drop down menu
        for preset in my_resolve.get_render_presets():
            self.presets.addItem(preset) # Add preset to our drop down menu
        self.layout.addRow(QLabel('Select a render preset:'), self.presets)

        # Add our presets to drop down menu
        for clip_color in my_resolve.get_clip_colors():
            self.clip_colors.addItem(clip_color) # Add clip color to our drop down menu
        self.layout.addRow(QLabel('Select a clip color to render:'), self.clip_colors)

        self.timeline_list = []
        for x in range(1, int(my_resolve.project.GetTimelineCount()) + 1):
            self.timeline_list.append(my_resolve.project.GetTimelineByIndex(x).GetName())
        
        # Add our timelines to possible render list
        for num, timeline in enumerate(self.timeline_list):
            self.timeline_list[num] = QCheckBox(timeline)
            self.timeline_list[num].stateChanged.connect(self.show_exclude_header)
            self.layout.addRow(self.timeline_list[num])
            
        suffix_label = QLabel('Add a suffix to file name?')
        self.suffix_yes = QRadioButton('Yes')
        self.suffix_no = QRadioButton('No')
        self.suffix_yes.toggled.connect(self.show_suffix_filename)
        self.suffix_no.toggled.connect(self.hide_suffix_filename)
        self.suffix_no.setChecked(True)

        suffix_hbox.addWidget(suffix_label)
        suffix_hbox.addWidget(self.suffix_yes)
        suffix_hbox.addWidget(self.suffix_no)

        suffix_filename_label = QLabel('Suffix:')

        suffix_filename_hbox.addWidget(suffix_filename_label)
        
        self.suffix_filename_widget.hide()
        self.layout.addRow(self.suffix_widget)
        self.layout.addRow(self.suffix_filename_widget)

        self.formGroupBox.setLayout(self.layout)
        self.show()
        
    # Get the file location from user 
    def show_dialog(self):
        self.hide()
        self.render_folder = str(QFileDialog.getExistingDirectory(self, 'Select Render Directory', os.path.expanduser('~/Desktop')))
        batch_render(self)
        
    # Change the state of QCheckBox 
    def show_suffix_filename(self, state):
        if state:
            self.suffix_filename_widget.show()
        
    def hide_suffix_filename(self, state):
        if state:
            self.suffix_filename_widget.hide()
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
































def pick_color():
    user_input_window.deiconify()
    clip_input.pack()
    tk.Label(clip_input, text='What clip color would you like to render?', justify = 'center', \
            padx = 20, font = 'Verdana 12 bold').grid(row = 0, sticky = tk.N)

    row_num = 1
    c.set(0)
    for position, clip_color in enumerate(clip_colors):
        try:
            tk.Radiobutton(clip_input, text=clip_color, indicatoron = 0, width = 10, \
                            variable = c, value = position, bg = clip_color, relief = tk.RAISED).grid(row = row_num, sticky = tk.N)
        #    tk.Label(user_input, bg = clip_color, width = 10, relief = tk.FLAT).grid(row = row_num)
        except tk.TclError:
            tk.Radiobutton(clip_input, text=clip_color, indicatoron = 0, width = 10, \
                            variable = c, value = position, bg = '#ff8000', relief = tk.RAISED).grid(row = row_num, sticky = tk.N)
        # tk.Label(user_input, bg = '#ff8000', width = 10, relief = tk.FLAT).grid(row = row_num)
        row_num += 1

    tk.Button(clip_input, text = 'Okay', command = pick_render, width = 10, relief = tk.GROOVE, bd = 5, \
                state = tk.ACTIVE).grid(row = row_num, sticky = tk.SE)

def pick_render():
    clip_input.destroy()
    preset_input.pack()
    tk.Label(preset_input, text='Which preset you would like to use to render?', justify = 'center', \
            padx = 20, font = 'Verdana 12 bold').grid(row = 0, sticky = tk.N)

    p.set(0)
    row_num = 1
    for position, preset in enumerate(preset_list):
        tk.Radiobutton(preset_input, text=preset, justify = tk.LEFT, \
                        variable = p, value = position, relief = tk.RAISED).grid(row = row_num, sticky = tk.W)
        row_num += 1

    tk.Button(preset_input, text = 'Okay', command = confirm_render, width = 10, relief = tk.GROOVE, bd = 5, \
                state = tk.ACTIVE).grid(row = row_num, sticky = tk.SE)

def get_directory():
    user_input_window.withdraw()
    directory = tk.filedialog.askdirectory(title = 'Choose a folder to render to:', mustexist = True, initialdir=os.path.expanduser('~'))
    return directory

def show_choices():
    preset_input.destroy()
    file_directory = get_directory()
    folder_name = os.path.basename(file_directory)
    print(clip_colors[c.get()])
    print(preset_list[p.get()])
    print(file_directory)
    print(folder_name)
    user_input_window.destroy()

def confirm_render():
    preset_input.destroy()
    file_directory = get_directory()
    user_input_window.deiconify()
    confirm_input.pack()
    label = tk.ttk.Label(confirm_input, wraplength = 300, justify = tk.CENTER, text = f"Please confirm you would like to render all clips with the '{clip_colors[c.get()]}', label with the preset '{preset_list[p.get()]}' to the file location '{file_directory}'.")
    cancel = tk.ttk.Button(confirm_input, text = 'Cancel', command = user_input_window.destroy)
    render = tk.ttk.Button(confirm_input, text = 'Add Jobs', command = add_render_jobs)
    label.grid(columnspan = 2, row = 0, sticky = (tk.N))
    cancel.grid(column = 0, row = 1, sticky = (tk.W))
    render.grid(column = 1, row = 1, sticky = (tk.E))

def add_render_jobs():
    resolve.add_clip_color_to_render_queue(clip_colors[c.get()], preset_list[p.get()], file_directory)
    user_input_window.destroy()

user_input_window = tk.Tk()
user_input_window.title('Clip Color Render')
clip_input = tk.Frame(user_input_window)
preset_input = tk.Frame(user_input_window)
confirm_input = tk.ttk.Frame(user_input_window, width = 300, height = 50)
# confirm_input.config(width = 200, height = 50)

loaded_clip_colors = []
clip_colors = resolve.get_clip_colors()
preset_list = resolve.get_render_presets()
file_directory = ''
c = tk.IntVar()
p = tk.IntVar()

pick_color()

user_input_window.mainloop()