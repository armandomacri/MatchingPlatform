import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from mongo_connection import MongoConnection
from transcriber import Transcriber
#from audio_retrieval import AudioRetriever
from topic_extractor import TopicExtractor
from tkinter import scrolledtext

# ********** Initializations **********
database = MongoConnection()
database.initialize()
transcriber = Transcriber()
retriever = []
# *************************************


# *********** root frame configuration ****************
root = tk.Tk()

win_width = 700
win_height = 500
bg_color = '#FFFFFF'
bg_button = '#ff6e6c'
fg_button = '#1f1235'
fg_text = '#1f1235'
button_font = font =("Calibri", 13)
# ******************************************************

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))

root.geometry('{}x{}+{}+{}'.format(win_width, win_height,start_x, start_y))
root.configure(background=bg_color)
root.title('Matching Platform')

# ****************************** APP frame ******************************
usernameframe = tk.Frame(root, pady=20, padx=20, bg='#50e3c2')
usernameframe.pack(side=tk.TOP, fill=tk.X)

# frame hidden, used for listening to
mainframe = tk.Frame(root, bg=bg_color)
searchframe = tk.LabelFrame(mainframe,
                            text="I'm waiting for you",
                            bg=bg_color,
                            fg=fg_text)

informationframe = tk.LabelFrame(mainframe,
                            text="Welcome",
                            bg=bg_color,
                            fg=fg_text)
searchframe.pack(side=tk.RIGHT, padx=30, anchor=tk.N)
informationframe.pack(side=tk.LEFT, padx=30, anchor=tk.N)

topicframe1 = tk.Frame(informationframe, bg=bg_color)
topicframe2 = tk.Frame(informationframe, bg=bg_color)

resultframe= tk.Frame(root, bg=bg_color)

resultscore = tk.StringVar()
tk.Label(resultframe,
             textvariable=resultscore,
             bg=bg_color,
             fg='#50e3c2',
             font=("Calibri", 18)).pack(side=tk.RIGHT, padx=5, pady=5)

matchframe = tk.LabelFrame(root, text='Best matches', fg=fg_text, bg=bg_color)
# ***********************************************************************

logo = ImageTk.PhotoImage(Image.open('./img/interests.png').resize((200, 200), Image.ANTIALIAS))
tk.Label(root,
        image=logo,
        bg='white',
        ).pack(anchor=tk.CENTER, pady=100)

# ********************* Insert Username *********************
containerusername = tk.Frame(usernameframe, bg='#50e3c2')
containerusername.pack(side=tk.TOP)

#Username label
tk.Label(containerusername,
                    text="Insert your username:",
                    bg='#50e3c2',
                    fg='#2a3544',
                    font=button_font).pack(side=tk.LEFT)

#Username Text field
usernameText = tk.Entry(containerusername, font=font)
usernameText.pack(side=tk.LEFT, padx=20)
#***************************************************************

# *****************************************************************************
img1 = ImageTk.PhotoImage(Image.open('./img/microphone.png').resize((40, 40), Image.ANTIALIAS))
img2 = ImageTk.PhotoImage(Image.open('./img/upload.png').resize((40, 40), Image.ANTIALIAS))

containerbutton = tk.Frame(searchframe, bg=bg_color)
containerbutton.pack(side=tk.TOP,pady=9)

tk.Button(containerbutton,
              image=img1,
              fg=fg_button,
              bg=bg_button,
              command=lambda:listen(),
              activebackground='#fffffe',
              font=button_font
              ).pack(side=tk.LEFT, padx=15, pady=10)

tk.Button(containerbutton,
                    bg=bg_button,
                    fg=fg_button,
                    image=img2,
                    command=lambda:open_file(),
                    activebackground='#fffffe',
                    font=button_font
            ).pack(side=tk.RIGHT, padx=15, pady=10)

checkVav = tk.IntVar()
check = tk.Checkbutton(searchframe,
                       text='Translate',
                       variable=checkVav,
                       onvalue=1,
                       offvalue=0,
                       activebackground=bg_color,
                       bg=bg_color,
                       font=font).pack(side=tk.TOP)
# *****************************************************************************

sporttext = tk.StringVar()
businesstext = tk.StringVar()
worldtext= tk.StringVar()
sciencetext = tk.StringVar()



textw = scrolledtext.ScrolledText(resultframe, width=50, height=7, wrap=tk.WORD)

