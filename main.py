from urllib.request import Request, urlopen
from tkinter import *
from tkinter import filedialog, messagebox
import validators
from bs4 import BeautifulSoup

from pln import Pln

window = Tk()
file = ""
directory = ""
tipo = ""
entry = ""
label = ""
r1 = ""
r2 = ""
button = ""
boutput = ""


def process_text(text, directorio):
    window.destroy()
    x = Pln(text, directorio)
    x.process()
    window2 = Tk()
    window2.title("Analizador")
    window2.geometry("400x200")
    window2.resizable(width=0, height=0)
    window2.configure(background="white")
    Label(window2, text="Análisis Terminado", bg="white").pack(anchor=CENTER)


def open_file():
    Label(window, text=" ", bg="white", width=10000).place(x=110, y=40)
    global file
    file = ""
    file = filedialog.askopenfilename(initialdir="/", title="Seleccione archivo",
                                      filetypes=(("txt files", "*.txt"), ("All files", "*.*")))
    global tipo
    tipo = "1"
    global label
    label = Label(window, text=file, bg="white").place(x=110, y=10)


def open_url():
    global label
    label = Label(window, text=" ", bg="white", width=10000).place(x=110, y=10)
    global file
    file = ""
    global tipo
    tipo = "2"
    global entry
    entry = Entry(window, width=40, bg="aquamarine")
    entry.place(x=110, y=40)


def save_file():
    global directory
    directory = filedialog.askdirectory()
    Label(window, text=directory, bg="white").place(x=110, y=90)


def send_text(archivo, directorio, t):
    if archivo == "" and entry != "":
        archivo = entry.get()
    if archivo == "" or directorio == "" or t == "":
        messagebox.showerror(title="Error", message="No se puede procesar hasta que seleccione ambos parámetros")
    else:
        if t == "1":
            print(archivo)
            f = open(archivo, 'r', encoding="utf8", errors="ignore")
            text = f.read()
            print(text)
            process_text(text, directorio)
        else:
            print(archivo)
            if validators.url(archivo):
                req = Request(archivo, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                soup = BeautifulSoup(webpage, "html.parser")
                text = soup.get_text(strip=True)
                print(text)
                print("\n")
                process_text(text, directorio)
            else:
                messagebox.showerror(title="Error", message="Url incorrecta")


if __name__ == "__main__":
    window.title("Analizador")
    window.geometry("400x200")
    window.resizable(width=1, height=0)
    window.configure(background="white")

    option = IntVar()

    r1 = Radiobutton(window, text="Archivo", variable=option, bg="white",
                     value=1, command=lambda: open_file()).place(x=10, y=10)

    r2 = Radiobutton(window, text="URL", variable=option, bg="white",
                     value=2, command=lambda: open_url()).place(x=10, y=40)

    boutput = Button(window, text="Directorio", bg="aquamarine", width=11, height=1,
                     command=lambda: save_file()).place(x=10, y=90)

    button = Button(window, text="Aceptar", bg="aquamarine", width=11, height=1,
                    command=lambda: send_text(file, directory, tipo)).pack(anchor=CENTER, side=BOTTOM, pady=10)

    window.mainloop()
