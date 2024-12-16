#login.py

from tkinter import *
from tkinter import ttk
#from PIL import ImageTk, Image
#from tkcalendar import Calendar
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime
import os,sys

# ---TIPO DE CUENTAS---
#  1 = Maestro
#  2 = Preceptor
#  3 = Administrador

tipoCuenta = 0

class login1:
    
    def conectar_mysql(self):
        self.sql = mysql.connector.connect(
                            host='eestn1.com.ar',
                            user='tecnica1',
                            password='z%51#q57A7BR',
                            database='tec_boletines2023',
                            port=3306
                            )
        self.cursor = self.sql.cursor()
    def cerrar_mysql(self):
        self.sql.close()
        self.cursor.close()
    def crear(self,tk,menuFunc): #crear login
        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)   
        BGcolor="#98c1d9" #color del fondo de pantalla esta ventana y otras

        tk.configure(bg=BGcolor)
 
        fuente_grande = ('Arial', 30, "bold")
        fuente_grande1 = ('Arial', 32, "bold")
        fuente_grande2 = ('Arial', 20)
        fuente_mediana = ('Arial', 16)
        fuente_chica = ('Arial', 12)

        BG2 = Frame(tk, bg='#98c1d9',width=512,height=32)
        BG1 = Frame(tk, bg='#4A90E2',width=80,height=256)
        BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.18, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

        etiqueta_derecha = Label(BG2, text="©6to5ta - 2024", bg="#98c1d9", fg="white",font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        #logo
        path = resource_path("Imagenes/Colegio_logo.ico")
        tk.iconbitmap(path)
        
#    def init(self):
        imagen_path = resource_path("Imagenes/Colegio_logo.png")
        image = Image.open(imagen_path)
        photo = ImageTk.PhotoImage(image.resize((200, 240)))
        image_label = Label(BG1,image=photo, bg='#4A90E2',highlightthickness=0, borderwidth=0)
        image_label.image = photo 
        image_label.pack()

       
        BG1.columnconfigure(0,weight=1)

        
        frame_label1 = Frame(BG1, bg='#4A90E2')
        frame_label1.place(relx=0.0, rely=0.4, anchor="nw")
        mayus_label1 = Label(frame_label1, text="E", fg="white", bg='#4A90E2', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=10)
        text_label1 = Label(frame_label1, text="scuela de", fg="white", bg='#4A90E2', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label2 = Frame(BG1, bg='#4A90E2')
        frame_label2.place(relx=0.0, rely=0.5, anchor="nw")
        mayus_label2 = Label(frame_label2, text="E", fg="white", bg='#4A90E2', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=10)
        text_label2 = Label(frame_label2, text="ducación", fg="white", bg='#4A90E2', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label3 = Frame(BG1, bg='#4A90E2')
        frame_label3.place(relx=0.0, rely=0.6, anchor="nw")
        mayus_label3 = Label(frame_label3, text="S", fg="white", bg='#4A90E2', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=10)
        text_label3 = Label(frame_label3, text="ecundaria", fg="white", bg='#4A90E2', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label4 = Frame(BG1, bg='#4A90E2')
        frame_label4.place(relx=0.0, rely=0.7, anchor="nw")
        mayus_label4 = Label(frame_label4, text="T", fg="white", bg='#4A90E2', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=10)
        text_label4 = Label(frame_label4, text="écnica", fg="white", bg='#4A90E2', font=fuente_grande2).grid(row=0, column=1, sticky='nws',pady=5)

        frame_label5 = Frame(BG1, bg='#4A90E2')
        frame_label5.place(relx=0.0, rely=0.8, anchor="nw")
        mayus_label5 = Label(frame_label5, text="Nº1", fg="white", bg='#4A90E2', font=fuente_grande1).grid(row=0, column=0, sticky='nes',pady=10)


        loginTitle1 = Label(tk, text="Inicio de Sesión",font=fuente_grande,bg=BGcolor)
        loginTitle1.place(relx = 0.6, rely = 0.02, anchor ='n')

        # ---Usuario---
        loginLabel1 = Label(tk, text="Usuario",font=fuente_mediana,bg=BGcolor)
        loginLabel1.place(relx = 0.6, rely = 0.2, anchor ='n')
        loginInput1 = Entry(tk, width = 25, font=fuente_mediana, borderwidth=0,relief="solid")
        loginInput1.place(relx = 0.6, rely = 0.27, anchor ='n')



        # ---Email---
        loginLabel2 = Label(tk, text="Email",font=fuente_mediana,bg=BGcolor,)
        loginLabel2.place(relx = 0.6, rely = 0.35, anchor ='n')
        loginInpu = Entry(tk, width = 25, font=fuente_mediana,borderwidth=0,relief="solid")
        loginInpu.place(relx = 0.6, rely = 0.42, anchor ='n')


        # ---Contraseña---
        
        loginLabel3 = Label(tk, text="Contraseña",font=fuente_mediana,bg=BGcolor)
        loginLabel3.place(relx = 0.6, rely = 0.5, anchor ='n')
        loginInput3 = Entry(tk, width = 25, font=fuente_mediana, borderwidth=0, relief="solid", show="*") 
        loginInput3.place(relx = 0.6, rely = 0.57, anchor ='n')


        loginError = Label(tk, text="", font=fuente_chica, bg=BGcolor) 
        loginError.place(relx = 0.6, rely = 0.67, anchor ='n')
        #INSERT INTO usuarios (usuario, email, contraseña) VALUES (%s,%s,%s);

        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()
        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))
        def procesar_enter(event):
            logear()
        def logear():
            self.conectar_mysql()
            usuario=loginInput1.get()
            email=loginInpu.get()
            contraseña=loginInput3.get()
            self.cursor.execute("SELECT * FROM usuarios WHERE Usuario=%s AND email=%s AND Contraseña=%s", (usuario, email, contraseña))
            loginFetch = self.cursor.fetchone()

            self.cerrar_mysql()
            
            if usuario=="" or email=="" or contraseña=="":
                loginError.config(text="Introduzca un Usuario, Email y Contraseña")
                tk.bell()
            elif loginFetch==None:
                loginError.config(text = "Usuario, Email o Contraseña Incorrectos.")
                tk.bell()
            else:
                loginInput1.delete(0,END)
                loginInpu.delete(0,END)
                loginInput3.delete(0,END)
                loginError.config(text="")
                if loginFetch[4]==1:
                    print("tipo de cuenta 1 (maestro)")
                    eliminar()
                    tipoCuenta = 1
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                elif loginFetch[4]==2:
                    print("tipo de cuenta 2 (preceptor)")
                    eliminar()
                    tipoCuenta = 2
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                elif loginFetch[4]==3:
                    print("tipo de cuenta 3 (administrador)")
                    eliminar()
                    tipoCuenta = 3
                    menuFunc(tipoCuenta,loginFetch[1])
                    return
                else:
                    print("ERROR: tipo de cuenta desconocido")
                    return
        style = ttk.Style()
        style.configure("TButton", background="black",width=40,)         
        loginBoton = Button(tk, text ="Iniciar Sesión",width=40,height=3,borderwidth=0, command = logear,background="#004385",fg="white")
        tk.bind('<Return>', procesar_enter)
        loginInput1.focus_set()
        loginBoton.place(relx = 0.6, rely = 0.7, anchor ='n')
        changeOnHover(loginBoton, "#16466B", "#004385")