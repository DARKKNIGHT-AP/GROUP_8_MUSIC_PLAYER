
# IMPORTING THE REQUIRED MODULES

# ========================================================================

from tkinter import *
from tkinter import filedialog as fldg
import tkinter.messagebox as tmsg
import pygame
from PIL import Image,ImageTk
from tkinter.ttk import Progressbar as progbr
from tkinter.ttk import Style
from tkinter.ttk import Scale
from mutagen.mp3 import MP3
import time

# ========================================================================


#      INITIALIZED THE PYGAME MODULE's MIXER

# ========================================================================

pygame.mixer.init()

# ===========================================================

#      GLOBAL VARIABLE FOR PAUSING AND UNPAUSING

# ========================================================================

global paused
paused=False

# ==================================================================

#            GLOBAL VARIABLE FOR PLAYING 

# ========================================================================

global played
played=False

# ====================================================================

#       GLOBAL VARIABLE FOR SONG DURATION ,PROGRESS BAR

# ========================================================================

# total_duration for fetching the total duration of the song being played
# cur_duration for fetching the current duration of the song being played
# max_duration for displaying the total_duration in the label
# progress is our progress bar

global total_duration,cur_duration,max_duration,progress


# ===============================================================================================

#              COMMANDS FOR MENU OPTIONS AND PLAY ,PAUSE,FORWARD,BACKWARDS,STOP BUTTONS

# =================================================================================================

#                       ADDDING A SINGLE SONG TO THE QUEUE

# =============================================================================================

def add_song():
    # our global variable(s)
    global played
    # song variable has the path of the song alongwith its name
    song=fldg.askopenfilename(initialdir="c:/",filetypes=(("Mp3 files","*.mp3"),("wav files","*.wav"),("OGG files","*.ogg"),))
    # condtions when user haven't made a selection or song has been selected
    if len(song)==0:
        tmsg.showwarning("No selection made","You haven't made a selection\nKindly choose a song")
    else:
        tmsg.showinfo("Song Added",f"Successfully added\n {song}\nto the Queue")
        songs_list.insert(END,song)
        # when successful selection has been made played variable's value is set to true
        played=True

# ========================================================================================

#                     ADDING MULTIPLE SONGS TO THE QUEUE

# =========================================================================================

def add_songs():
    # our global variable(s)
    global played
    # songs variable has the path of the songs as a tuple alongwith their names
    songs=fldg.askopenfilenames(initialdir="c:/",title="Please select a Song",filetypes=(("mp3 files","*.mp3"),("wav files","*.wav"),("OGG files","*.ogg"),))
    # condtions when user haven't made a selection or songs has been selected
    if len(songs)==0:
        tmsg.showwarning("No selection made","You haven't made a selection\nKindly choose some songs")
    else:
        tmsg.showinfo("file details",f"Successfully added  Songs to the Queue")
        for x in songs:
            songs_list.insert(END,x)
        # when successful selection has been made played variable's value is set to true
        played=True

# ===========================================================================================

#                   FOR THE DURATION OF THE SONG BEING PLAYED

# ============================================================================================

def play_duration():
    # our global variable(s)
    global total_duration,cur_duration,max_duration,progress
    # song variable gets which song is selected or being played
    song=songs_list.get(ACTIVE)

    # FOR TOTAL SONG DURATION AND FOR THE PROGRESS BAR
    audio=MP3(song)

    # GET THE TOTAL TIME LENGTH OF THE SONG TO BE PLAYED
    # Converted the total time length into integer format

    total_duration=int(audio.info.length)

    # CONVERSION OF TIME INTO MINUTES AND SECONDS FORMAT
    total_time=time.strftime('%M:%S',time.gmtime(total_duration))

    progress['maximum']=total_duration
    # CONVRETING THE MAXIMUM DURATION TO SECONDS AND DISPLAYING IN THE LABEL
    max_duration.configure(text=total_time)

    def progressbarmusic():
        # globa variable for handling the duration times
        global cur_duration
        # get the current time of the song and converted it into a more simplified value
        current=pygame.mixer.music.get_pos()/1000
        # updating the progress bar along the progression of song
        progress['value']=current
        # get the current duration in converted time format
        current_time=time.strftime('%M:%S',time.gmtime(current))
        # configuring the label to store the value of the current duration
        cur_duration.configure(text=current_time)
        # calling the function after 2 milliseconds to give our progress bar a dynamic look
        # Making it progress as the song is progressing
        progress.after(2,progressbarmusic)
    # Call to the function made for durations of the song
    progressbarmusic()


