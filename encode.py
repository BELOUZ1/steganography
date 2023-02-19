import cv2
import numpy as np


class Encode:

    def msg_to_bin(self, msg):
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")

        # defining function to hide the secret message into the image

    def hide_data(self, img, secret_msg):
        # calculating the maximum bytes for encoding
        nBytes = img.shape[0] * img.shape[1] * 3 // 8
        print("Maximum Bytes for encoding:", nBytes)
        # checking whether the number of bytes for encoding is less
        # than the maximum bytes in the image
        if len(secret_msg) > nBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")
        secret_msg += '#####'  # we can utilize any string as the delimiter
        dataIndex = 0
        # converting the input data to binary format using the msg_to_bin() function
        bin_secret_msg = self.msg_to_bin(secret_msg)

        # finding the length of data that requires to be hidden
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

    def encodeText(self, data, img_name):
        img = cv2.imread(img_name)

        print("The shape of the image is: ",
              img.shape)
        print("The original image is as shown below: ")

        if len(data) == 0:
            raise ValueError('Data is Empty')

        encodedimage = self.hide_data(img, data)

        return encodedimage

    def save_new_image(self, encodedImage, file_name):
        cv2.imwrite(file_name, encodedImage)

    def decodeText(self, img_name):
        img = cv2.imread(img_name)  # reading the image using the imread() function

        text = self.show_data(img)
        return text
