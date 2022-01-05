import tkinter as tk
from PIL import Image, ImageTk
from mongo_connection import MongoConnection

database = MongoConnection()
database.initialize()

root = tk.Tk()

win_width = 700
win_height = 400
bg_color = 'SteelBlue4'
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))

root.geometry('{}x{}+{}+{}'.format(win_width, win_height,start_x, start_y))
root.configure(background=bg_color)
root.title('Matching Platform')


usernameframe = tk.LabelFrame(root, text="Insert your information!", padx=10, pady=10, fg='white' ,bg=bg_color)
usernameframe.pack(side=tk.TOP)


# frame hidden, used for listening to
searchframe = tk.LabelFrame(root, text="I'm listening to you", padx=10, pady=10, bg=bg_color, fg='white')

closebutton = tk.Frame(root, padx=10, bg=bg_color)
closebutton.pack(side=tk.BOTTOM)


#Username label
username = tk.Label(usernameframe, text="Insert your username:", bg=bg_color, fg='white')
username.pack(side=tk.LEFT)

#Username Text field
usernameText = tk.Entry(usernameframe, width=40)
usernameText.pack(side=tk.LEFT)

def search_speaker_phane():

    welcome = tk.Label(searchframe, text="WELCOME", bg=bg_color)
    welcome.pack(side=tk.TOP)
    img = ImageTk.PhotoImage(Image.open('./img/sound-waves.png').resize((70, 70), Image.ANTIALIAS))
    img_widget = tk.Label(searchframe, image=img, text='Say something...', bg=bg_color, fg='white')
    img_widget.image = img
    #imglabel.place(x=20, y=20)
    img_widget.pack(side=tk.TOP, fill="both", expand="yes")
    searchframe.pack()
    pass

def makeOnline():
    if usernameText.get() == "":
        print("Errore")
    else:
        user = database.get_user(usernameText.get())
        if user is None:
            print('user doesnt exists')

        else:
            usernameText["state"] = "disabled"
            print(user['fname']) # select a field
    search_speaker_phane()

# Enter button
enter = tk.Button(usernameframe, text='ENTER', width=20, command=makeOnline, fg='green', cursor="hand1")
enter.pack(side=tk.LEFT)


# Disconnect button
button = tk.Button(closebutton, text='Disconnect', width=25, command=root.destroy)
button.pack(side=tk.BOTTOM)

''' img in a button
# Position text in frame
Label(root, text = 'Position image on button', font =('<font_name>', <font_size>)).pack(side = TOP, padx = <x_coordinate#>, pady = <y_coordinate#>)

# Create a photoimage object of the image in the path
photo = PhotoImage(file = "</path/image_name>")

# Resize image to fit on button
photoimage = photo.subsample(1, 2)

# Position image on button
Button(root, image = photoimage,).pack(side = BOTTOM, pady = <y_coordinate#>)
'''
root.mainloop()