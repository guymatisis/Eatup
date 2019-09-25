from Tkinter import *
from PIL import ImageTk, Image
import cv2

# function for video streaming
def func(image):

	#image = image.resize((100,100), Image.ANTIALIAS)
	lmain1 = Label(app)
	lmain1.grid()
	image = ImageTk.PhotoImage(image)
	lmain1.imgtk = image
	lmain1.configure(image=image)

def video_stream():
    _, frame = cap.read()
    global stop
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    img= img.resize((100,100), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if stop==True:
    	func(img)
    	return 
    lmain.after(1, video_stream) 


def stopf():
	global stop
	stop = True

stop = False
root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()
b= Button(app, command=lambda: stopf())
b.grid()

# Capture from camera
cap = cv2.VideoCapture("whole_field.mp4")



image = video_stream()

root.mainloop()
