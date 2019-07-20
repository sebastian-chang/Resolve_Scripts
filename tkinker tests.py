import tkinter as tk
import tkinter.filedialog
import os

user_input_window = tk.Tk()
user_input_window.title('Clip Color Renderer')
clip_input = tk.Frame(user_input_window)
preset_input = tk.Frame(user_input_window)
clip_colors = ['Orange', 'Apricot', 'Yellow', 'Lime', 'Olive', 'Green', 'Teal', 'Navy', 'Blue', 'Purple', 'Violet', 'Pink', 'Tan', 'Beige', 'Brown', 'Chocolate']
preset_list = ['YouTube - 720p', 'YouTube - 1080p', 'YouTube - 2160p', 'Vimeo - 720p', 'Vimeo - 1080p', 'Vimeo - 2160p', 'ProRes Master', 'H.264 Master', 'H.265 Master', 'IMF - Generic', 'IMF - Netflix', 'FCP - Final Cut Pro 7', 'FCP - Final Cut Pro X', 'Premiere XML', 
                 'Pro Tools', 'Audio Only', 'Yellow - DNxHD 36 HD 2398', 'Pink - ProResProxy HD 2398', 'Green - ProResProxy HD 2398']
c = tk.IntVar()
p = tk.IntVar()

def show_choices():
    preset_input.destroy()
    file_directory = get_directory()
    folder_name = os.path.basename(file_directory)
    print(clip_colors[c.get()])
    print(preset_list[p.get()])
    print(file_directory)
    print(folder_name)
    user_input_window.destroy()

def get_directory():
    user_input_window.withdraw()
    directory = tk.filedialog.askdirectory(title = 'Choose a folder to render to:', mustexist = True, initialdir='/Users/schang')
    return directory

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

    tk.Button(preset_input, text = 'Okay', command = show_choices, width = 10, relief = tk.GROOVE, bd = 5, \
                state = tk.ACTIVE).grid(row = row_num, sticky = tk.SE)

def pick_color():
    user_input_window.deiconify()
    clip_input.pack()
    tk.Label(clip_input, text='What clip color would you like to render?', justify = 'center', \
            padx = 20, font = 'Verdana 12 bold').grid(row = 0, sticky = tk.N)

    row_num = 1
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

pick_color()

user_input_window.mainloop()