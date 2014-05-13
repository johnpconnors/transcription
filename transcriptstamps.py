# http://my-python3-code.blogspot.com/2012/08/basic-tkinter-text-editor-online-example.html

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
            file = Tkinter.filedialog.asksaveasfile(mode='w')
            textoutput = self.text.get(0.0, END) # Gets all the text in the field
            file.write(textoutput.rstrip()) # With blank perameters, this cuts off all whitespace after a line.
            file.write("\n") # Then we add a newline character.

    def doOpen(self):
            # Returns the opened file
            file = tkFileDialog.askopenfile(mode='r')
            fileContents = file.read() # Get all the text from file.

            # Set current text to file contents
            self.text.delete(0.0, END)
            self.text.insert(0.0, fileContents) 

    def openAudio(self):
        fname = tkFileDialog.askopenfile(mode='r')
        self.fpath = os.path.abspath(fname.name)

    def playAudio(self):    
        self.p=vlc.MediaPlayer(self.fpath)
        self.p.play()
        self.rate=1
    
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
        print(t)
    
    def statuscheck(self):
        status=vlc.libvlc_media_player_get_state(self.p)
        self.status=str(status)

    def looping(self):
        self.statuscheck()
        if self.status in ['State.Playing']:
            self.timestamps()
        threading.Timer(self.stamprate, self.looping).start()

    def __init__(self):
            # Set up the screen, the title, and the size.
            self.root = Tk()
            self.root.title("Basic Notepad")
            self.root.minsize(width=500,height=400)

                    
            # Set up basic Menu
            menubar = Menu(self.root)
    
            # Set up a separate menu that is a child of the main menu
            filemenu = Menu(menubar,tearoff=0)
            filemenu.add_command(label="New File", command=self.doNew, accelerator="Ctrl+N")
    
            # Try out openDialog
            filemenu.add_command(label="Open", command=self.doOpen, accelerator="Ctrl+O")
    
            # Try out the saveAsDialog
            filemenu.add_command(label="Save", command=self.doSaveAs, accelerator="Ctrl+Shift+S")
            menubar.add_cascade(label="File", menu=filemenu)
            self.root.config(menu=menubar)
    
            #Set up the AudioMenu
            AudioMenu = Menu(menubar,tearoff=0)
            AudioMenu.add_command(label="Select Audio File", command=self.openAudio)
            AudioMenu.add_command(label="Play", command=self.playAudio)
            AudioMenu.add_command(label="Stop", command=self.stopAudio)
            AudioMenu.add_command(label="Pause", command=lambda:self.pauseAudio(None), accelerator="Ctrl+P")
            AudioMenu.add_command(label="Speed +", command=lambda:self.speedUpAudio(None), accelerator="Crtl +/=")
            AudioMenu.add_command(label="Speed -", command=lambda:self.slowDownAudio(None), accelerator="Ctrl -")
            AudioMenu.add_command(label="Go Forward", command=lambda:self.forwardAudio(None), accelerator="Ctrl ->")
            AudioMenu.add_command(label="Go Backward", command=lambda:self.backwardAudio(None), accelerator="Ctrl <-")
            menubar.add_cascade(label="Audio", menu=AudioMenu)

            #Set up Transcription Menu
            TranscriptMenu = Menu(menubar, tearoff=0)
            TranscriptMenu.add_command(label='Auto Add Timestamps', command=self.timeStampSet)
            TranscriptMenu.add_command(label='Insert Timestamp', command=lambda:self.timestamps(None), accelerator="Ctrl+T")
            TranscriptMenu.add_command(label='Insert Audio Metadata')
            menubar.add_cascade(label="Transcription Tools", menu=TranscriptMenu)

            # Set up the text widget
            self.text = Text(self.root)
            self.text.bind('<Control-t>', self.timestamps)
            self.text.bind('<Control-p>', self.pauseAudio)
            self.text.bind('<Control-equal>', self.speedUpAudio)
            self.text.bind('<Control-minus>', self.slowDownAudio)
            self.text.bind('<Control-Right>', self.forwardAudio)
            self.text.bind('<Control-Left>', self.backwardAudio)
            self.text.pack(expand=YES, fill=BOTH) # Expand to fit vertically and horizontally


app = App()
app.root.mainloop()
