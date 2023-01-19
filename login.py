import customtkinter
from test import Test
from ldap3 import Server, Connection, SAFE_SYNC

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"







class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Secure chat")
        self.geometry(f"{800}x{580}")

        # configure grid layout (4x4)
        #self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2 , weight=3)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Features :",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkLabel(self.sidebar_frame,text="- RSA encryption", anchor="w")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10,)
        self.sidebar_button_2 = customtkinter.CTkLabel(self.sidebar_frame,text="- Ldap ....", anchor="w")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkLabel(self.sidebar_frame,text="- Certificate x509..", anchor="w")
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



        #login frame

        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=1, rowspan=5,columnspan=4, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.login_frame, text="Welcome to secure chat",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10),sticky="n")
        self.name_label = customtkinter.CTkLabel(self.login_frame, text="Username :",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.name_label.grid(row=1,column=0,padx=20, pady=(20, 20))
        self.name_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="")
        self.name_entry.grid(row=1, column=1,  padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.password_label = customtkinter.CTkLabel(self.login_frame, text="Password :",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.password_label.grid(row=2, column=0, padx=20, pady=(20, 20))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="")
        self.password_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.login_button = customtkinter.CTkButton(self.login_frame, command=self.login_button_event)
        self.login_button.grid(row=3, column=1, padx=20, pady=10)

        self.sign_label = customtkinter.CTkLabel(self.login_frame, text="No account ? :",
                                                     font=customtkinter.CTkFont(size=10, weight="normal"))
        self.sign_label.grid(row=4, column=0, padx=20, pady=(20, 20))
        self.sign_button = customtkinter.CTkButton(self.login_frame,fg_color="transparent",border_width=2, text_color=("gray10", "#DCE4EE"), command=self.sign_button_event)
        self.sign_button.grid(row=4, column=1, padx=20, pady=10)


        #Sign up frame
        self.sign_up_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.logo_label = customtkinter.CTkLabel(self.sign_up_frame, text="Welcome to secure chat",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="n")
        self.name_label = customtkinter.CTkLabel(self.sign_up_frame, text="Username :",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.name_label.grid(row=1, column=0, padx=20, pady=(20, 20))
        self.name_entry = customtkinter.CTkEntry(self.sign_up_frame, placeholder_text="")
        self.name_entry.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.mail_label = customtkinter.CTkLabel(self.sign_up_frame, text="email :",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.mail_label.grid(row=2, column=0, padx=20, pady=(20, 20))
        self.mail_entry = customtkinter.CTkEntry(self.sign_up_frame, placeholder_text="")
        self.mail_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.password_label = customtkinter.CTkLabel(self.sign_up_frame, text="Password :",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.password_label.grid(row=3, column=0, padx=20, pady=(20, 20))
        self.password_entry = customtkinter.CTkEntry(self.sign_up_frame, placeholder_text="")
        self.password_entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.sign_up_button = customtkinter.CTkButton(self.sign_up_frame, command=self.signup_button_event)
        self.sign_up_button.grid(row=4, column=1, padx=20, pady=10)
        self.back_button = customtkinter.CTkButton(self.sign_up_frame, command=self.back_button_event,fg_color="transparent",border_width=2, text_color=("gray10", "#DCE4EE"),)
        self.back_button.grid(row=5, column=1, padx=20, pady=10)


        # user frame




        # set default values
        self.login_button.configure( text="Login")
        self.sign_button.configure(text="Sign up!")
        self.sign_up_button.configure(text="Sign up")
        self.back_button.configure(text="back")

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")




    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sign_button_event(self):
        self.login_frame.grid_remove()
        self.sign_up_frame.grid(row=0, column=1, rowspan=5, columnspan=4, sticky="nsew")

    def back_button_event(self):
        self.sign_up_frame.grid_remove()
        self.login_frame.grid(row=0, column=1, rowspan=5, columnspan=4, sticky="nsew")

    def login_button_event(self):
        print("logiiiin")
        self.name = self.name_entry.get()
        self.password = self.password_entry.get()
        print(self.name)
        print(self.password)


    def signup_button_event(self):
        print("siiiiign up")
        self.name = self.name_entry.get()
        self.password = self.password_entry.get()
        self.mail = self.mail_entry.get()
        print(self.name)
        print(self.password)
        print(self.mail)


app = App()
app.mainloop()