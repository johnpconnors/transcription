# This basic GUI text editor is intended to aid researchers that must transcribe or take notes from audio files.
# The audio tools utilize the VLC bindings for Python. 
# The code is maintained and branchable here: https://github.com/johnpconnors/transcription
# The initial design of the text editor was inspired by and borrowed form this code: http://my-python3-code.blogspot.com/2012/08/basic-tkinter-text-editor-online-example.html

import tkFileDialog
from Tkinter import *
import vlc
import os
import datetime
import threading

class App:

    def doNew(self):
        # Clear the text
        self.text.delete(0.0, END)

    def doSaveAs(self):
        # Returns the saved file
        file = tkFileDialog.asksaveasfile(mode='w')
        self.savefile = file
        textoutput = self.text.get(0.0, END) # Gets all the text in the field
        file.write(textoutput.rstrip()) # With blank perameters, this cuts off all whitespace after a line.
        file.write("\n") # Then we add a newline character.

    def doSave(self):
        try:
            textoutput = self.text.get(0.0, END) # Gets all the text in the field
            self.savefile.write(textoutput.rstrip()) # With blank perameters, this cuts off all whitespace after a line.
            self.savefile.write("\n") # Then we add a newline character.
        except:
            self.doSaveAs()

    def doOpen(self):
        # Returns the opened file
        file = tkFileDialog.askopenfile(mode='r')
        self.savefile = file
        fileContents = file.read() # Get all the text from file.
        # Set current text to file contents
        self.text.delete(0.0, END)
        self.text.insert(0.0, fileContents) 

    def openAudio(self, event):
        fname = tkFileDialog.askopenfile(mode='r')
        self.fpath = os.path.abspath(fname.name)
        self.nameVar.set(self.fpath)

    def playAudio(self, event):    
        self.p=vlc.MediaPlayer(self.fpath)
        self.p.play()
        self.rate=1
        self.displayTime()
    
    def stopAudio(self):
        self.p.stop()

    def pauseAudio(self, event):
        self.p.pause()

    def slowDownAudio(self, event):
        self.rate=self.rate*0.75
        vlc.libvlc_media_player_set_rate(self.p, self.rate)

    def speedUpAudio(self, event):
        self.rate=self.rate*1.25
        vlc.libvlc_media_player_set_rate(self.p, self.rate)

    def timeStampSet(self):
        self.stamprate=10
        self.looping()

    def forwardAudio(self,event):
        current=vlc.libvlc_media_player_get_time(self.p)
        vlc.libvlc_media_player_set_time(self.p, current+30000)

    def backwardAudio(self,event):
        current=vlc.libvlc_media_player_get_time(self.p)
        vlc.libvlc_media_player_set_time(self.p, current-30000)

    def timestamps(self, event):
        tmillisec=vlc.libvlc_media_player_get_time(self.p)
        sec=tmillisec/1000
        tsec= datetime.timedelta(seconds=sec)
        t=str(tsec)
        stamp=' ('+t+') '
        self.text.insert(END, stamp)

    def timecheck(self):
        tmillisec=vlc.libvlc_media_player_get_time(self.p)
        sec=tmillisec/1000
        tsec= datetime.timedelta(seconds=sec)
        t=str(tsec)
        self.stamp=' ('+t+') '
    
    def statuscheck(self):
        status=vlc.libvlc_media_player_get_state(self.p)
        self.status=str(status)

    def looping(self):
        self.statuscheck()
        if self.status in ['State.Playing']:
            self.timestamps()
        threading.Timer(self.stamprate, self.looping).start()

    def displayTime(self):
        self.statuscheck()
        if self.status in ['State.Playing']:
            self.timecheck()
            self.clock.config(text=self.stamp)
        self.clock.after(200, self.displayTime)
    #Functions for th custom text inserts
    def customButton1(self, event):
        c1text=self.CE0.get()
        self.text.insert(END, c1text)
    def customButton2(self, event):
        c2text=self.CE1.get()
        self.text.insert(END, c2text)
    def customButton3(self, event):
        c3text=self.CE2.get()
        self.text.insert(END, c3text)
    def customButton4(self, event):
        c4text=self.CE3.get()
        self.text.insert(END, c4text)

    def __init__(self):
            # Set up the screen, the title, and the size.
            self.root = Tk()
            self.root.title("Transcription Tools")
            self.root.minsize(width=500,height=800)

            # Set up File Information
            self.fileFrame = Frame(self.root)
            self.fileFrame.grid(row=0, column=1, sticky=S)
            self.fileFrame.pack()
            Label(self.fileFrame, text="Audio File:").grid(row=0, column=0, sticky=W)
            self.nameVar = StringVar()
            self.name = Entry(self.fileFrame, textvariable=self.nameVar)
            self.name.grid(row=0, column=1, sticky=W)
            BOpen = Button(self.fileFrame, text="Open Audio...", command=lambda:self.openAudio(None))
            BOpen.grid(row=0, column=2, sticky=W)
            #Set up a clock to show the time of the audio file
            self.clock = Label(self.fileFrame)
            self.clock.grid(row=0, column=3, sticky=W)


            # Set up Buttons Frame
            self.bFrame = Frame(self.root)
            self.bFrame.grid(row=0, column=1, sticky=S)
            self.bFrame.pack()

            # Set up the audio buttons
            B0 = Button(self.bFrame, text="Play", command=lambda:self.playAudio(None))
            B1 = Button(self.bFrame, text="Pause", command=lambda:self.pauseAudio(None))
            B2 = Button(self.bFrame, text="Forward", command=lambda:self.forwardAudio(None))
            B3 = Button(self.bFrame, text="Backward", command=lambda:self.backwardAudio(None))
            B4 = Button(self.bFrame, text="Speed Up", command=lambda:self.speedUpAudio(None))
            B5 = Button(self.bFrame, text="Slow Down", command=lambda:self.slowDownAudio(None))
            B6 = Button(self.bFrame, text="Time Stamp", command=lambda:self.timestamps(None))
            B0.pack(side=LEFT);B1.pack(side=LEFT); B2.pack(side=LEFT); B3.pack(side=LEFT); B4.pack(side=LEFT); B5.pack(side=LEFT); B6.pack(side=LEFT);

            # Set Up Custom Insert Shortcuts Frame
            self.customFrame = Frame(self.root)
            self.customFrame.grid(row=1, column=1)
            self.customFrame.pack()

            CB0 = Button(self.customFrame, text="Ctrl+1", command=lambda:self.customButton1(None))
            inserttext0 = StringVar()
            self.CE0 = Entry(self.customFrame, textvariable=inserttext0, width=10)
            CB1 = Button(self.customFrame, text="Ctrl+2", command=lambda:self.customButton2(None))
            inserttext1 = StringVar()
            self.CE1 = Entry(self.customFrame, textvariable=inserttext1, width=10)
            CB2 = Button(self.customFrame, text="Ctrl+3", command=lambda:self.customButton3(None))
            inserttext2 = StringVar()
            self.CE2 = Entry(self.customFrame, textvariable=inserttext2, width=10)
            CB3 = Button(self.customFrame, text="Ctrl+4", command=lambda:self.customButton4(None))
            inserttext3 = StringVar()
            self.CE3 = Entry(self.customFrame, textvariable=inserttext3, width=10)
            CB0.pack(side=LEFT);self.CE0.pack(side=LEFT);CB1.pack(side=LEFT);self.CE1.pack(side=LEFT);CB2.pack(side=LEFT);self.CE2.pack(side=LEFT);CB3.pack(side=LEFT);self.CE3.pack(side=LEFT)

            # Set up Text Tool Frame
            self.textFrame = Frame(self.root)
            self.textFrame.pack(expand=YES, fill=BOTH)

            # Set up the text widget
            self.text = Text(self.textFrame)
            self.text.bind('<Control-t>', self.timestamps)
            self.text.bind('<Control-p>', self.pauseAudio)
            self.text.bind('<Control-equal>', self.speedUpAudio)
            self.text.bind('<Control-minus>', self.slowDownAudio)
            self.text.bind('<Control-Right>', self.forwardAudio)
            self.text.bind('<Control-Left>', self.backwardAudio)
            self.text.bind('<Control-Key-1>', self.customButton1)
            self.text.bind('<Control-Key-2>', self.customButton2)
            self.text.bind('<Control-Key-3>', self.customButton3)
            self.text.bind('<Control-Key-4>', self.customButton4)
            scroll = Scrollbar(self.textFrame, orient=VERTICAL)
            scroll.config (command=self.text.yview)
            scroll.pack(side=RIGHT, fill=Y)
            self.text.config(yscrollcommand=scroll.set)
            self.text.pack(expand=YES, fill=BOTH) # Expand to fit vertically and horizontally

            # Set up basic Menu
            menubar = Menu(self.root)
    
            # Set up a separate menu that is a child of the main menu
            filemenu = Menu(menubar,tearoff=0)
            filemenu.add_command(label="New File", command=self.doNew, accelerator="Ctrl+N")
    
            # Try out openDialog
            filemenu.add_command(label="Open", command=self.doOpen, accelerator="Ctrl+O")
    
            # Try out the saveAsDialog
            filemenu.add_command(label="Save", command=self.doSave, accelerator="Ctrl+S")
            filemenu.add_command(label="Save As", command=self.doSaveAs, accelerator="Ctrl+Shift+S")
            menubar.add_cascade(label="Text", menu=filemenu)
            self.root.config(menu=menubar)
    
            #Set up the AudioMenu
            AudioMenu = Menu(menubar,tearoff=0)
            AudioMenu.add_command(label="Select Audio File", command=lambda:self.openAudio(None))
            AudioMenu.add_command(label="Play", command=lambda:self.playAudio(None))
            AudioMenu.add_command(label="Stop", command=self.stopAudio)
            AudioMenu.add_command(label="Pause", command=lambda:self.pauseAudio(None), accelerator="Ctrl+P")
            AudioMenu.add_command(label="Speed +", command=lambda:self.speedUpAudio(None), accelerator="Ctrl+=")
            AudioMenu.add_command(label="Speed -", command=lambda:self.slowDownAudio(None), accelerator="Ctrl+-")
            AudioMenu.add_command(label="Go Forward", command=lambda:self.forwardAudio(None), accelerator="Ctrl+Right")
            AudioMenu.add_command(label="Go Backward", command=lambda:self.backwardAudio(None), accelerator="Ctrl+Left")
            menubar.add_cascade(label="Audio", menu=AudioMenu)

            #Set up Transcription Menu
            TranscriptMenu = Menu(menubar, tearoff=0)
            TranscriptMenu.add_command(label='Auto Add Timestamps', command=self.timeStampSet)
            TranscriptMenu.add_command(label='Insert Timestamp', command=lambda:self.timestamps(None), accelerator="Ctrl+T")
            TranscriptMenu.add_command(label='Insert Audio Metadata')
            menubar.add_cascade(label="Transcription Tools", menu=TranscriptMenu)



app = App()
app.root.mainloop()
