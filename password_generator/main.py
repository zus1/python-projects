import tkinter as tk
from generator import Generator
from tkinter import messagebox
from dto import EncodingKeyDto, GeneratedPasswordDto


def provide_encoding_key():
    if encode_var.get():
        encoding_dto.key_label = tk.Label(root, text="Encryption Key")
        encoding_dto.key_entry = tk.Entry(root, textvariable=encode_key_var)
        encoding_dto.key_label.pack()
        encoding_dto.key_entry.pack()
    else:
        encoding_dto.key_label.destroy()
        encoding_dto.key_entry.destroy()

def generate_password():
    generated_password_dto.destroy()

    generator = Generator()
    generator.upper_case_required = uppercase_required.get()
    generator.numbers_required = numbers_required.get()
    generator.symbols_required = symbols_required.get()
    generator.encode = encode_var.get()
    if encode_key_var.get():
        generator.encoding_key = encode_key_var.get()

    password = None
    try:
        password = generator.generate(length=int(length_var.get()) if length_var.get() else None)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

    if password:
        generated_password_dto.generated_password = tk.Text(root, font=("Arial", 30, "bold"), height=1, borderwidth=1)
        generated_password_dto.generated_password.insert(1.0, password)
        generated_password_dto.generated_password.config(state='disabled')
        generated_password_dto.generated_password.pack()

def main():
    requirements = tk.Label(root, text="Requirements:", font=("Arial", 20, "bold"))
    requirements.pack(pady=5)

    length_label = tk.Label(root, text='Length')
    length_label.pack()
    length_entry = tk.Entry(root, textvariable=length_var)
    length_entry.pack(pady=10)

    check_uppercase = tk.Checkbutton(root, text="Must contain uppercase", variable=uppercase_required, onvalue=True, offvalue=False)
    check_uppercase.pack()
    check_numbers = tk.Checkbutton(root, text="Must contain number", variable=numbers_required, onvalue=True, offvalue=False)
    check_numbers.pack()
    check_symbols = tk.Checkbutton(root, text="Must contain symbol", variable=symbols_required, onvalue=True, offvalue=False)
    check_symbols.pack()
    encode_password = tk.Checkbutton(root, text="Encode", variable=encode_var, onvalue=True,offvalue=False, command=provide_encoding_key)
    encode_password.pack()

    generate_btn = tk.Button(root, text="Generate", command=generate_password)
    generate_btn.pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("500x500")

    length_var = tk.StringVar()
    uppercase_required = tk.BooleanVar()
    numbers_required = tk.BooleanVar()
    symbols_required = tk.BooleanVar()
    encode_var = tk.BooleanVar()
    encode_key_var = tk.StringVar()

    encoding_dto = EncodingKeyDto()
    generated_password_dto = GeneratedPasswordDto()

    main()

    root.mainloop()