import os
from tkinter import *
from tkinter import filedialog

import PIL
import cv2
import numpy as np
from PIL import ImageTk


class EncodeWindow(Toplevel):
    filepath = "";
    def msg_to_bin(self, msg):
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")

    def encodeText(self, data, img_name):
        img = cv2.imread(img_name)

        print("The shape of the image is: ",
              img.shape)
        print("The original image is as shown below: ")

        if len(data) == 0:
            raise ValueError('Data is Empty')

        encodedimage = self.hide_data(img, data)

        return encodedimage

    def hide_data(self, img, secret_msg):
        nBytes = img.shape[0] * img.shape[1] * 3 // 8
        print("Maximum Bytes for encoding:", nBytes)
        if len(secret_msg) > nBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")
        secret_msg += '#####'
        dataIndex = 0
        bin_secret_msg = self.msg_to_bin(secret_msg)

        dataLen = len(bin_secret_msg)
        for values in img:
            for pixels in values:
                # converting RGB values to binary format
                r, g, b = self.msg_to_bin(pixels)
                # modifying the LSB only if there is data remaining to store
                if dataIndex < dataLen:
                    # hiding the data into LSB of Red pixel
                    pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hiding the data into LSB of Green pixel
                    pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hiding the data into LSB of Blue pixel
                    pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)
                    dataIndex += 1
                    # if data is encoded, break out the loop
                if dataIndex >= dataLen:
                    break

        return img

    def setImage(self):
        global filepath
        file = filedialog.askopenfile(mode='r', filetypes=[('Image JPG', '*.jpg'), ('Image PNG', '*.png')])
        if file:
            filepath = os.path.abspath(file.name)
            image = PIL.Image.open(filepath)
            load = image.resize((400, 400))
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=10, y=10)

    def encoderImage(self, text, image):
        global newimage
        newimage = self.encodeText(data=text, img_name=image)

    def saveNewImage(self):
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename:
            filepath = os.path.abspath(filename.name)
            cv2.imwrite(filepath, newimage)


    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Encoder")
        self.geometry("800x600")

        inputtxt = Text(self, height=25, width=40, borderwidth=3, bg="white")
        inputtxt.place(x=450, y=10)

        openImage = Button(self, text="Choisir une image", width=20, height=2, command=lambda: self.setImage())
        openImage.place(x=50, y=500)

        encoderText = Button(self, text="Encoder le text", width=20, height=2,
                             command=lambda: self.encoderImage(inputtxt.get(1.0, "end-1c"),
                                                               filepath))
        encoderText.place(x=270, y=500)

        saveImage = Button(self, text="Sauvegarder l'image", width=20, height=2, command=lambda: self.saveNewImage())
        saveImage.place(x=500, y=500)
