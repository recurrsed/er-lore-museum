import tkinter as tkr
from pynput import keyboard

app = None
overlayWidth = 340
overlayHeight = 85
avatarWidth = 60
avatarHeight = 60
mainLabelTxt = None
isAppVisible = False

def setPromptText(location: str):
    global mainLabelTxt

    if mainLabelTxt == None:
        return

    mainLabelTxt.set(f"Learn about {location}.")
    showApp()

def showApp():
    global isAppVisible

    app.wm_attributes('-alpha', 0.7, '-topmost', 1)
    isAppVisible = True

def hideApp():
    global isAppVisible

    app.wm_attributes('-alpha', 0, '-topmost', 0)
    mainLabelTxt.set("")
    isAppVisible = False

def setupUI(onWindowClose, setWatchScreenPauseState):
    global app, mainLabelTxt
    
    if app != None:
        return app

    app = tkr.Tk()
    app.title('Lore Master')
    app.wm_attributes('-alpha', 0, '-topmost', 0)
    app.overrideredirect(True)

    # Size + position
    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()    
    windowXPosition = ws - overlayWidth - 20
    windowYPosition = hs - overlayHeight - 100

    app.configure(background='black', padx=10, pady=10)
    app.geometry('%dx%d+%d+%d' % (overlayWidth, overlayHeight, windowXPosition, windowYPosition))

    # Avatar
    canvas = tkr.Canvas(app, bg="black", width=avatarWidth, height=avatarHeight, highlightthickness=0)
    canvas.pack()
    background = tkr.PhotoImage(file="./melina-avatar-2.png")
    canvas.create_image(30, 30, image=background)
    canvas.place(x=10, y=5)

    mainLabelTxt = tkr.StringVar()
    mainLabel = tkr.Label(app, textvariable=mainLabelTxt, fg="white", bg="black", font=(25))
    mainLabel.place(x=80, y=5)
    infoLabel = tkr.Label(app, text='Press alt-r to play audio', bg="black", fg="gray", font=("Arial", 10))
    infoLabel.place(x=80, y=30)

    # This is when audio plays
    def onKeyPress(key: keyboard.Key):
        if key == keyboard.Key.alt_gr and isAppVisible == True:
            mainLabelTxt.set("Playing...")
            # This goes after audio is done
            setWatchScreenPauseState(False)
            # hideApp()
        if key == keyboard.Key.ctrl_r:
            hideApp()
            setWatchScreenPauseState(False)
        elif key == keyboard.Key.esc:
            onWindowClose()
            app.destroy()

    listener = keyboard.Listener(on_press=onKeyPress)
    listener.start()

    app.mainloop()

    return app