# ======================================================================================

#                      TO PLAY THE SELECTED SONG

# =========================================================================================

def play_song():
    # our global variable(s)
    global played

    # Stop any music that is playing 
    pygame.mixer.music.stop()
    # configuring the label for our current duration to be displayed clearly
    cur_duration.configure(bg="black",fg="skyblue")
    
    # main condition to check is any music is being played or not
    if played:
        # get the selected song from the listbox
        song=songs_list.get(ACTIVE)
        tmsg.showinfo("Now Playing",f"Playing \n{song}")
        # loading the song into pygame mixer
        pygame.mixer.music.load(song)
        # playing the selected song
        pygame.mixer.music.play()
        # Calling the play duration function for displaying the minutes seconds of the song
        play_duration()

    else:
        tmsg.showerror("Playlist Empty","Your playlist is Empty\nPlease add some song(s)\nvia The Songs Menu option")
    
# ========================================================================================

#                             TO PAUSE/UNPAUSE THE SONG BEING PLAYED

# =========================================================================================

def pause_song(is_paused):
    # our global variable(s)
    global paused,played
    paused=is_paused

    # main condition to check is any music is being played or not
    if played:
        if paused:
            # Unpause the song that is currently paused
            pygame.mixer.music.unpause()
            # Setting the pause var's value to false indicating that song is now, not paused
            paused=False
        else:
            # pause the song that is currently unpaused or playing
            pygame.mixer.music.pause()
            # Setting the pause var's value to true indicating that song is now, paused
            paused=True
    else:
        tmsg.showerror("Playlist Empty","Your playlist is Empty\nPlease add some song(s)\nvia The Songs Menu option")



# =======================================================================================


#                TO STOP THE SONG BEING PLAYED AND MAKE THE FIRST SONG ACTIVE

# =========================================================================================

def stop_song():
    # our global variable(s)
    global played,cur_song,max_duration,cur_duration,progress

    # main condition to check is any music is being played or not
    if played:
        # get the curent song selected from the listbox
        cur_song=songs_list.curselection()
        # Stop any music palying
        pygame.mixer.music.stop()
        # Clearing the listbox 
        songs_list.select_clear(0,END)
        # Setting the selection of listbox to the first element 
        songs_list.selection_set(0,last=None)
        # activating the highlight bar background for the first element
        songs_list.activate(0)

        # RESET THE DURATION TIME AND THE PROGRESS BAR
        max_duration.configure(text="--:--")
        cur_duration.configure(bg="black",fg="black")
        # Set the value  of progress bar to 0 as its Stop button
        progress['value']=0

    else:
        tmsg.showerror("Empty Playlist","No song is being played\nPlease add some songs to the Queue")

# =====================================================================================

#                                  TO PLAY THE PREVIOUS SONG

# =========================================================================================

def previous():
    # The global variables
    global played,cur_duration,max_duration

    # configuring the label for our current duration to be displayed clearly
    cur_duration.configure(bg="black",fg="skyblue")
    # stop any song which is  currently playing
    pygame.mixer.music.stop()
    

    # main condition to check is any music is being played or not
    if played:

        # Get the index of current song being played in form of a Tuple
        prev_one=songs_list.curselection()

        # if length of 'prev_song' tuple is zero it indicates that end has been reached 
        if len(prev_one)==0:
            tmsg.showerror("End Reached","You have reached the end of playlist\nAdd some more songs or\nselect from existing list of songs to carry on")
            # Clearing the selection from the listbox--'songs_list'
            songs_list.selection_clear(0,END)
            # Configuring the labels dispalying the durations
            max_duration.configure(text="--:--")
            cur_duration.configure(bg="black",fg="black")

        else:
        # Setting the index of the next song to be played,by incrementing it by one
            prev_one=prev_one[0]-1

            # when the user reaches the first song in the 'songs_list' listbox 
            if prev_one <0:
                # Stop any music playing
                pygame.mixer.music.stop()
                tmsg.showerror("End Reached","You have reached the end of playlist\nAdd some more songs or\nselect from existing list of songs to carry on")
                # The selection is cleared as beginning has been reached
                # Clearing the selection from the listbox--'songs_list'
                songs_list.selection_clear(0,END)
                # Configuring the labels dispalying the durations
                max_duration.configure(text="--:--")
                cur_duration.configure(bg="black",fg="black")
        

            else:
                # Fetch the next song in the playlist
                song=songs_list.get(prev_one)

                # Load and play the song 
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()

                # Clear the highlighted bar in listbox
                songs_list.selection_clear(0,END)

                # Activation of highlighted bar for the next song in queue 
                songs_list.activate(prev_one)

                # Moved the selection,i.e,the underline from previous song to the next song
                songs_list.selection_set(prev_one,last=None)

                # Calling the play_duration() function to update the song durations being displayed, according to the current song
                play_duration()
    else:
        tmsg.showerror("Empty Playlist","No song is being played\nPlease add some songs to the Queue")
    
