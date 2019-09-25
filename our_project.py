import tkinter as tk
import ingredients_to_relevant_recipes as i2r
from PIL import ImageTk, Image
import requests
from io import BytesIO
from google.cloud import vision
import cv2
import numpy
import urllib.request
import base64




def stopf():
    global stop
    stop = True

def clear_window() :
    global canvas
    canvas.delete("all")

    
def find_ingredients(img):
    global canvas
    client = vision.ImageAnnotatorClient()
    #img =cv2.Image(img)
    img = numpy.array(img)
    cv2.imwrite("/home/guy/Studies/IDHO/GUI/img.jpg",img)
    with open("/home/guy/Studies/IDHO/GUI/img.jpg", 'rb') as image_file:
        content = image_file.read()
    image1 = vision.types.Image(content=content)
    objects = client.object_localization(image=image1).localized_object_annotations
    clear_window()
    global image
    canvas.image = image
    canvas.create_image(int(width/2), int(height/2), image=image)
    labels = set()
    for object_ in objects:

        labels.add(object_.name)
    label_height = 140
    for label in labels:
        out = tk.Label(canvas, text=label)
        canvas.create_window(width/2, label_height, window=out)
        label_height = label_height + 30
    button = tk.Button(canvas, text="Get ALL the recipes!;)", bg="green", command =lambda i = labels:third_frame(i))
    canvas.create_window(width/2, label_height, window=button)

def fourth_frame(recipe):
    clear_window()
    global canvas
    global image
    canvas.image = image
    canvas.create_image(int(width/2), int(height/2), image=image)

    canvas.create_text(width/2,30, width = width-20,fill="darkblue",font="Arial 25 italic bold",
                        text=recipe[0])
    canvas.create_text(width/2,150,width = width-20,fill="darkblue",font="Arial 10 italic bold",
                        text=recipe[1])

    response = requests.get(recipe[2])
    image = Image.open(BytesIO(response.content))
    image = image.resize((width,width), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(int(width/2), int(520), image=image)

def third_frame(ingredients):
    clear_window()
    global canvas
    global image
    canvas.image = image
    canvas.create_image(int(width/2), int(height/2), image=image)

    canvas.create_text(width/2,height/5,fill="darkblue",font="Times 20 italic bold",
                        text="I am thinking...")
    canvas.update()
    #ingredients = ['cucumber', 'flour','sugar']
    recipes = i2r.ingredients_to_recipe(ingredients)
    clear_window()
    canvas.image = image
    canvas.create_image(int(width/2), int(height/2), image=image)
    #recipes = [['aasdf','bsfdffd        asdsad','csdsdsdf'],['d','e','f'],['g','h','i']]
    height_adder = 200
    canvas.create_text(width/2,height/5,fill="darkblue",font="Times 20 italic bold",
                    text="RECIPES:")

    for recipe in recipes:
        recipe_name = tk.Button(canvas, text=recipe[0], fg='white', bg='black',command = lambda r=recipe: fourth_frame(r))
        canvas.create_window(width/2, height_adder, window=recipe_name)       
        height_adder = height_adder + 30



def video_stream():
    url = 'http://10.100.102.7:8080/shot.jpg'
    imgResp=urllib.request.urlopen(url)
    imgNp=numpy.array(bytearray(imgResp.read()),dtype=numpy.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgh,imgw,dim = img.shape


    '''
    _, frame = cap.read()
    global stop
    global video_label
    global canvas
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    '''
    img1 = Image.fromarray(img)
    img1= img1.resize((width,int(height*(6/7))), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img1)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    if stop==True:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img =cv2.resize(img,(int(imgw/3),int(imgh/3)))
        find_ingredients(img)
        return 
    video_label.after(5, video_stream )

def second_frame():
    clear_window() 
    global canvas
    global video_label
    #background image
    global image
    #canvas.image = image
    #canvas.create_image(int(width/2), int(height/2), image=image)

    #video
    video_label =  tk.Label(canvas)
    canvas.create_window(width/2, (height/7) *2, window=video_label)

    # Capture button
    capture_button= tk.Button(canvas, text="Capture", command= lambda:stopf())
    canvas.create_window(width/2, (height/7) *6, window=capture_button)
    
    # function for video streaming
        
    video_stream()
    
video_label = None
stop = False
# SETUP INITIAL WINDOW AND CANVAS
width = 350
height = 700
dimenstion_string = str(width) + "x" + str(height)
window = tk.Tk()
window.title("FridgeratorAI")
window.geometry(dimenstion_string)
canvas = tk.Canvas(window, width=width, height=height)
canvas.pack()


# SETUP BACKGROUND IMAGE FOR INITIAL FRAME

path = "home_screen.jpg"
image = Image.open(path)
image = image.resize((width,height), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
canvas.create_image(int(width/2), int(height/2), image=image)

#recipe = ['name of recipe', 'direcions \n more directions \....',"https://image.shutterstock.com/image-photo/picure-taken-kotka-finland-260nw-1438248707.jpg" ]
#SETUP BUTTON
img = cv2.imread("/home/guy/Studies/IDHO/GUI/pic1.jpg")
b1 = tk.Button(canvas, text="Start!", command=second_frame)

capture = False
img_capture = None



'''
loadimage = tk.PhotoImage(file="rounded_button.png")
roundedbutton = tk.Button(canvas, image=loadimage,command = second_frame)
roundedbutton["bg"] = "white"
roundedbutton["border"] = "0"
roundedbutton["text"] = "START"
'''


button1_window = canvas.create_window(width/2, (height/7) *6, window=b1)
#main loop
window.mainloop()
