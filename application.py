import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from mongo_connection import MongoConnection
import time
from transcriber import Transcriber
#from audio_retrieval import AudioRetriever
from topic_extractor import TopicExtractor
from tkinter import scrolledtext

# ********** Initializations **********
database = MongoConnection()
database.initialize()
transcriber = Transcriber()
#retriever = AudioRetriever()
# *************************************

root = tk.Tk()

win_width = 700
win_height = 400
bg_color = '#FFFFFF'
bg_button = '#ff6e6c'
fg_button = '#1f1235'
fg_text = '#1f1235'
button_font = font=("Arial", 15)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))

root.geometry('{}x{}+{}+{}'.format(win_width, win_height,start_x, start_y))
root.configure(background=bg_color)
root.title('Matching Platform')

# ****************************** APP frame ******************************
usernameframe = tk.LabelFrame(root, text="Insert your information!", padx=10, pady=10, fg=fg_text ,bg=bg_color)
usernameframe.pack(side=tk.TOP, pady=10)

# frame hidden, used for listening to
searchframe = tk.LabelFrame(root,
                            text="I'm listening to you",
                            bg=bg_color,
                            fg=fg_text)

# ***********************************************************************

# *****************************************************************************
img1 = ImageTk.PhotoImage(Image.open('./img/sound-waves.png').resize((60, 30), Image.ANTIALIAS))
img2 = ImageTk.PhotoImage(Image.open('./img/upload.png').resize((30, 30), Image.ANTIALIAS))

tk.Button(searchframe,
              text='Start listening to',
              image=img1,
              compound='left',
              fg=fg_button,
              bg=bg_button,
              command=lambda:listen(),
              activebackground='#fffffe',
              font=button_font
              ).pack(side=tk.TOP,padx=15, pady=15, fill="both", expand='yes')

tk.Button(searchframe,
                    text='Choose File',
                    bg=bg_button,
                    fg=fg_button,
                    compound='left',
                    image=img2,
                    command=lambda:open_file(),
                    activebackground='#fffffe',
                    font=button_font
            ).pack(side='top', padx=15, pady=15, expand='yes', fill='both')

# *****************************************************************************


closebutton = tk.Frame(root, padx=10, bg=bg_color)
closebutton.pack(side=tk.BOTTOM, pady=10)


#Username label
username = tk.Label(usernameframe,
                    text="Insert your username:",
                    bg=bg_color,
                    fg=fg_text,
                    font=button_font)
username.pack(side=tk.LEFT)

#Username Text field
usernameText = tk.Entry(usernameframe, width=30)
usernameText.pack(side=tk.LEFT, padx=10)

textw = scrolledtext.ScrolledText(root, width=70, height=30)

def open_file():
    file_path = filedialog.askopenfilename(title='Open your file audio', initialdir='/', filetypes=[('audio files', '*.wav')])
    if file_path is not None:
        pass
    sentence=transcriber.transcriptWav(file_path)
    extractor = TopicExtractor()
    topic, score = extractor.get_topic(sentence)
    username, newscore = user.updateScore(topic, score)
    database.update_topic_score(username, topic, newscore)
    matches = database.get_similar_score_users(username, topic, newscore)
    textw.delete("1.0", tk.END)
    textw.pack()
    textw.config(background=bg_color, foreground=fg_text,
                 font='times 12 bold', wrap='word')
    textw.insert(tk.END, sentence + topic + matches[0].username)

def listen():
    #audio = retriever.retrieve()
    sentence = transcriber.transcriptWav("file.wav")
    extractor = TopicExtractor()
    topic, score = extractor.get_topic(sentence)
    username, newscore = user.updateScore(topic, score)
    database.update_topic_score(username, topic, newscore)
    matches = database.get_similar_score_users(username, topic, newscore)
    textw.delete("1.0", tk.END)
    textw.pack()
    # textw.grid(column=1, row=2, sticky=tk.N + tk.S + tk.E + tk.W)
    textw.config(background=bg_color, foreground=fg_text,
                 font='times 12 bold', wrap='word')
    textw.insert(tk.END, sentence + topic + matches[0].username)



def uploadFile():
    pb1 = tk.Progressbar(
                        usernameframe,
                        orient=tk.HORIZONTAL,
                        length=300,
                        mode='determinate'
                        )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        usernameframe.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    tk.Label(usernameframe, text='File Uploaded Successfully!', fg= fg_text).grid(row=4, columnspan=3, pady=10)

def search_speaker_phane():
    searchframe.pack(side='top', padx=10, pady=10)
    pass

def makeOnline():
    global user
    if usernameText.get() == "":
        print("Errore")
    else:
        user = database.get_user(usernameText.get())
        if user is None:
            print('user doesnt exists')
        else:
            usernameText["state"] = "disabled"
    search_speaker_phane()

# Enter button
enter = tk.Button(usernameframe,
                  text='ENTER',
                  width=20,
                  command=makeOnline,
                  fg=fg_button,
                  bg=bg_button,
                  font=button_font,
                  cursor="hand1")
enter.pack(side=tk.LEFT)


# Disconnect button
button = tk.Button(closebutton, text='Disconnect', width=25, command=root.destroy, bg='#67568c')
button.pack(side=tk.BOTTOM)


root.mainloop()