# =========================================================================================

#                              TO PLAY THE NEXT SONG

# =========================================================================================

def next():
    # The global variables
    global played,cur_duration,max_duration

    # Configuring the label for displaying the duration more clearly
    cur_duration.configure(bg="black",fg="skyblue")

    # STOP ANY SONG WHICH IS PLAYING
    pygame.mixer.music.stop()

    # main condition to check is any music is being played or not
    if played:

        # Get the index of current song being played in form of a Tuple
        next_one=songs_list.curselection()

        # if length of 'next_one' tuple is zero it indicates that end has been reached 
        if len(next_one)==0:
            tmsg.showerror("End Reached","You have reached the end of playlist\nAdd some more songs or\nselect from existing list of songs to carry on")
            
            # Clearing the selection from the listbox--'songs_list'
            songs_list.selection_clear(0,END)

            # Configuring the labels dispalying the durations
            max_duration.configure(text="--:--")
            cur_duration.configure(bg="black",fg="black")

        else:
        # Setting the index of the next song to be played,by incrementing it by one
            next_one=next_one[0]+1

            # The value of 'next_one' should not exceed the max no. of songs in the playlist
            if next_one >= songs_list.size():

                # stop any music playing
                pygame.mixer.music.stop()
                tmsg.showerror("End Reached","You have reached the end of playlist\nAdd some more songs or\nselect from existing list of songs to carry on")

                # The selection is cleared as end has been reached
                songs_list.selection_clear(0,END)

                # Configuring the labels dispalying the durations
                max_duration.configure(text="--:--")
                cur_duration.configure(bg="black",fg="black")
        

            else:
                # Fetch the next song in the playlist
                song =songs_list.get(next_one)

                # Load and play the song 
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()

                # Clear the highlighted bar in listbox
                songs_list.selection_clear(0,END)

                # Activation of highlighted bar for the next song in queue 
                songs_list.activate(next_one)

                # Moved the selection ,i.e the underline,from previous song to the next song
                songs_list.selection_set(next_one,last=None)

                # Calling the play_duration() function to update the song durations being displayed, according to the current song
                play_duration()

    else:
        tmsg.showerror("Empty Playlist","No song is being played\nPlease add some songs to the Queue")


# ======================================================================================

#                            TO REMOVE THE SELECTED SONG

# ==============================================================================================


def remove_song():
    # The global variables
    global played,cur_duration,max_duration

    # TO GET THE INDEX OF CUURENT SONG BEING PLAYED IN FORM OF A TUPLE
    current_song=songs_list.curselection()

    # condition when playlist is complete cleared
    if len(current_song)==0:
        # Setting value of played variable to false 
        played=False
        tmsg.showinfo("Playlist Cleared","The playlist has been emptied")
        # Configuring the duration lables
        max_duration.configure(text="--:--")
        cur_duration.configure(bg="black",fg="black")

    else:
        # FETCH THE INDEX FROM THE TUPLE OF current_song
        next_song=current_song[0]-1

        # IF THE PLAYLIST HAS ONLY ONE SONG IN IT
        if next_song==-1:
            # STOP ANY MUSIC PLAYING
            pygame.mixer.music.stop()

            # DELETING THE SELECTED SONG
            songs_list.delete(ACTIVE)

            played=False
            tmsg.showinfo("Playlist Cleared","The playlist has been emptied")
            max_duration.configure(text="--:--")
            cur_duration.configure(bg="black",fg="black")

        # FOR PLAYLIST HAVING MORE THAN ONE SONG
        else:

            # STOP ANY MUSIC PLAYING
            pygame.mixer.music.stop()

            cur_duration.configure(bg="black",fg="black")
            # DELETING THE SELECTED SONG
            songs_list.delete(ACTIVE)

            # Clear the highlighted bar in listbox
            songs_list.selection_clear(0,END)

            # Activation of highlighted bar for the next song in queue 
            songs_list.activate(next_song)

            # Moved the selection from previous song to the next song
            songs_list.selection_set(next_song,last=None)    

            # Calling the duration function
            play_duration()

