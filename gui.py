import Tkinter as tk
from PIL import ImageTk, Image



def callback (event) :
	global frame
	window = frame
	_list = window.winfo_children()

	for item in _list :
	    if item.winfo_children() :
	        _list.extend(item.winfo_children())

	for item in _list:
		item.pack_forget()

#This creates the main window of an application
width = 300
height = 300
window = tk.Tk()
frame = tk.Frame(window)
frame.pack()
window.title("Join")
string = str(width) + "x" +str(height)
window.geometry(string)
window.configure(background='grey')

path = "pic.jpg"

#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
image = Image.open(path)
image = image.resize((width,height), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)

canvas = tk.Canvas(frame, width=width, height=height)
canvas.bind("<Button-1>", callback)
canvas.pack()
canvas.create_image(int(width/2), int(height/2), image=image)


print(frame.winfo_children())

#Start the GUI
window.mainloop()








