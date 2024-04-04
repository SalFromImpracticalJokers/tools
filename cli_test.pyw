import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import threading
import time
import random
import os
from firebase_admin import credentials, db, initialize_app

## GUI CLASS ##

class caspser_GUI:
    def __init__(self, root):
        self.service_account_info = {
            "type": "service_account",
            "project_id": "server-c0ac8",
            "private_key_id": "0cb0544fa293ab097f20813ce29362235fa6e6b7",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDojMt5ijXz8fVF\n4riktqKwY1lGOh4zGFHEP9TKBRd8f+iB086S/y+UCrara9NRpEb/v1cl7krTPpcN\nZ8b483dGw9vjMatjtyO3IUirbujcS3RG4eP4i2pT0NhFrsEkMeq+kb3dO73h7qqk\nP8GLOI0X8eFrWpkCA5xTFhng6TwaSV2UE50yjKnq1x9g4fSXDkeZkaWMuFT0jalA\n7HHiCN7IUvtNUVL8Hk+Sq071Yl+HLmNBl/isi23FCfSugLhZkvnp5+CHa/m/tCQ1\nzARC5my/ufP6BMvYtTlyfSLqRUvQNqv5qQcHXTMQeY3eBU7zITMScHIZMcaN65jQ\nrRaGb9GvAgMBAAECggEAPjG1k45eypzZ+7RcrJS54xHXBPyzKfglmiZ2Kwd8lgwB\na4NxuoesOlw5KZR/YlTctjZ+wMK/2UpijK/GG7vFmTP1oYgdreADmc05ibvyZER7\n1x8/4K+sorj2toA74InHHeuNi1cYfA3gLmhsw2a++Xnzz0neJRdBHkmJZ0kJjX+y\nDIf3ie898mxyuZgre1CAZ2BDeYnBXbwVyg4r6dgW6sW87pk+sV4Ggz/zAtHi/RN8\nnaoBhGSCTwdFrvWx9t+rarjKrz/1WEfJ9QbAGK1+qhCfXllBPDSCFlcnO0eWB+Wg\nBW9reeT2MWcfIzCQc24xpm+H8aSKkOSwyPC80KGD0QKBgQD6cs2KwH7IvPzICtEE\nfS8RWXrYd04dXvI7IgY4AFvXsJaO67KQxpUcnpKK6AOC/c4W6OJW7Jbbzrs+UvJC\ndWrd95hgw9445+Y8dTTTaM8MmIW3HKn8i/ZdKnnk9tkf8Lsl1tnXCBISRcY3GyRd\npzvGMGARJr3Llkc0ld/ZgMnkfwKBgQDttGzTuR795+w3XSbDz0u+Ov8eylayt5wY\nKEMYrOm9TMJsXJ9YjOkufqkq88LW+PEJgG9cjqObt9hpONN7AJAJ2+rF1W+r8Fjc\nE+t//ldUH+HoJwnMaJDRvP4sPDg40jQnoSJaaigJbL7L4u9gz3niCkck7DlV8lvF\nECNsImi60QKBgQCLv22Tw8+7AUFn+ikhgRy3aJ+UlBXha65scpLXwtN8qkuImlo8\nUKK5on4Qxl/XQvoxbGeHq2KOam+u2ifWD6C/FL5RGFoylKuzBo+ge7Y0yBKs13C+\nu/aPi/kSWu9S1EgJWDabtyQmUArHivyiyYMgFrQ0PdLf/A3leM+8lRGSzwKBgDh2\nRe9YpprrDvnrn3ydbcFm5BidOVDEOkimr6FZ2T+Ezx3MNnFjLzRDE83HDv3fLeny\n3wDeRNCFL9t2iw1Jie09lpudYiQ2N/U2qhbCBF5QIGnzc+lg4R1gxgMd3sDodUkA\nhldxpcbvVLa7Vd7qCWp+xH1puwjGQ7QgbDmQRs4xAoGBANbTJBFDfJCz85vOYnb9\nqgLoC8/ymyU/EB214JMvqfsxo0P6Jmz0uEL0GxANLBHNNlCR05DozNKD7dMYwB2C\nJpOiO1xZW5ejTeuGzJh7WzyrkNV2+EkDzJtnPBxxC+GclUf72sY/50V4B5Xf+Cgi\nuQUyAtFiI5RkLZud+/h5fRQN\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-4mxn3@server-c0ac8.iam.gserviceaccount.com",
            "client_id": "108573463227937256273",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4mxn3%40server-c0ac8.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

        # Replace with your service account key
        self.cred = credentials.Certificate(self.service_account_info)  # Replace with your service account key
        initialize_app(self.cred, {'databaseURL': 'https://server-c0ac8-default-rtdb.firebaseio.com/'})
        self.db = db
        
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.handle_window_close)
        self.display_frame = None
        self.input_frame = None
        self.menu_frame = None

        self.user_name = False
        self.chat_name = False
        self.chat_password = False

        # Set initial window size
        self.root.geometry("400x150")

        # Create a frame for the menu
        self.menu_frame = tk.Frame(self.root, bg="#333333")
        self.menu_frame.pack(expand=True, fill=tk.BOTH)

        # Add input field for user name
        user_name_label = tk.Label(self.menu_frame, text="Your Name:", bg="#333333", fg="white")
        user_name_label.grid(row=0, column=0, padx=10, pady=5)
        self.user_name_entry = tk.Entry(self.menu_frame, bg="#333333", fg="white", width=40)  # Increase width
        self.user_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Add input fields for chat name and password
        chat_name_label = tk.Label(self.menu_frame, text="Chat Name:", bg="#333333", fg="white")
        chat_name_label.grid(row=1, column=0, padx=10, pady=5)
        self.chat_name_entry = tk.Entry(self.menu_frame, bg="#333333", fg="white", width=40)  # Increase width
        self.chat_name_entry.grid(row=1, column=1, padx=10, pady=5)
        chat_password_label = tk.Label(self.menu_frame, text="Chat Password:", bg="#333333", fg="white")
        chat_password_label.grid(row=2, column=0, padx=10, pady=5)
        self.chat_password_entry = tk.Entry(self.menu_frame, bg="#333333", fg="white", width=40)  # Increase width
        self.chat_password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Add a frame for the buttons
        button_frame = tk.Frame(self.menu_frame, bg="#333333")
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Add buttons to create or join chat
        create_chat_button = tk.Button(button_frame, text="Create Chat", command=self.create_chat)
        create_chat_button.pack(side=tk.LEFT, padx=5)
        create_chat_button.bind("<Return>", lambda event: self.create_chat())

        join_chat_button = tk.Button(button_frame, text="Join Chat", command=self.join_chat)
        join_chat_button.pack(side=tk.LEFT, padx=5)
        join_chat_button.bind("<Return>", lambda event: self.join_chat())

        delete_chat_button = tk.Button(button_frame, text="Delete Chat", command=self.delete_chat)
        delete_chat_button.pack(side=tk.LEFT, padx=5)
        delete_chat_button.bind("<Return>", lambda event: self.delete_chat())

        list_chat_button = tk.Button(button_frame, text="List Chats", command=self.list_chats)
        list_chat_button.pack(side=tk.LEFT, padx=5)
        list_chat_button.bind("<Return>", lambda event: self.list_chats())

        # Adjust column weights
        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        self.menu_frame.grid_columnconfigure(2, weight=1)
        self.menu_frame.grid_columnconfigure(3, weight=1)



    def handle_window_close(self):
        # Add any necessary cleanup or exit logic here
        self.root.destroy()

    def list_chats(self):
        try:
            root_ref = db.reference()
            sections = root_ref.get(shallow=True)
            section_names = list(sections.keys())
            for i in section_names:
                if "deleted-" in str(i): section_names.pop(section_names.index(i))
        except:
            section_names = []
        messagebox.showinfo("Chats", (("Chats:\n\n"+"\n".join(section_names)) if section_names != [] else "There are no chats"))

    def delete_chat(self):
        user_name = self.user_name_entry.get()
        chat_name = self.chat_name_entry.get()
        chat_password = self.chat_password_entry.get()

        # Check if any field is empty
        if not all((user_name, chat_name, chat_password)):
            messagebox.showerror("Error", "Please fill out all fields.")
            return
        else:
            # Clear input fields
            self.clear_input_fields()

        try:
            root_ref = db.reference()
            sections = root_ref.get(shallow=True)
            section_names = list(sections.keys())
        except:
            section_names = []
        if chat_name in section_names:
            self.user_name = user_name
            self.chat_name = chat_name
            self.chat_password = chat_password

            ref = self.db.reference(f'/{self.chat_name}')
            messages = ref.get()
            if messages:
                for message_id, message_data in messages.items():
                    if not casper_dec(message_data.get('sender'), self.chat_password):
                        messagebox.showerror("Error", "Incorrect password.")
                        self.go_back_to_menu()
                    else:
                        ref = self.db.reference(f'/{self.chat_name}')
                        ref.push().set({"message": casper_enc(f"deleted the chat", self.chat_password), "sender": casper_enc(f"{self.user_name}", self.chat_password)})
                        ref = self.db.reference('/')

                        # Rename the node
                        ref = self.db.reference('/')
                        # Get the data from the old node
                        old_data = ref.child(f'{self.chat_name}').get()
                        # Delete the old node
                        ref.child(f'{self.chat_name}').delete()
                        # Set the data to the new node
                        ref.child(f'deleted-{self.chat_name}').set(old_data)
                        messagebox.showinfo("Chats", "Chat deleted")
                        
                    break
            else:
                messagebox.showerror("Error", "Chat is corrupt.")
                self.go_back_to_menu()

        else:
            messagebox.showerror("Error", "Could not find this chat.")
            self.go_back_to_menu()
        self.go_back_to_menu()

    def create_chat(self):
        user_name = self.user_name_entry.get()
        chat_name = self.chat_name_entry.get()
        chat_password = self.chat_password_entry.get()

        # Check if any field is empty
        if not all((user_name, chat_name, chat_password)):
            messagebox.showerror("Error", "Please fill out all fields.")
            return
        else:
            # Clear input fields
            self.clear_input_fields()

        try:
            root_ref = db.reference()
            sections = root_ref.get(shallow=True)
            section_names = list(sections.keys())
        except:
            section_names = []
        if chat_name not in section_names:
            self.user_name = user_name
            self.chat_name = chat_name
            self.chat_password = chat_password

            ref = self.db.reference(f'/{self.chat_name}')
            ref.push().set({"message": casper_enc(f"made the chat", self.chat_password), "sender": casper_enc(self.user_name, self.chat_password)})

            # Open display area with chat details
            self.open_display()
        
        else:
            messagebox.showerror("Error", "This chat already exists")
            self.go_back_to_menu()

    def join_chat(self):
        user_name = self.user_name_entry.get()
        chat_name = self.chat_name_entry.get()
        chat_password = self.chat_password_entry.get()

        # Check if any field is empty
        if not all((user_name, chat_name, chat_password)):
            messagebox.showerror("Error", "Please fill out all fields.")
            return
        else:
            # Clear input fields
            self.clear_input_fields()
        try:
            root_ref = db.reference()
            sections = root_ref.get(shallow=True)
            section_names = list(sections.keys())
        except:
            section_names = []
        if chat_name in section_names:
            self.user_name = user_name
            self.chat_name = chat_name
            self.chat_password = chat_password

            ref = self.db.reference(f'/{self.chat_name}')
            messages = ref.get()
            if messages:
                for message_id, message_data in messages.items():
                    if not casper_dec(message_data.get('sender'), self.chat_password):
                        messagebox.showerror("Error", "Incorrect password.")
                        self.go_back_to_menu()
                    else:
                        ref = self.db.reference(f'/{self.chat_name}')
                        ref.push().set({"message": casper_enc(f"joined the chat", self.chat_password), "sender": casper_enc(f"{self.user_name}", self.chat_password)})

                        # Open display area with chat details
                        self.open_display()
                    break
            else:
                messagebox.showerror("Error", "Chat is corrupt.")
                self.go_back_to_menu()

        else:
            messagebox.showerror("Error", "Could not find this chat.")
            self.go_back_to_menu()

    def open_display(self):
        # Hide the menu
        self.menu_frame.pack_forget()

        # Create the main window
        self.root.title(f"{self.chat_name} - {self.user_name}")
        self.root.geometry("700x500")  # Set window size

        # Create a frame for the display
        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(expand=True, fill=tk.BOTH)

        # Create a scrolled text widget for display
        self.display_text = scrolledtext.ScrolledText(self.display_frame, wrap=tk.WORD, bg="#333333", fg="white")
        self.display_text.pack(expand=True, fill=tk.BOTH)
        self.display_text.config(state=tk.DISABLED)  # Disable editing
        self.display_text.tag_config("command", foreground="white")

        # Add entry box for sending messages
        self.input_frame = tk.Frame(self.root, bg="#333333")
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM)
        input_entry = tk.Entry(self.input_frame, bg="#333333", fg="white", width=60)  # Increase width
        input_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        input_entry.bind("<Return>", lambda event: self.send_message(input_entry))

        # Add button to send messages
        send_button = tk.Button(self.input_frame, text="Send", command=lambda: self.send_message(input_entry))
        send_button.pack(side=tk.LEFT, padx=5, pady=10)
        send_button.bind("<Return>", lambda event: self.send_message(input_entry))

        # Add button to exit the chat
        exit_button = tk.Button(self.input_frame, text="Exit Chat", command=self.go_back_to_menu)
        exit_button.pack(side=tk.LEFT, padx=5, pady=10)
        exit_button.bind("<Return>", lambda event: self.go_back_to_menu())

        self.stop_thread = threading.Event()
        self.thread = threading.Thread(target=self.check_for_new_messages)
        self.thread.start()

    def send_message(self, input_entry):
        message = input_entry.get()
        if message.strip() != "" and message != None:
            input_entry.delete(0, tk.END)
            time.sleep(0.01)
            ref = self.db.reference(f'/{self.chat_name}')
            ref.push().set({"message": casper_enc(message, self.chat_password), "sender": casper_enc(f"{self.user_name}", self.chat_password)})

    def add_messages_to_display(self, new_messages):
        if self.display_frame:
            self.display_text.config(state=tk.NORMAL)
            current_text = self.display_text.get(1.0, tk.END)
            cur_list = current_text.split("\n")[1:][:-1]
            if new_messages != cur_list:
                try:
                    add = "\n".join(new_messages[(len(cur_list) if cur_list != [] else 0):])
                    time.sleep(0.001)
                    self.display_text.insert(tk.END, "\n"+add)
                except:
                    self.display_text.delete(1.0, tk.END)
                    time.sleep(0.001)
                    self.display_text.insert(tk.END, "\n"+"\n".join(new_messages))
                self.display_text.config(state=tk.DISABLED)
                self.display_text.see(tk.END)

    def go_back_to_menu(self):
        self.user_name = False
        self.chat_name = False
        self.password = False

        # Destroy or hide the display frame and input frame to go back to the menu
        if self.display_frame:
            self.display_frame.destroy()
        if self.input_frame:
            self.input_frame.destroy()
        self.menu_frame.pack(expand=True, fill=tk.BOTH)
        self.root.geometry("400x150")  # Set initial window size

    def clear_input_fields(self):
        self.user_name_entry.delete(0, tk.END)
        self.chat_name_entry.delete(0, tk.END)
        self.chat_password_entry.delete(0, tk.END)

    def check_for_new_messages(self):
        while not self.stop_thread.is_set():
            try:
                new_messages = []  # List to store new messages
                ref = self.db.reference(f'/{self.chat_name}')
                messages = ref.get()
                if messages:
                    for message_id, message_data in messages.items():
                        if "str" not in str(type(message_data)).lower():
                            if casper_dec(message_data.get('sender'), self.chat_password) != self.user_name:
                                message = casper_dec(message_data.get('sender'), self.chat_password)
                                message += ": " + casper_dec(message_data.get('message'), self.chat_password)
                                new_messages.append(message)
                            elif casper_dec(message_data.get('sender'), self.chat_password) == self.user_name:
                                message = "You"
                                message += ": " + casper_dec(message_data.get('message'), self.chat_password)
                                new_messages.append(message)
                    
                    # Update display all at once
                    self.add_messages_to_display(new_messages)
                    
                time.sleep(0.01)  # Adjust sleep duration as needed
            except Exception as e:
                time.sleep(0.1)
                #print(casper_dec(message_data.get('message'), self.chat_password))

    def stop_checking_messages(self):
        try:
            self.stop_thread.set()
            self.thread.join()
        except: pass