# ===================================================================================

#                     TO REMOVE ALL SONGS i.e., TO CLEAR THE PLAYLIST

# =========================================================================================

def remove_songs():
    # STOP ANY MUSIC PLAYING
    pygame.mixer.music.stop()
    # Global variables
    global played,cur_duration,max_duration
    # Deleting the whole songs
    songs_list.delete(0,END)
    tmsg.showinfo("Playlist Cleared","The playlist has been emptied")
    # Setting value of played variable to false 
    played=False
    # Configuring the duration lables
    max_duration.configure(text="--:--")
    cur_duration.configure(bg="black",fg="black")

# ===============================================================================

#                          VOLUME FUNCTION

# ===============================================================================

def volume(x):
    # variable for storing the current volume level
    global volume_value
    # Fetch the value from the slider and convert it into integer format
    volume_value=int(volmune_slider.get()*100)
    # Setting the value of the song played according to the value from volume slider
    pygame.mixer.music.set_volume(volmune_slider.get())
    # Configure the value of volume displayed in the volume_frame
    volume_frame.configure(text=f"Volume : {volume_value}")    


# ===============================================================================

#                   THE MAIN WINDOW DESIGN ANS ITS ELEMENTS

# =================================================================================


root=Tk()
root.title("   ME-LODY")
root.geometry("950x650+250+20")

# TITLE IMAGE
titleicon = ImageTk.PhotoImage(Image.open("GUI/ME-LODY.jpg"))

# IMAGE IN THE ROOT WINDOW
melody_icon = ImageTk.PhotoImage(Image.open("GUI/melody2.jpg"))

# Icon for the music player
root.iconphoto(False,titleicon)

root.configure(bg="black")
root.resizable(FALSE,FALSE)


# ============================================

#              BUTTON ICON IMAGES

# ============================================

play=PhotoImage(file='GUI/play black.png')
pause=PhotoImage(file='GUI/pause black.png')
stop = ImageTk.PhotoImage(Image.open("GUI/stop1.jpg"))
# ============================================================
forward = ImageTk.PhotoImage(Image.open("GUI/forward black1.png"))
backward = ImageTk.PhotoImage(Image.open("GUI/backward.jpg"))

# ========================================================================================

# ========================================================================================

#                         MENU FOR ADDING SONGS

# =========================================================================================

# Main menu to hold further submenu options
main_menu=Menu(root)

# Menu for the addition of songs
songs_add=Menu(main_menu)
# Tweaking the menu's appearance
songs_add.configure(tearoff=0,font="ubuntu 16",bg="black",fg="turquoise",activebackground="black",activeforeground="gold")

# Adding the separators
songs_add.add_separator()

songs_add.add_command(label="Add a Song",command=add_song)

# Adding the separators
songs_add.add_separator()
songs_add.add_separator()

songs_add.add_command(label="Add Multiple Songs",command=add_songs)

# Adding the separators
songs_add.add_separator()

# Adding the cascade option to show further menu options
main_menu.add_cascade(label="Songs..",menu=songs_add)
# Setting the menu for the root window
root.configure(menu=main_menu)



# ======================================================================================

#                      MENU FOR DELETING SONGS FROM THE QUEUE

# =========================================================================================

# Menu for the deletion of songs
deletion=Menu(main_menu)

# Tweaking the menu's appearance
deletion.configure(tearoff=0,font="ubuntu 16",bg="black",fg="turquoise",activebackground="black",activeforeground="gold")

# Adding the separators
deletion.add_separator()

# Adding the command to Removing the selected song
deletion.add_command(label="Remove the Selected Song",command=remove_song)

# Adding the separators
deletion.add_separator()
deletion.add_separator()

# Adding the command to Empty the playlist
deletion.add_command(label="Remove All Songs",command=remove_songs)

# Adding the separators
deletion.add_separator()

