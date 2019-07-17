import tkinter as tk
import tkinter.filedialog

user_input = tk.Tk()
clip_colors = ['Orange', 'Apricot', 'Yellow', 'Lime', 'Olive', 'Green', 'Teal', 'Navy', 'Blue', 'Purple', 'Violet', 'Pink', 'Tan', 'Beige', 'Brown', 'Chocolate']

c = tk.IntVar()

def ShowChoice():
    print(clip_colors[c.get()])
    user_input.destroy()

tk.Label(user_input, text='What clip color would you like to render?', justify = 'center', \
        padx = 20, font = 'Verdana 12 bold').grid(row = 0, sticky = tk.N)

row_num = 1
for position, clip_color in enumerate(clip_colors):
    try:
        tk.Radiobutton(user_input, text=clip_color, indicatoron = 0, width = 10, \
                        variable = c, value = position, bg = clip_color, relief = tk.RAISED).grid(row = row_num, sticky = tk.W)
    #    tk.Label(user_input, bg = clip_color, width = 10, relief = tk.FLAT).grid(row = row_num)
    except tk.TclError:
        tk.Radiobutton(user_input, text=clip_color, indicatoron = 0, width = 10, \
                        variable = c, value = position, bg = '#ff8000', relief = tk.RAISED).grid(row = row_num, sticky = tk.W)
       # tk.Label(user_input, bg = '#ff8000', width = 10, relief = tk.FLAT).grid(row = row_num)
    row_num += 1

tk.Button(user_input, text = 'Okay', command = ShowChoice, width = 10, relief = tk.GROOVE, bd = 5, \
            state = tk.ACTIVE).grid(row = row_num, sticky = tk.SE)

user_input.mainloop()




def quit_loop():
    print "Selection:",var.get()
    global selection
    selection = var.get()
    master.quit()

Label(master, text = "Select OCR language").grid(row=0, sticky=W)
Radiobutton(master, text = "default", variable=var, value = 1).grid(row=1, sticky=W)
Radiobutton(master, text = "user-defined", variable=var, value = 2).grid(row=2, sticky=W)
Button(master, text = "OK", command=quit_loop).grid(row=3, sticky=W)


tk.Label(user_input, text="Select Render Destination:")
save_directory = tk.filedialog.askdirectory()
print(save_directory)


import tkinter.filedialog

user_input = Tk()

user_input.directory = tkinter.filedialog.askdirectory()

print(type(user_input))
print(type(user_input.directory))
print(user_input.directory)


import tkinter as tk
import tkinter.filedialog

user_input = tk.Tk()
user_input.withdraw()
save_directory = tk.filedialog.askdirectory()
print(save_directory)

def select_export():
    selected = filedialog.askdirectory(initialdir=getcwd(), title='Select Export Tables Folder')





import tkinter as tk
import tkinter.filedialog
 
root = tkinter.Tk()
 
def print_path():  
    f = tkinter.filedialog.askdirectory(
        parent=root, initialdir='/Users/schang',
        title='Export Folder'
        )
 
    print(f)
 
b1 = tkinter.Button(root, text='Print path', command=print_path)  
b1.pack(fill='x')
 
root.mainloop()  

import os

root = tkinter.Tk()
root.update()
root.withdraw()

current_directory = tkinter.filedialog.askdirectory()
file_name = "test.txt"

file_path = os.path.join(current_directory,file_name)
print(file_path)


root = tk.Tk()
v = tk.IntVar()
v.set(1)  # initializing the choice, i.e. Python

languages = [
    ("Python",1),
    ("Perl",2),
    ("Java",3),
    ("C++",4),
    ("C",5)
]

def ShowChoice():
    print(v.get())

tk.Label(root, 
         text="""Choose your favourite 
programming language:""",
         justify = tk.LEFT,
         padx = 20).pack()

for val, language in enumerate(languages):
    tk.Radiobutton(root, 
                  text=language,
                  padx = 20, 
                  variable=v, 
                  command=ShowChoice,
                  value=val).pack(anchor=tk.W)

slogan = tk.Button(frame,
                   text="Hello",
                   command=write_slogan)
slogan.pack(side=tk.LEFT)

root.mainloop()





import tkinter.colorchooser

def callback():
    result = tk.colorchooser.askcolor(color="#6A9662", 
                      title = "Bernd's Colour Chooser") 
    print(result)
    
root = tk.Tk()
tk.Button(root, 
       text='Choose Color', 
       fg="darkgreen", 
       command=callback).pack(side=tk.LEFT, padx=10)
tk.Button(text='Quit', 
       command=root.destroy,
       fg="red").pack(side=tk.LEFT, padx=10)
tk.mainloop()