import os
import sys
import datetime
import random
import qrcode as qr
import tkinter as tk
from PIL import ImageTk, Image
from qrcode.image.pil import PilImage


def generate_qr_code():
    qr_image = generate()
    filename = save(qr_image)
    display(filename)

def generate()->PilImage:
    code = qr.QRCode(
        version=1,
        error_correction=qr.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    code.add_data(url_var.get())
    code.make(fit=True)

    return code.make_image(fill_color="black", back_color="white")

def save(qr_image: PilImage)->str:
    filename = f'{random.randint(1000, 9999)}_{str(datetime.datetime.now().timestamp()).split(".")[0]}.png'
    qr_image.save(f'./codes/{filename}')

    return filename

def display(filename:str):
    image = Image.open(f'./codes/{filename}')
    image = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=image)
    image_label.image = image  # Prevent GC
    image_label.pack(pady=30)

def clear():
    for filename in os.listdir('./codes'):
        if os.path.isfile(f'./codes/{filename}'):
            os.remove(f'./codes/{filename}')

    if len(os.listdir('./codes')):
        sys.stderr.write('Could not delete qr code images\n')

def main():

    label = tk.Label(root, text="Enter Url to Generate QR Code")
    label.pack()

    url = tk.Entry(root, textvariable=url_var, width=50)
    url.pack(pady=10)

    generate_btn = tk.Button(root, text='Generate', width=30, command=generate_qr_code)
    generate_btn.pack(pady=10)

    generate_btn = tk.Button(root, text='Clear all codes', width=30, command=clear)
    generate_btn.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("QR Code Generator")
    root.geometry("500x700")

    url_var = tk.StringVar()

    main()

    root.mainloop()