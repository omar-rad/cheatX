from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, filedialog
import tensorflow_hub as hub
import numpy as np
import contextlib as cl
import os
import pdfplumber as pdf
from threading import Thread

window = Tk()
window.title("CheatX")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.geometry("900x600")
window.resizable(False, False)

homePage = Frame(window)
mainPage = Frame(window)

for frame in (homePage, mainPage):
    frame.grid(row=0, column=0, sticky="nsew")


def show_frame(frame):
    frame.tkraise()


show_frame(homePage)

# ************ home page code

logo = ImageTk.PhotoImage(Image.open("logo.png"))
logoo = ImageTk.PhotoImage(Image.open("logoo.png"))
back = ImageTk.PhotoImage(Image.open("back-button.png"))

logo_lable = Label(homePage, image=logo)
logo_lable_2 = Label(mainPage, image=logoo)
logo_lable.place(x=900 / 2 - 200, y=600 / 2 - 250)
logo_lable_2.place(x=265, y=3)
back_label = Label(mainPage, image=back)
back_label.place(x=16, y=16)
back_label.bind('<Button-1>', lambda _: show_frame(homePage))


selectFilesButton = ttk.Button(homePage, text="Select Folder", command=lambda: open_file())
selectFilesButton.place(width=200, height=40, x=900 - 210, y=600 - 100)

path = None


def open_file():
    global path
    path = filedialog.askdirectory(title="Choose Folder")
    if path != "":
        checkPlagiarism.state(["!disabled"])


checkPlagiarism = ttk.Button(homePage, text="Check Plagiarism", state='disabled', command=lambda: show_frame(mainPage),
                             style='Accent.TButton')
checkPlagiarism.place(width=200, height=40, x=690, y=550)


# ************* Main page code

class TextScrollCombo(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ensure a consistent GUI size
        self.grid_propagate(False)
        # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = Text(self, font=("Helvetica", 12))
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

    def set_text(self, txt):
        self.txt.configure(state=NORMAL, wrap=WORD)
        self.txt.delete('1.0', END)
        self.txt.insert('1.0', txt)
        self.txt.configure(state=DISABLED, wrap=WORD)


text_displayer = TextScrollCombo(mainPage)
export = ttk.Button(mainPage, text="Export", command=lambda: export_(), style='Accent.TButton')


def show_text():  # display Pa
    text_displayer.place(width=850, height=400, x=25, y=110)
    displayParaText.state(["disabled"])
    displayPercentageButton.state(["disabled"])
    Thread(target=check, daemon=True).start()
    export.place(width=100, height=30, x=400, y=513)
    export.state(["disabled"])


displayed_text = ""


def export_():
    with open(os.path.expanduser("~/Desktop/cheatX_report.txt"), 'w', encoding='utf-8') as r:
        r.write(displayed_text)


def check():
    global displayed_text
    text_displayer.set_text('Please, wait...')
    text_displayer.update()
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    filenames = [file[:-4] for file in os.listdir(path) if file.endswith(".pdf")]
    filepaths = [f"{path}\{file}.pdf" for file in filenames]

    with cl.ExitStack() as stack:
        files = [stack.enter_context(pdf.open(fp)) for fp in filepaths]
        displayed_text = ''
        for f, fn in zip(files, filenames):
            files.remove(f)
            filenames.remove(fn)
            text = ""
            for p in f.pages:
                text += p.extract_text()
            sentences = text.split('.')
            for g, gn in zip(files, filenames):
                displayed_text += '▓' * 69 + f"\n{fn} ─── {gn}\n" + '▓' * 69 + '\n'
                text2 = ""
                for p in g.pages:
                    text2 += p.extract_text()
                sentences2 = text2.split('.')
                for sentence in sentences:
                    for sentence2 in sentences2:
                        embeddings = embed([sentence, sentence2])
                        r = np.inner(embeddings, embeddings)
                        if r[0][1] >= .85:
                            displayed_text += '─' * 69 + f"\n{sentence}\n\n{sentence2}\n" + '─' * 69 + '\n\n'
    text_displayer.set_text(displayed_text)
    displayParaText.state(["!disabled"])
    displayPercentageButton.state(["!disabled"])
    export.state(["!disabled"])


displayPercentageButton = ttk.Button(mainPage, text="Display Percentage", command=lambda: show_perc(),style='Accent.TButton')
displayPercentageButton.place(width=430.5 + 5, height=40, x=603 - 143.5 - 5, y=550)


def show_perc():
    text_displayer.place(width=850, height=400, x=25, y=110)
    displayPercentageButton.state(["disabled"])
    displayParaText.state(['disabled'])
    text_displayer.set_text('Please, wait...')
    text_displayer.update()
    export.place(width=100, height=30, x=400, y=513)
    export.state(["disabled"])

    def _workload():
        global displayed_text
        displayed_text = '─' * 75 + '\n'
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        filenames = [file[:-4] for file in os.listdir(path) if file.endswith(".pdf")]
        filepaths = [f"{path}\{file}.pdf" for file in filenames]
        x = []
        with cl.ExitStack() as stack:
            files = [stack.enter_context(pdf.open(fp)) for fp in filepaths]
            for f in files:
                text = ""
                for p in f.pages:
                    text += p.extract_text()
                x.append(text)
            embeddings = embed(x)
            r = np.inner(embeddings, embeddings)
            for i in range(len(filenames) - 1):
                j = i + 1
                for _ in range(len(filenames) - i - 1):
                    displayed_text += f"{filenames[i]} ─•─ {filenames[j]}: {round(r[i][j] * 100)}%\n" \
                                      + '─' * 75 + '\n'
                    j += 1
        text_displayer.set_text(displayed_text)
        displayPercentageButton.state(["!disabled"])
        displayParaText.state(['!disabled'])
        export.state(["!disabled"])

    Thread(target=_workload, daemon=True).start()


displayParaText = ttk.Button(mainPage, text="Display plagiarized Text", command=lambda: show_text(), style='Accent.TButton')
displayParaText.place(width=430.5 + 5, height=40, x=10, y=550)

window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "light")
window.mainloop()
