from tkinter import *
from tkinter import messagebox
import subprocess as sub
import shlex

def backup():
	path = "E:\\Huyen Trang\\project\\djangows\\client\\windows\\backcli.py"
	command = "python \"" + path + "\" -t " + file_name.get() + " -s " + server_name.get()
	process = sub.call(shlex.split(command))
	if(process == 0):
		list1.insert(END, "Backup done!\n")
	else:
		list1.insert(END, "Have something error. Let's start again.")


window = Tk()

window.title("Backup by Ginkgo")

# def on_closing():
#     if messagebox.askokcancel("Quit", "Do you want to quit?"):
#         window.destroy()

# window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

l1=Label(window, text="Backup File")
l1.grid(row = 0, column = 0, columnspan=2)

l2=Label(window, text="Files")
l2.grid(row = 1, column = 1)

l3=Label(window, text="Server")
l3.grid(row = 2, column = 1)

l4=Label(window, text="G:\\\\test.txt")
l4.grid(row = 1, column = 3, padx=5)

l5=Label(window, text="192.168.20.51")
l5.grid(row = 2, column = 3, padx=5)

l6=Label(window, text="Output")
l6.grid(row = 3, column = 1)


file_name=StringVar()
e1=Entry(window, textvariable=file_name)
e1.grid(row=1, column=2, padx=2, pady=2)

server_name=StringVar()
e1=Entry(window, textvariable=server_name)
e1.grid(row=2, column=2, padx=2, pady=2)

#define Listbox
list1=Listbox(window, height=6, width=35)
list1.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

# Atach Scrollbar to the list
sb1=Scrollbar(window)
sb1.grid(row=3,column=4, padx=5)

#Apply to the list
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)


b1=Button(window, text="Backup", width=12, command=backup)
b1.grid(row=4, column=2, padx=2, pady=2)

#window.geometry("350x200+500+200")
window.mainloop()