## CASPER ##

## VARS ##

subs = ['#@', 'jj', '11', 'Yd', '}T', ')E', 'AV', 'O ', 'c/', '}5', 'I1', '#d', 'oz', '2k', '$!', '3E', 'iv', 'R@', ' D', 'tT', '22', ">'", 'W ', 'p-', "s'", '-$', '>o', 'eP', '|D', '33', '|1', 'rv', 'y[', 'W&', 'SN', '5m', 'MD', 'MV', '44', 'U+', '55', 'Y:', 'p*', 'zN', '|t', '1i', 'Xb', 'g;', 's~', 'c6', 'fT', 'JF', '(C', 'u.', '66', '77', 'D2', '88', 'Ru', 'YF', '[d', ';_', 'R|', '`)', 'P<', '%t', 'Wa', 'G"', 'XU', 'Bd', ']8', 'wd', '!b', '3t', '99', 'kM', 'o6', 'm<', 'WR', '5t', '[c', '"|', 'Ac', 'v:', 'x[', 'XM', 'a!', 'Dq', 'u9', '}=', 'Km', 'VD', '.K', '2}', ']q']
characters = ['2', '8', '\\', '`', "'", 'Z', '#', '1', ';', 'D', '5', 'j', 'M', '&', 'n', ']', 'i', 'X', '6', 'C', 'p', '3', 'v', '{', 's', '0', 'B', 'T', '.', 'f', '/', '^', 't', 'U', 'N', 'u', ':', 'J', '[', 'P', ')', 'H', '}', '>', 'I', 'b', 'Q', 'w', 'F', '=', '*', 'W', ',', 'e', 'x', 'h', 'V', 'S', '4', 'k', '7', 'A', 'G', 'l', 'r', '-', 'a', '(', 'R', 'y', 'g', '9', 'c', 'Y', '<', 'L', '%', '?', '"', '$', '|', '+', 'o', 'z', 'O', 'E', '@', '~', 'K', ' ', '_', 'm', 'q', 'd', '!']
defualt = "01010010010101110110110100110101011111000101001001100011010110110110101001101010010100100101011101101010011010100101001001010111"

