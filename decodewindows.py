import os
from tkinter import *
from tkinter import filedialog

import PIL
import cv2
import numpy as np
from PIL import ImageTk


class DecodeWindow(Toplevel):

    def msg_to_bin(self, msg):
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")

    def show_data(self, img):
        bin_data = ""
        for values in img:
            for pixels in values:
                # converting the Red, Green, Blue values into binary format
                r, g, b = self.msg_to_bin(pixels)
                # data extraction from the LSB of Red pixel
                bin_data += r[-1]
                # data extraction from the LSB of Green pixel
                bin_data += g[-1]
                # data extraction from the LSB of Blue pixel
                bin_data += b[-1]
                # splitting by 8-bits
        allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]
        # converting from bits to characters
        decodedData = ""
        for bytes in allBytes:
            decodedData += chr(int(bytes, 2))
            # checking if we have reached the delimiter which is "#####"
            if decodedData[-5:] == "#####":
                break
                # print(decodedData)
        # removing the delimiter to display the actual hidden message
        return decodedData[:-5]

    def decodeText(self, img_name):
        img = cv2.imread(img_name)
        return self.show_data(img=img)

    def decodetext(self):
        mytext = self.decodeText(filepath)
        my_label.config(text=mytext)

    def setImage(self):
        global filepath
        file = filedialog.askopenfile(mode='r', filetypes=[('Image JPG', '*.jpg'), ('Image PNG', '*.png')])
        if file:
            filepath = os.path.abspath(file.name)
            image = PIL.Image.open(filepath)
            load = image.resize((350, 350))
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=200, y=10)

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Decoder")
        self.geometry("800x600")

        openImage = Button(self, text="Choisir une image", width=20, height=2, command=lambda: self.setImage())
        openImage.place(x=50, y=500)

        decodeText = Button(self, text="Décoder l'image", width=20, height=2, command=lambda: self.decodetext())
        decodeText.place(x=270, y=500)

        global my_label
        my_label = Label(self,
                         text="decoded text")
        my_label.place(x=50, y=400)
