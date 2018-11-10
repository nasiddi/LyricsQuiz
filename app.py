import azapi
from ctypes import windll
from tkinter import *
import re
from song_lib import SongLib


class App:
    def __init__(self, master):
        self.lib = SongLib()
        self.boxes = []
        self.master = master
        self.entry_text = StringVar()
        self.score = StringVar()
        self.answers = []
        self.found_counter = 0
        self.song_length = 0
        self.frame = Frame(self.master, highlightthickness=0)
        self.frame.grid()
        master.grid_columnconfigure(0, weight=1)

        self.entry_field = Entry(self.frame, textvariable=self.entry_text, font=('Korolev Light', 15))
        self.entry_field.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="news")
        self.label = Label(self.frame, textvariable=self.score, font=('Korolev Light', 15), bg='white')
        self.label.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky=N+S+W+E)
        self.show = Button(self.frame, text="Show all", command=self.show_all, font=('Korolev Light', 12),
                           relief='flat', bg='white', justify=CENTER, bd=0)
        self.show.grid(row=1, column=3, columnspan=1, padx=10, pady=10, sticky=N+S+W+E)
        self.new_song = Button(self.frame, text="new Song", command=self.new_song, font=('Korolev Light', 12),
                               relief='flat', bg='white', justify=CENTER, bd=0)
        self.new_song.grid(row=1, column=4, columnspan=1, padx=10, pady=10, sticky="news")


    def new_song(self):
        n = 0
        while n < 6:
            lyric = self.lib.get_random_song()
            n = len(lyric)
        k = 6

        lyric = azapi.lyrics('bruce springsteen', 'thunderroad')
        length = int(n / k) + 1

        try:
            lower_frame.destroy()
        except UnboundLocalError:
            pass

        lower_frame = Frame(self.master, highlightthickness=0)
        lower_frame.grid_rowconfigure(0, weight=1)
        lower_frame.grid_columnconfigure(0, weight=1)
        lower_frame.grid(row=2, column=0, sticky=NW)
        #lower_frame.grid_propagate(False)
        canvas = Canvas(lower_frame)

        canvas_frame = Frame(canvas)
        canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

        max_len = len(max(lyric, key=len))

        for i in range(k):
            box = self.get_listbox(max_len, canvas_frame)
            self.add_box_to_grid(box, i)
            self.boxes.append(box)

        canvas.grid(row=0, column=0, sticky="news")
        vsb = Scrollbar(lower_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')

        bbox = canvas.bbox(ALL)
        canvas_width = bbox[2] - bbox[1]
        canvas_height = bbox[3] - bbox[1]
        canvas.config(scrollregion=bbox)
        disp_width = canvas_width
        disp_height = int((canvas_width/length) * 50)


        canvas_frame = Frame(canvas)
        self.boxes = []

        canvas.configure(yscrollcommand=vsb.set, width=disp_width, height=disp_height)
        canvas_frame.update_idletasks()





        self.fill_in_lyrics(lyric)

    def fill_in_lyrics(self, lyric):
        n = len(lyric)
        k = 6
        length = int(n/k)+1
        columns = []
        print(n)
        for i in range(k):
            columns.append(lyric[i*length:(i+1)*length])

        maximum = len(max(columns, key=len))
        for lyr, b in zip(columns, self.boxes):
            while len(lyr) < maximum:
                lyr.append('')
            for l in lyr:
                b.insert(END, l)
                if not l == '':
                    b.itemconfig(END, {'fg': 'darkred', 'bg': 'darkred'})
            b.configure(justify='center')
            self.update_score()

    def show_all(self):
        for b in self.boxes:
            for i, listbox_entry in enumerate(b.get(0, END)):
                if listbox_entry not in self.answers:
                    b.itemconfig(i, {'bg': 'white'})



    def update_score(self):
        self.score.set(str(self.found_counter) + ' / ' + str(self.song_length))

    def get_listbox(self, max_len, canvas_frame):
        listbox = Listbox(canvas_frame, height=0, width=max_len, font=('Korolev Light', 12),
                          relief='flat', highlightthickness=0)
        listbox.bindtags((listbox, self.master, "all"))
        return listbox

    def add_box_to_grid(self, box, position):
        box.grid(row=2, column=position, columnspan=1, padx=10, pady=10)

    def load_song(self, artist, song):
        return azapi.lyrics(artist, song)

    def apply_input(self):
        answer = self.entry_field.get()
        if answer in self.answers:
            return
        found = False
        for b in self.boxes:
            for i, listbox_entry in enumerate(b.get(0, END)):
                result = re.sub(r'[^A-Za-z0-9]', '', listbox_entry).lower()
                if answer == result:
                    b.itemconfig(i, {'fg': 'black', 'bg': 'white'})
                    self.found_counter += 1
                    if not found:
                        self.answers.append(answer)
                    found = True

        if found:
            self.entry_field.delete(0, END)
        self.update_score()


windll.shcore.SetProcessDpiAwareness(1)
root = Tk()
root.configure(background='white')
app = App(root)


def callback(*_):
    app.apply_input()


var = app.entry_text
var.trace("w", callback)

def press_enter(_):
    app.apply_input()


def shift_enter(_):
    app.entry_field.delete(0, END)


app.entry_field.bind('<Return>', press_enter)
app.entry_field.bind('<Shift-Return>', shift_enter)

root.mainloop()