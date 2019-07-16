import tkinter as tk      

def callback():
    name = tk.askaskopenfilename() 
    print(name)
    
errmsg = 'Error!'
tk.Button(text='File Open', command=callback).pack(fill=tk.X)
mainloop()