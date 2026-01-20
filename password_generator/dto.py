import tkinter as tk

class EncodingKeyDto:
    def __init__(self):
        self.__key_label = None
        self.__key_entry = None

    @property
    def key_label(self):
        return self.__key_label
    @key_label.setter
    def key_label(self, key_label: str):
        self.__key_label = key_label
    @property
    def key_entry(self):
        return self.__key_entry
    @key_entry.setter
    def key_entry(self, key_entry: str):
        self.__key_entry = key_entry

class GeneratedPasswordDto:
    def __init__(self):
        self.__generated_password: tk.Text | None = None

    @property
    def generated_password(self)->tk.Text | None:
        return self.__generated_password
    @generated_password.setter
    def generated_password(self, generated_password: tk.Text):
        self.__generated_password = generated_password

    def destroy(self):
        if self.__generated_password:
            self.generated_password.destroy()