## ENC FUNCS ##

def string_to_binary_byte_data(string):
    byte_data = string.encode('ascii')    
    binary_byte_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_byte_data

def binary_byte_data_to_string(binary_byte_data):
    byte_chunks = [binary_byte_data[i:i+8] for i in range(0, len(binary_byte_data), 8)]
    byte_data = bytes(int(chunk, 2) for chunk in byte_chunks)
    decoded_string = byte_data.decode('ascii')
    return decoded_string

def calculate_byte_data_size(byte_data):
    size_in_bits = len(byte_data) * 8
    padding = (int((128-(size_in_bits % 128)) / 8))
    return size_in_bits, padding

def xor(binary, key):
    return ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(binary, key))

def enc(string):
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    new_string = "".join([subs[characters.index(i)] for i in string])
    new_string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in new_string])
    return new_string

def dec(string):
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    new_string = "".join([characters[subs.index(i)] for i in ([string[i:i+2] for i in range(0, len(string), 2)])])
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in new_string])
    return string

def pad(string, padding):
    if padding != 0:
        string = string[-1] + string
        while padding > 1:
            add_char = random.choice(characters)
            if add_char != string[0]:
                padding -= 1
                string += add_char
    return string

def de_pad(string):
    orig = string
    last_letter = string[0]
    last_index = string.rfind(last_letter)
    string = string[:last_index+1][1:]
    if string.strip() != "": return string
    else: return orig

