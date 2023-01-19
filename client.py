import threading
import socket

import rsa
import customtkinter


#nickname = input("Choose your Username: ")
#public_key, private_key = rsa.newkeys(1024)

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(('127.0.0.1', 7777))

HOST = '127.0.0.1'
PORT = 7777

class Client():
    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST,PORT))
        self.nickname = input("Choose your Username: ")
        self.public_key, self.private_key = rsa.newkeys(1024)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

        # configure window

    def gui_loop(self):

        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
        self.app = customtkinter.CTk()

        self.app.title("Secure chat")
        self.app.geometry(f"{800}x{580}")

        # configure grid layout

        self.app.grid_columnconfigure(1, weight=3)
        self.app.grid_columnconfigure(2, weight=3)
        self.app.grid_rowconfigure((0, 1, 2), weight=1)

        #sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self.app, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Features :",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkLabel(self.sidebar_frame, text="- RSA encryption", anchor="w")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, )
        self.sidebar_button_2 = customtkinter.CTkLabel(self.sidebar_frame, text="- Ldap ....", anchor="w")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkLabel(self.sidebar_frame, text="- Certificate x509..", anchor="w")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # chaaat
        self.textbox = customtkinter.CTkTextbox(self.app)
        self.textbox.grid(row=0, column=1, rowspan=3, columnspan=3, sticky="nsew")

        #self.textbox.insert("0.0", "new text to insert")  # insert at line 0 character 0
        #text = self.textbox.get("0.0", "end")  # get text from line 0 character 0 till the end
        self.textbox.configure(state='disabled')

        self.entry = customtkinter.CTkEntry(self.app, placeholder_text="")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.send_button = customtkinter.CTkButton(master=self.app, fg_color="transparent", border_width=2,text="Send",
                                                     text_color=("gray10", "#DCE4EE"),command=self.write)
        self.send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s",)

        self.gui_done = True
        self.app.protocol("WM_DELETE_WINDOW",self.stop)
        self.app.mainloop()


    def write(self):

        message = f"{self.nickname}:{self.entry.get()}"
        self.sock.send(message.encode('ascii'))
        self.entry.delete(0,END)


    def stop(self):
        self.running = False
        self.app.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        i = 2
        while self.running:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.sock.recv(1024)
                if (i == 0):
                    if(self.gui_done):

                      msg = rsa.decrypt(message, self.private_key).decode('ascii')
                      self.textbox.configure(state='normal')
                      self.textbox.insert("end", msg+'\n')
                      self.textbox.yview('end')
                      self.textbox.configure(state='disabled')
                      print(msg)
                    continue
                if message.decode('ascii') == 'Username':
                    i -= 1
                    self.sock.send(self.nickname.encode('ascii'))
                elif message.decode('ascii') == 'key':
                    i -= 1
                    self.sock.send(self.public_key.save_pkcs1("PEM"))
                else:
                    msg = rsa.decrypt(message, self.private_key).decode('ascii')
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.sock.close()
                break

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = Client()
    #app.gui_loop()

#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#write_thread = threading.Thread(target=write)
#write_thread.start()


