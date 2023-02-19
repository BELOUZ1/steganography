from tkinter import *
from encodewindow import EncodeWindow
from decodewindows import DecodeWindow

fenetre = Tk()


def encodeWindow():
    EncodeWindow(fenetre)


def decodeWindow():
    DecodeWindow(fenetre)


def app():
    fenetre.geometry("500x300")
    fenetre.title("Steganography")
    buttonEncoder = Button(fenetre, text="Encoder", width=10, height=2, command=encodeWindow)
    buttonEncoder.place(x=200, y=80)
    buttonDecoder = Button(fenetre, text="Décoder", width=10, height=2, command=decodeWindow)
    buttonDecoder.place(x=200, y=160)

    fenetre.mainloop()


if __name__ == '__main__':
    app()