def rep(binary):
    byte_data = bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    hex_data = byte_data.hex()[::-1]
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in hex_data])
    return string

def de_rep(text):
    text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in text])
    hex_data = text[::-1]
    byte_data = bytes.fromhex(hex_data)
    binary_byte_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_byte_data

def casper_enc(text, password):
    ciphered_text = enc(text)[::-1]
    initial_size, padding = calculate_byte_data_size(ciphered_text)
    padded_text = pad(ciphered_text, padding)
    encrypted_padded_text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in padded_text])
    new_size = initial_size + (8*padding)
    key = key_gen(password, new_size)
    binary_data = string_to_binary_byte_data(encrypted_padded_text)
    binary_data = xor(binary_data, key)
    binary_data = xor(binary_data, key[::-1])
    defualt_com = defualt
    while len(defualt_com) != len(binary_data):
        defualt_com = defualt_com[::-1] + defualt
    binary_data = xor(binary_data, defualt_com)
    binary_data = xor(binary_data[::-1], key)
    binary_data = binary_data[::-1]
    output = rep(binary_data)
    return output

## DEC FUNCS

def casper_dec(text, password):
    try:
        if text[0] == "'" and text[-1] == "'": text = text[1:][:-1]
        binary_data = de_rep(text)
        key = key_gen(password, len(binary_data))
        binary_data = binary_data[::-1]
        binary_data = xor(binary_data, key)[::-1]
        defualt_com = defualt
        while len(defualt_com) != len(binary_data):
            defualt_com = defualt_com[::-1] + defualt
        binary_data = xor(binary_data, defualt_com)
        binary_data = xor(binary_data, key[::-1])
        binary_data = xor(binary_data, key)
        cipher_text = binary_byte_data_to_string(binary_data)
        cipher_text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in cipher_text])
        cipher_text = de_pad(cipher_text)
        final = dec(cipher_text[::-1])
        return final
    except Exception as e:
        input(e)
        return False

## KEY GEN ##

def ceaser(string, size):
    new_string = "".join([characters[(characters.index(i)+size)%len(characters)] for i in string])
    return new_string

def key_gen(string, size):
    for i in string:
        string = ceaser(string, characters.index(i))
    string = enc(string + string[::-1])
    key_size, _ = calculate_byte_data_size(string)
    string_list = [characters.index(i) for i in string]
    string = "".join([characters[i] for i in sorted(string_list)])
    if key_size > size:
        new_string = string[:(len(string))-int((key_size - size) / 8)]
    elif key_size < size:
        while calculate_byte_data_size(string)[0] < size:
            string = enc(string)
        if calculate_byte_data_size(string)[0] > size:
            string = string[:(len(string))-int((calculate_byte_data_size(string)[0] - size) / 8)]
        new_string = string
    else:
        new_string = string
    binary = string_to_binary_byte_data(new_string[::-1])
    defualt_com = defualt
    while len(defualt_com) != len(binary):
        defualt_com = defualt_com[::-1] + defualt
    binary = xor(binary, defualt_com)
    return binary


## VARS ##
           
root = tk.Tk()
root.title("CASPER ETE CHAT")
app = caspser_GUI(root)

## THREADS ##

root.mainloop()
os._exit(1)