def show_result(text, topic, score):
    textw.delete("1.0", tk.END)

    textw.config(background=bg_color, foreground=fg_text,
                 font='times 12 bold', wrap='word')
    textw.insert(tk.END, text)
    textw.pack(side=tk.LEFT)

    resultscore.set('Topic:\n'+topic+': '+str(round(score, 4)))

    if topic == 'sport':
        sporttext.set('Sport: '+str(round(user.sport[0],4)))
    elif topic == 'business':
        businesstext.set('Business: ' + str(round(user.sport[0], 4)))
    elif topic == 'world':
        worldtext.set('World: ' + str(round(user.sport[0], 4)))
    elif topic == 'science':
        sciencetext.set('Sci/Tech: ' + str(round(user.sport[0], 4)))

    resultframe.pack(side='top',fill=tk.X, anchor=tk.N, pady=10, padx=30)

def suggest_users(users):

    # The variable photo is a local variable which gets garbage collected after the class is instantiated.
    global i
    for widget in matchframe.winfo_children():
        widget.destroy()
    i = ImageTk.PhotoImage(Image.open('./img/user.png').resize((20, 20), Image.ANTIALIAS))
    for u in users:
        tk.Label(matchframe,
                 image=i,
                 text=u.username,
                 compound='left',
                 bg=bg_color,
                 fg=fg_button
                 ).pack(side=tk.LEFT, padx=10, pady=15)

    matchframe.pack(anchor=tk.S, padx=25, pady=10)

def open_file():
    file_path = filedialog.askopenfilename(title='Open your file audio', initialdir='/', filetypes=[('audio files', '*.wav')])
    if file_path is not None:
        pass

    extract_topic(file_path)


def listen():
    '''
    retriever = AudioRetriever()
    audio = retriever.retrieve()
    extract_topic()
    # sentence = transcriber.transcriptWav("file.wav")
    extract_topic()
    '''


def extract_topic(file_path="file.wav"):

    sentence = []
    if checkVav.get() == 1:
        sentence = transcriber.transcriptWav(file_path, True)
    else:
        sentence = transcriber.transcriptWav(file_path)

    extractor = TopicExtractor()
    topic, tipicscore = extractor.get_topic(sentence)
    username, newscore = user.updateScore(topic, tipicscore)
    database.update_topic_score(username, topic, newscore)
    show_result(sentence, topic, tipicscore)
    suggest_users(database.get_similar_score_users(username, topic, newscore))



def search_speaker_phane():
    mainframe.pack(side=tk.TOP, fill=tk.X, pady=15)


def makeOnline():
    global user, sport, business, science, world
    if usernameText.get() == "":
        print("Errore")
    else:
        user = database.get_user(usernameText.get())
        if user is None:
            print('user doesn\'t exists')
        else:
            # *************** remove logo ********************
            i = 0
            for widget in root.winfo_children():
                if i != 0:
                    widget.pack_forget()
                i += 1
            # *************************************************
            enter["state"] = "disabled"
            userimg = ImageTk.PhotoImage(Image.open('./img/user.png').resize((15, 15), Image.ANTIALIAS))
            tk.Label(informationframe,
                    text=user.fname+' '+user.lname,
                    image=userimg,
                     compound='left',
                    bg = bg_color,
                    fg = fg_text,
                    font = button_font).pack(side='top', padx=5, pady=5)

            tk.Label(topicframe1,
                     textvariable=sporttext,
                     bg=bg_color,
                     fg=fg_text,
                     font=button_font).pack(side=tk.LEFT, padx=5, pady=5)
            sporttext.set('Sport: '+str(round(user.sport[0],4)))
            tk.Label(topicframe1,
                                textvariable=businesstext,
                     bg=bg_color,
                     fg=fg_text,
                     font=button_font).pack(side=tk.LEFT, padx=5, pady=5)
            businesstext.set('Business: ' +str(round(user.business[0],4)))
            tk.Label(topicframe2,
                             textvariable=worldtext,
                     bg=bg_color,
                     fg=fg_text,
                     font=button_font).pack(side=tk.LEFT, padx=5, pady=5)
            worldtext.set('World: ' + str(round(user.world[0], 4)))
            tk.Label(topicframe2,
                               textvariable=sciencetext,
                     bg=bg_color,
                     fg=fg_text,
                     font=button_font).pack(side=tk.LEFT, padx=5, pady=5)
            sciencetext.set('Sci/tech: ' + str(round(user.science[0], 4)))
            topicframe1.pack(side='bottom')
            topicframe2.pack(side='bottom')

            search_speaker_phane()


# Enter button
enter = tk.Button(containerusername,
                  text='ENTER',
                  command=makeOnline,
                  fg='#344457',
                  bg="#8c88ff",
                  font=button_font,
                  cursor="hand1")
enter.pack(side=tk.LEFT)

root.mainloop()