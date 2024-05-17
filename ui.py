import tkinter as tkr
from pynput import keyboard

app = None
overlayWidth = 340
overlayHeight = 85
avatarWidth = 60
avatarHeight = 60

def setupUI(onWindowClose):
    global app
    
    if app != None:
        return app

    app = tkr.Tk()
    app.title('Lore Master')
    app.wm_attributes('-alpha', 0.6, '-topmost', 1)
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

    questionLabel = tkr.Label(app, text='Would you like to learn about ?', fg="white", bg="black", font=(25))
    questionLabel.place(x=80, y=5)
    infoLabel = tkr.Label(app, text='Press ] to confirm', bg="black", fg="gray", font=(20))
    infoLabel.place(x=170, y=30)

    # This is when audio plays
    def onKeyPress(key: keyboard.Key):
        if key == keyboard.Key.alt_gr:
            print("Play audio")
        elif key == keyboard.Key.esc:
            onWindowClose()
            app.destroy()

    listener = keyboard.Listener(on_press=onKeyPress)
    listener.start()

    app.mainloop()

    return app