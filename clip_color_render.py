import importlib.util
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
import os

# Initialize  additional Python scripts needed to run code.
# timecode.py is used to do any timecode conversions.
# python_get_resolve.py is script giving By BlackMagicDesign to load resolve python modules.
resolve_func_path = '/Users/schang/Google Drive/Editables/Python/Resolve/resolve_functions.py'
spec1 = importlib.util.spec_from_file_location('resolve', resolve_func_path)

resolve = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(resolve)

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