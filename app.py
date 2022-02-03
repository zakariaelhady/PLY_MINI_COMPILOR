#Modules used
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import subprocess
import os

global open_file_name
open_file_name=False

global dir_path
dir_path=os.path.abspath(".")


def new_file():
    my_text.delete("1.0",END)
    root.title("New File ")
    global open_file_name
    open_file_name=False

def open_file():
    my_text.delete("1.0",END)
    text_file=filedialog.askopenfilename(initialdir=dir_path,title="Open File",filetypes=(("Text","*.txt"),("Python file","*.py")))
    if text_file:
        global open_file_name
        open_file_name=text_file
    name=text_file
    name=name.replace(dir_path,"")
    root.title(f'{name} ')
    text_file=open(text_file,'r')
    stuff=text_file.read()
    my_text.insert(END,stuff)
    text_file.close()

def save_file():
    global open_file_name
    if open_file_name:
        text_file=open(open_file_name,'w')
        text_file.write(my_text.get(1.0,END))
        text_file.close()
    else:
        global dir_path
        text_file=filedialog.asksaveasfilename(defaultextension=".*",initialdir=dir_path,title="Save File",filetypes=(("Text","*.txt"),("Python file","*.py")))
        if text_file:
            name=text_file
            name=name.replace(dir_path,"")
            root.title(f'{name} ') 
            text_file=open(text_file,'w')
            text_file.write(my_text.get(1.0,END))
            
            open_file_name=name
            text_file.close()
            

def execute_file():
    if open_file_name:
        proc = subprocess.Popen('cmd.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        os.chdir(dir_path)
        comd='python main.py {}   '.format(open_file_name)
        comd=comd.encode('utf-8')
        proc.stdin.write(comd)
        stdout = proc.communicate(proc.stdout.readline())
        execute_text.insert(END,stdout)



def insert_line_numbers():
    global lines
    data = ""
    for i in range(1, 50):
        data += str(i) + "\n"
    lines.insert(END,data)

def yview( *args):
        lines.yview(*args)
        my_text.yview(*args)




#IDE Implementation
root = Tk("Text Editor")

root.title("T++")
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = Frame(root, bg="#333333")
frame_main.grid(sticky='news')


#Line numbers
lines = Text(frame_main, background='#232323', foreground='#00bfff', pady=5, padx=5, width=5, height=33, insertbackground='#EEEEEE')
lines.grid(row=0, column=0, sticky=(N, W, E, S))
insert_line_numbers()
lines.configure(state='disabled')



#Text widget
my_text = Text(frame_main, background='#121212', foreground='#00bfff', pady=5, padx=5, width=150, height=33, insertbackground='#EEEEEE')
my_text.grid( row=0, column=1, sticky=(N, W, E, S))


text_scroll = ttk.Scrollbar(frame_main, orient=VERTICAL, command=yview)
text_scroll.grid(row=0, column=2, sticky=(NS))
my_text.configure(yscrollcommand=text_scroll.set)
lines.configure(yscrollcommand=text_scroll.set)

frame_exec = Frame(root, bg="#333333")
frame_exec.grid(sticky='news')
execute_text = Text(frame_exec, background='black', foreground='white', pady=0, padx=0,width=158, height=10, insertbackground='gray')
execute_text.grid( row=0, column=0, sticky=(N, W, E, S))

exec_scroll = ttk.Scrollbar(frame_exec, orient=VERTICAL, command=execute_text.yview)
exec_scroll.grid(row=0, column=1, sticky=(NS))
execute_text.configure(yscrollcommand=exec_scroll.set)



my_menu=Menu(root)
root.config(menu=my_menu)

file_menu=Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)

execute_menu=Menu(my_menu,tearoff=False)
my_menu.add_command(label="Execute",command=execute_file)


#Loop
root.mainloop()