# Main label to store remove song(s) options in the menu
# Adding the cascade option to show further menu options
main_menu.add_cascade(label="Manage Playlist",menu=deletion)




# ==================================================================================

#                    Scrollbar for songs_list named listbox

# =========================================================================================

scrlbr=Scrollbar(root)
scrlbr.pack(side=RIGHT,fill="y") 

# ======================================================================================

#                           List box for songs QUEUE

# =========================================================================================

songs_list=Listbox(root,width=50,bg="mediumturquoise",fg="black",font="ubuntu 16",yscrollcommand=scrlbr.set)
songs_list.configure(selectbackground="lavenderblush",selectforeground="midnightblue",height=7)
songs_list.pack(pady=20,fill="x")



# =========================================================================================

#                    CONFIGURING THE SCROLLBAR FOR THE LISTBOX

# =========================================================================================

scrlbr.config(command=songs_list.yview,width=20,bd=5,relief=RAISED,bg="black",activebackground="black")


# ======================================================================

#              PROGRESS BAR FOR THE SONG BEING PLAYED

# ======================================================================

# Main label for storing the current, maximum duration and the progress bar
duration = Label(root,bg="black",font="ubuntu 20 bold")
duration.pack(pady=15,fill=BOTH)

# Label for displaying the Current duration of the song
cur_duration = Label(duration,width=4,text="--:--",bg="black",fg="skyblue",font="ubuntu 20 bold")
cur_duration.grid(row=0,column=0)

# Label for displaying the Maximum duration of the song
max_duration = Label(duration,width=4,text="--:--",bg="black",fg="skyblue",font="ubuntu 20 bold")
max_duration.grid(row=0,column=2)

# --------------=======================================---------------------------------------

#               CHANGING THE STYLE AND CREATING THE PROGRESS BAR

# =========================================================================================

# Configuring the style for Progress bar
progress_style=Style()
progress_style.theme_use('winnative')
progress_style.configure("TProgressbar",troughcolor="black",background="skyblue")

# Creating the progress bar
progress = progbr(duration,style="TProgressbar",orient=HORIZONTAL,mode='determinate',value=0,length=750)

progress.grid(row=0,column=1,padx=11)



# ==================================================================================

#           FRAME FOR THE BUTTONS :: PLAY,PAUSE,FORWARD,BACKWARD,STOP

# =========================================================================================

f1=Frame(root)
f1.configure(bg="black")
f1.pack(fill="y")

# =========================================================================================

#                           VOLUME CONTROL SLIDER 

# =========================================================================================

# Configuring the style for Volume Scale
volume_style=Style()
volume_style.theme_use('winnative')
volume_style.configure("TScale",troughcolor="skyblue",background="black")

# Creating a label frame for containing the volume slider
volume_frame=LabelFrame(f1,text=f"Volume : 100",bd=0,bg="black",font="ubuntu 20",fg="skyblue")
volume_frame.grid(row=0,column=5,padx=1)

# Creating the volume slider
volmune_slider=Scale(volume_frame,style="TScale",from_=0,to=1,value=1,orient=HORIZONTAL,length=150,command=volume)
volmune_slider.pack(side=RIGHT)

# ====================================================================================


# ============================================================================

#              BUTTONS:: PLAY,PAUSE,STOP,NEXT,PREVIOUS

# ===============================================================================

backward_button=Button(f1,padx=10,border=0,image=backward,highlightthickness=0,command=previous)
backward_button.grid(row=0,column=0,padx=11)

forward_button=Button(f1,padx=10,border=0,image=forward,highlightthickness=0,command=next)
forward_button.grid(row=0,column=1,padx=6)

play_button=Button(f1,padx=10,border=0,image=play,highlightthickness=0,command=play_song)
play_button.grid(row=0,column=2,padx=3)

pause_button=Button(f1,padx=10,bd=0,image=pause,highlightthickness=0,command=lambda:pause_song(paused))
pause_button.grid(row=0,column=3,padx=2)

stop_button=Button(f1,padx=10,border=0,image=stop,highlightthickness=0,command=stop_song)
stop_button.grid(row=0,column=4,padx=2)




# =======================================================================================

#                            DISPLAYING THE ME-LODY ICON
 
# =======================================================================================

melody_image=Label(root,image=melody_icon,bg="black")
melody_image.pack(fill=BOTH,pady=20)


# =======================================================================================
root.mainloop()