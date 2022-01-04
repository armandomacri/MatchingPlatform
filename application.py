import tkinter as tk

root = tk.Tk()
root.geometry("800x400")
root.title('Matching Platform')

usernameframe = tk.LabelFrame(root, text="Insert your information!", padx=10, pady=10)
usernameframe.pack()
closebutton = tk.Frame(root, padx=10)
closebutton.pack(side=tk.BOTTOM)

#Username label
username = tk.Label(usernameframe, text="Insert your username:").grid(row=0)

#Username Text field
usernameText = tk.Entry(usernameframe, width=40)
usernameText.grid(row=0, column=1, padx=10)

def makeOnline():
    if usernameText.get() == "":
        print("Errore")
    else:
        print(usernameText.get())
    pass

# Enter button
enter = tk.Button(usernameframe, text='ENTER', width=20, command=makeOnline, fg='green', cursor="hand1").grid(row=0, column=2)


# Disconnect button
button = tk.Button(closebutton, text='Disconnect', width=25, command=root.destroy)
button.pack(side=tk.BOTTOM)


root.mainloop()