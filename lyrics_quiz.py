from tkinter import *
from ctypes import windll
from song_lib import SongLib, load_url


MAX_WIDTH = 1300
MAX_HEIGHT = 1400


class MyApp(Tk):
    def __init__(self, title='lyrics quiz', *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.lib = SongLib()
        self.title(title)
        self.configure(background="white")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.entry_text = StringVar()
        self.boxes = []
        self.score = StringVar()
        self.answers = []
        self.found_counter = 0
        self.song_length = 0
        self.canvas = None
        self.song = ''
        self.artist_var = StringVar(value='artist')
        self.title_var = StringVar(value='title')
        self.url_var = StringVar(value='azlyrics url')

        master_frame = Frame(self, bg="white", bd=3, relief=FLAT)
        master_frame.grid(sticky=NSEW)
        master_frame.columnconfigure(0, weight=1)

        frame1 = Frame(master_frame, bg="white", bd=0, relief=FLAT)
        frame1.grid(row=1, column=0, sticky='news')

        self.artist_field = Entry(frame1, textvariable=self.artist_var, font=('Korolev Light', 18), name='artist')
        self.artist_field.grid(row=0, column=4, columnspan=6, padx=10, pady=10, sticky='news')
        self.title_field = Entry(frame1, textvariable=self.title_var, font=('Korolev Light', 18))
        self.title_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='news')

        self.url_field = Entry(frame1, textvariable=self.url_var, font=('Korolev Light', 18))
        self.url_field.grid(row=1, column=0, columnspan=10, padx=10, pady=10, sticky='news')

        self.entry_field = Entry(frame1, textvariable=self.entry_text, font=('Korolev Light', 18))
        self.entry_field.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="news")
        sore_label = Label(frame1, textvariable=self.score, font=('Korolev Light', 18), bg='white')
        sore_label.grid(row=2, column=2, columnspan=1, padx=10, pady=10, sticky="news")
        show = Button(frame1, text="show all", command=self.show_all, font=('Korolev Light', 15),
                      relief='flat', bg='white', justify=CENTER, bd=0)
        show.grid(row=2, column=3, columnspan=1, padx=10, pady=10, sticky="news")
        show_title_button = Button(frame1, text="show title", command=self.show_title, font=('Korolev Light', 15),
                                   relief='flat', bg='white', justify=CENTER, bd=0)
        show_title_button.grid(row=2, column=4, columnspan=1, padx=10, pady=10, sticky="news")
        new_song_button = Button(frame1, text="new Song", command=self.new_song, font=('Korolev Light', 15),
                                 relief='flat', bg='white', justify=CENTER, bd=0)
        new_song_button.grid(row=2, column=5, columnspan=1, padx=10, pady=10, sticky="news")
        delete_button = Button(frame1, text='delete', command=lambda: self.lib.delete_song(self.song),
                               font=('Korolev Light', 15), relief='flat', bg='white', justify=CENTER, bd=0)
        delete_button.grid(row=2, column=6, columnspan=1, padx=10, pady=10, sticky="news")

        self.frame2 = Frame(master_frame, relief=FLAT, bd=0, bg='white')
        self.frame2.grid(row=3, column=0, sticky='news')

        self.new_song()

    def new_song(self, artist='', title='', url=''):
        if not artist or not title:
            self.artist_var.set('artist')
            self.title_var.set('title')

        if not url:
            self.url_var.set('azlyrics url')



        if self.canvas:
            self.canvas.destroy()
            self.boxes = []
            self.answers = []
            self.found_counter = 0
        n = 0

        if artist and title and title != 'title':
            self.song = self.lib.get_song(artist, title)
            lyric = self.song.lyric
            n = len(lyric)
            if n < 6:
                self.artist_var.set('failed')
                self.title_var.set('failed')
                return
        if artist:
            self.song = self.lib.get_random_song(artist=artist)
            lyric = self.song.lyric
            n = len(lyric)
            if n < 6:
                self.artist_var.set('failed')
                self.title_var.set('failed')
                return
        elif url:
            self.song = load_url(url)
            lyric = self.song.lyric
            n = len(lyric)
            if n < 6:
                self.url_var.set('failed')
                return

            self.artist_var.set(self.song.artist)
            self.title_var.set(self.song.title)

        elif not (artist or title or url):
            while n < 6:
                self.song = self.lib.get_random_song()
                lyric = self.song.lyric
                n = len(lyric)



        k = 7
        print(self.song.artist, self.song.title)

        self.canvas = Canvas(self.frame2, bg="white", bd=0)
        self.canvas.grid(row=0, column=0)

        solution_frame = Frame(self.canvas, bg="white", bd=0)

        max_len = len(max(lyric, key=len))
        max_len = max(max_len, 10)

        for i in range(k):
            box = self.get_listbox(max_len, solution_frame)
            self.add_box_to_grid(box, i)
            self.boxes.append(box)

        self.fill_in_lyrics(lyric)

        self.canvas.create_window((0,0), window=solution_frame, anchor=NW)

        solution_frame.update_idletasks()
        bbox = self.canvas.bbox(ALL)

        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]

        if w > MAX_WIDTH:
            dw = MAX_WIDTH
        else:
            dw = w

        if h > MAX_HEIGHT:
            dh = MAX_HEIGHT
        else:
            dh = h

        if h != dh:
            vsbar = Scrollbar(self.frame2, orient=VERTICAL, command=self.canvas.yview)
            vsbar.grid(row=0, column=1, sticky=NS)
            self.canvas.configure(yscrollcommand=vsbar.set)
            self.canvas.bind_all("<MouseWheel>", self.scroll_vertically)

        if w != dw:
            hsbar = Scrollbar(self.frame2, orient=HORIZONTAL, command=self.canvas.xview)
            hsbar.grid(row=1, column=0, sticky=EW)
            self.canvas.configure(xscrollcommand=hsbar.set)
            self.canvas.bind_all('<Shift-MouseWheel>', self.scroll_horizontally)

        self.canvas.configure(scrollregion=bbox, width=dw, height=dh)

    def get_listbox(self, max_len, frame):
        listbox = Listbox(frame, height=0, width=max_len, font=('Korolev Light', 15),
                          relief='flat', highlightthickness=0)
        listbox.bindtags((listbox, self.master, "all"))
        return listbox

    def add_box_to_grid(self, box, position):
        pad = 0
        if position % 2 == 0:
            pad = 10

        box.grid(row=2, column=position, columnspan=1, padx=pad, pady=0, sticky='news')

    def fill_in_lyrics(self, lyric):
        n = len(lyric)
        k = 7
        length = int(n / k) + 1
        self.song_length = len(lyric)

        columns = []
        for i in range(k):
            columns.append(lyric[i * length:(i + 1) * length])

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

    def update_score(self):
        self.score.set(str(self.found_counter) + ' / ' + str(self.song_length))

    def show_all(self):
        self.show_title()
        for b in self.boxes:
            for i, listbox_entry in enumerate(b.get(0, END)):
                if listbox_entry not in self.answers:
                    b.itemconfig(i, {'fg': 'black'})

    def show_title(self):
        self.title_var.set(self.song.title)
        self.artist_var.set(self.song.artist)

    def scroll_horizontally(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_vertically(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def callback(*_):
    app.apply_input()


def press_enter(_):
    app.entry_field.delete(0, END)
    parent = app.entry_field.master
    print(parent.winfo_width(), parent.winfo_height())


def artist_focus(_):
    if app.artist_var.get() == 'artist':
        app.artist_field.delete(0, END)


def title_focus(_):
    if app.title_var.get() == 'title':
        app.title_field.delete(0, END)


def url_focus(_):
    if app.url_var.get() == 'azlyrics url':
        app.url_field.delete(0, END)


def load_song(_):
    app.new_song(artist=app.artist_var.get(), title=app.title_var.get())


def load_from_url(_):
    app.new_song(url=app.url_var.get())


if __name__ == "__main__":
    app = MyApp("lyrics quiz")
    windll.shcore.SetProcessDpiAwareness(1)
    var = app.entry_text
    var.trace("w", callback)
    app.entry_field.bind('<Return>', press_enter)
    app.artist_field.bind('<Return>', load_song)
    app.title_field.bind('<Return>', load_song)
    app.url_field.bind('<Return>', load_from_url)
    app.artist_field.bind('<1>', artist_focus)
    app.title_field.bind('<1>', title_focus)
    app.url_field.bind('<1>', url_focus)
    app.mainloop()
