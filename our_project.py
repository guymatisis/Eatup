import tkinter as tk
import ingredients_to_relevant_recipes as i2r
from PIL import ImageTk, Image
import requests
import io
from google.cloud import vision
import cv2
import numpy
import urllib.request
import base64
import tkinter.font as tkf

def stopf():
    global stop
    stop = True

def clear_window() :
    global canvas
    canvas.delete("all")

    
def find_ingredients(img):
    global canvas
    global background_image
 
    # CONVERT IMAGE TO BYTES FOR GOOGLE API
    img = numpy.array(img)
    success, encoded_image = cv2.imencode('.jpeg', img)
    img= encoded_image.tobytes()

    #GOOGLE VISION DETECTS OBJECTS IN PICUTRE
    client = vision.ImageAnnotatorClient()
    image1 = vision.types.Image(content=img)
    objects = client.object_localization(image=image1).localized_object_annotations
    
    #REPAINT CANVAS
    clear_window()
    canvas.image =  background_image
    canvas.create_image(int(width/2), int(height/2), image=background_image)
    canvas.create_text(width/2,height/10,fill="darkgreen",justify=tk.CENTER,font="Times 24 italic bold",
                    text="INGREDIENTS")

    #CONVERT LIST TO SET TO ELIMINATE DUPLICATE INGREDIENTS FOUND
    labels = set()
    for object_ in objects:
        labels.add(object_.name)

    #CREATE LABEL FOR EACH INGREDEINT FOUND
    label_height = 140
    for label in labels:
        out = tk.Label(canvas, text=label)
        canvas.create_window(width/2, label_height, window=out)
        label_height = label_height + 30
    
    #IF INGREDIENTS WERE FOUND THEN DISPLAY BUTTON THAT GETS RECIPES
    if labels:
        button = tk.Button(canvas, text="Get ALL the recipes!;)", bg="green", command =lambda i = labels:third_frame(i))
        canvas.create_window(width/2, label_height, window=button)
    
    #IF NO INGREDIENTS WERE FOUND THEN DISPLAY ERROR MESSAGE
    else:
        canvas.create_text(width/2,(height/10) * 3, width = width -60,fill="darkred",font="Times 30 italic bold",
                    text="No INGREDIENTS RECOGNIZED")

def fourth_frame(recipe):
    clear_window()
    global canvas
    global background_image

    #SETUP BACKGROUND IMAGE
    canvas.image = background_image
    canvas.create_image(int(width/2), int(height/2), image=background_image)

    #CREATE TITLE
    title = canvas.create_text(width/2,height/10, anchor ='n',width = width-50,fill="darkgreen",font="Arial 24 bold",
                        text=recipe[0])

    #CALCULATE SPACING
    x1,y1,x2,y2 = canvas.bbox(title)
    #CREATE DIRECTIONS
    canvas.create_text(width/2,y2 ,anchor = 'n',width = width-50,fill="darkgreen",font="Arial 10 bold",
                        text=recipe[1])

    #CREATE PICTURE OF RECIPE
    response = requests.get(recipe[2])
    image1 = Image.open(io.BytesIO(response.content))
    image1 = image1.resize((width-50,width-50), Image.ANTIALIAS)
    image1 = ImageTk.PhotoImage(image1)
    canvas.image = image1
    canvas.create_image(int(width/2 ), int(height-int(width/2)-10), image=image1)

def third_frame(ingredients):
    clear_window()
    global canvas
    global background_image

    #SETUP BACKGROUND IMAGE
    canvas.image = background_image
    canvas.create_image(int(width/2), int(height/2), image=background_image)

    # TEXT FOR WHILE THE COMPUTATION TAKES PLACE
    canvas.create_text(width/2,height/5,fill="darkblue",font="Times 20 italic bold",
                        text="I am thinking...")
    canvas.update()
    
    #FIND THE APPROPRIATE RECIPES
    recipes = i2r.ingredients_to_recipe(ingredients)

    #REPAINT CANVAS
    clear_window()
    canvas.image = background_image
    canvas.create_image(int(width/2), int(height/2), image=background_image)
    height_adder = 200
    canvas.create_text(width/2,height/5,fill="darkblue",font="Times 20 italic bold",
                    text="RECIPES:")

    #CREATE A BUTTON FOR EACH RECIPE
    for recipe in recipes:
        recipe_name = tk.Button(canvas, text=recipe[0], fg='white', bg='black',command = lambda r=recipe: fourth_frame(r))
        canvas.create_window(width/2, height_adder, window=recipe_name)       
        height_adder = height_adder + 30



def video_stream():
    #URL FOR PHONE CAMER. MUST CHANGE EVERY TIME YOU RECONNECT
    url = 'http://10.0.0.239:8080/shot.jpg'
    imgResp=urllib.request.urlopen(url)

    #CONVERT VIDEO TO APPROPRIATE SIZE AND FORMAT
    imgNp=numpy.array(bytearray(imgResp.read()),dtype=numpy.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgh,imgw,dim = img.shape
    img1 = Image.fromarray(img)
    img1= img1.resize((width-50,int(height *(3/4))), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img1)

    #SET UP VIDEO IN CANVAS
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    #IF CAPTURE BUTTON IS PRESSED STOP WILL BE TRUE AND PROCEED TO FIND INGREDIENTS AND EXIT
    if stop==True:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img =cv2.resize(img,(640,480))
        find_ingredients(img)
        return 

    #LOOPS THE FUNCTION
    video_label.after(5, video_stream )

def second_frame():
    clear_window() 
    global canvas
    global video_label

    #BACKGROUND IMAGE
    global background_image
    canvas.image = background_image
    canvas.create_image(int(width/2), int(height/2), image=background_image)

    #VIDEO
    video_label =  tk.Label(canvas)
    canvas.create_window(width/2-2, int(height * (3/8)+46), window=video_label)

    # CAPTURE BUTTON
    capture_button= tk.Button(canvas, text="Capture", command= lambda:stopf())
    canvas.create_window(width/2, (height/7) *6, window=capture_button)
    
    # STREAM VIDEO  
    video_stream()

# GLOBALS
capture = False
img_capture = None 
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
background_image = Image.open(path)
background_image = background_image.resize((width,height), Image.ANTIALIAS)
background_image= ImageTk.PhotoImage(background_image)
canvas.create_image(int(width/2), int(height/2), image=background_image)

# UNCOMMENT TO TEST FOURTH FRAME
#recipe = ['name of recipe', 'direcions  more directions asdlfjasdld;jasd;lkjjadsf;lkjadsf;lkjadsfl;jkfsdal;kjsadf;ljksadf;lkjasfdf;lkjasdf;ljksdaff',"https://image.shutterstock.com/image-photo/picure-taken-kotka-finland-260nw-1438248707.jpg" ]
#fourth_frame(recipe)

#SETUP BUTTON
img = cv2.imread("/home/guy/Studies/IDHO/GUI/pic1.jpg")
b1 = tk.Button(canvas, text="Start!", command=second_frame)
button1_window = canvas.create_window(width/2, (height/7) *6, window=b1)


#main loop
window.mainloop()
