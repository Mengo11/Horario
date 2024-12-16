import tkinter as tk
from tkinter import ttk
import mysql.connector
import re,sys,os
from PIL import Image, ImageTk  # Para imágenes

# Definir los colores
BGcolor = "#c9daf8"
BG1color = "#212121"
BG2color = "#6D9EEB"
#BLUE = "#6D9EEB"
#BLACK = "#212121"


class registrar1():
    #def __init__(self,ventana,sql,cursor):
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
    def crear(self,ventana,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc,valores=[False]):
        ventana.columnconfigure (0,minsize=0)
        #ventana.columnconfigure (6,minsize=250)

        def eliminar():
            for elemento in ventana.winfo_children():
                elemento.destroy()
        def volver():
            ventana.columnconfigure (0,minsize=0)
            eliminar()
            cuentasFunc(ventana,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            return
        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
        def registrar():
            mensaje_error.config(text="\n", fg="red")
            # Obtener los valores ingresados por el usuario
            nombre_usuario = entry_usuario.get()
            contraseña = entry_contraseña.get()
            email = entry_email.get()
            confirmar_contraseña = entry_confirmar_contraseña.get()
           
            tipoSelect = entry_tipo.get()
            
            tipo = 0
            for i in tipos:
                if i[1] == tipoSelect:
                    tipo = i[0]
                    print(tipo)
                    break
            if not tipo in (1,2,3):
                print("ERROR: tipo de cuenta no seleccionado o invalido")
                ventana.bell()
                return
            
            if email.count('.') > 3 or email.count('.') == 0 or email.count('@') != 1 or not re.match(r'^[\w-]+@', email):
                # Si el correo no cumple con el formato o tiene más de una "@", mostramos un mensaje de error
                tk.messagebox.showerror("Error", "Dirección de correo inválida su correo debe verse asi example@gmail.com")
                entry_email.delete(0, tk.END)  # Borramos el contenido del Entry
                return False 
            
            LoginValores = [nombre_usuario,contraseña,email,tipo,confirmar_contraseña]
            SQLmaterias = []
            if tipo == 1:
                for materia in seleccionM:
                    materia = ",".join(materia)
                    SQLmaterias.append(materia)
                    print(materia)
                SQLmaterias = list(set(SQLmaterias)) #remover materias duplicadas si por cualquier razon las hay
                SQLmaterias = ";".join(SQLmaterias)
                print(SQLmaterias)

            # --CHECKEO TODOS LOS CAMPOS LLENADOS--
            incompleto = False
            for valor in LoginValores:
                if valor is None or valor=="":
                    incompleto=True
            
            if incompleto is True:
                mensaje_error.config(text="Llene todos los campos\n", fg="red")
                ventana.bell()
                return

            
            # --CHECKEO CONTRASEÑAS COINCIDEN--
            if contraseña != confirmar_contraseña:
                # Mostrar un mensaje de error si las contraseñas no coinciden
                mensaje_error.config(text="Las contraseñas no coinciden\n", fg="red")
                ventana.bell()
                return
            

            # --CHECKEO CONTRASEÑA Y USUARIO SON DIFERENTES--
            if contraseña == nombre_usuario:
                # Mostrar un mensaje de error si la contraseña y el nombre son lo mismo
                mensaje_error.config(text="El usuario y la contraseña\nno pueden ser iguales.", fg="red")
                ventana.bell()
                return

            self.conectar_mysql()
            # --CHECKEO CUENTA YA EXISTE--
            self.cursor.execute(f"SELECT ID FROM usuarios WHERE usuario='{nombre_usuario}' or email='{email}' ")
            registrado = self.cursor.fetchone()
            self.cerrar_mysql()
            #si la cuenta ya existe y no se esta editando, si no que registrando un usuario nuevo:
            if not registrado is None and valores[0] is False: 
                mensaje_error.config(text="Esta Cuenta ya Existe\n", fg="red")
                ventana.bell()
                return
            


            # --SI TODOS LOS CHECKEOS SE PASAN, REGISTRAR O ACTUALIZAR CUENTA--
            if LoginValores[3]==1: #en el caso que el tipo sea maestro, agrega horarios al query de insert
                print("a")
                queryMaterias = f", '{SQLmaterias}'"
                queryMaterias2 = ",MATERIAS"
                queryMaterias3 = f", MATERIAS='{SQLmaterias}'"
            else: #en cualquier otro caso, no agrega nada
                print("b")
                queryMaterias = ""
                queryMaterias2 = ""
                queryMaterias3 = ""

            if valores[0]==True: #en el caso de que se este editando un usuario existente

                if valores[1] is False: #en el caso que la contraseña este oculta
                    queryContraseña = f", contraseña='{LoginValores[1]}'"
                else:
                    queryContraseña = ""

                print(LoginValores)
                print(queryContraseña)
                print(queryMaterias3)
                print(valores[6])
                self.conectar_mysql()
                self.cursor.execute(f"""UPDATE usuarios SET
                               usuario='{LoginValores[0]}',
                               email='{LoginValores[2]}'{queryContraseña},
                               tipo='{LoginValores[3]}'{queryMaterias3}
                               WHERE ID={valores[6]}""")
                self.sql.commit()
                print("Usuario Actualizado")
                self.cerrar_mysql()


            else: #en el caso que se este registrando un usuario nuevo
                self.conectar_mysql()
                self.cursor.execute(f"INSERT INTO usuarios (usuario,email,contraseña,tipo{queryMaterias2}) VALUES ('{LoginValores[0]}', '{LoginValores[2]}', '{LoginValores[1]}', '{LoginValores[3]}'{queryMaterias})")
                print("Usuario Registrado")
                self.sql.commit()
                mensaje_error.config(text="Usuario Registrado Exitosamente\n", fg="black")
                self.cerrar_mysql()
            
            #vaciar todos los campos
            entry_usuario.delete(0, tk.END)
            entry_contraseña.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_confirmar_contraseña.delete(0, tk.END)
            entry_tipo.current(0)

            #si se estaba editando, volver a cuentas.py
            if valores[0]==True:
                volver()
                    

        def arroba(event):
            contenido = entry_email.get()
            # Utilizamos una expresión regular para verificar el formato del correo
            if contenido.count('.') > 3 or contenido.count('.') == 0 or contenido.count('@') != 1 or not re.match(r'^[\w-]+@', contenido):
                if len(contenido) >0:
                    # Si el correo no cumple con el formato o tiene más de una "@", mostramos un mensaje de error
                    tk.messagebox.showerror("Error", "Dirección de correo inválida su correo debe verse asi example@gmail.com")
                    entry_email.delete(0, tk.END)  # Borramos el contenido del Entry
                    return False
                
        def limite(event):
            contenido = entry_email.get()
            contenido2 = entry_usuario.get()
            contenido3 = entry_contraseña.get()
            contenido4 = entry_confirmar_contraseña.get()
            
            if len(contenido) > 100:
                # Limitar el contenido a 11 caracteres
                nuevo_contenido = contenido[:100]
                entry_email.delete(0, tk.END)
                entry_email.insert(0, nuevo_contenido)
                tk.messagebox.showerror("Error", "Solo se permiten 100 caracteres")
            elif len(contenido2) > 50:
                nuevo_contenido2 = contenido2[:50]
                entry_usuario.delete(0, tk.END)
                entry_usuario.insert(0, nuevo_contenido2)
                tk.messagebox.showerror("Error", "Solo se permiten 50 caracteres")
            elif len(contenido3) > 20:
                nuevo_contenido3 = contenido3[:20]
                entry_contraseña.delete(0, tk.END)
                entry_contraseña.insert(0, nuevo_contenido3)
                tk.messagebox.showerror("Error", "Solo se permiten 20 caracteres")
            elif len(contenido4) > 20:
                nuevo_contenido4 = contenido4[:20]
                entry_confirmar_contraseña.delete(0, tk.END)
                entry_confirmar_contraseña.insert(0, nuevo_contenido4)
                tk.messagebox.showerror("Error", "Solo se permiten 20 caracteres")
                
                

        # Obtener la altura de la ventana
        #ventana_height = int(ventana.winfo_height()) #por ahora no se usa para nada esto

        # Crear un canvas para el rectángulo negro a la izquierda
        # canvas_izquierda = tk.Canvas(ventana, bg=BLACK, height=ventana_height)
        # canvas_izquierda.place(relx=0.0, rely=1.0, anchor='sw', relwidth=0.18, relheight=1.0)  # Sticky para que el rectángulo se expanda verticalmente

        # Crear un canvas para la barra azul abajo
        # canvas_abajo = tk.Canvas(ventana, bg=BLUE, width=512, height=32)  # Height es la altura de la barra azul
        # canvas_abajo.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)  # "ew" para que la barra se expanda horizontalmente
        

        # Crear un Frame que servirá como fondo
        frame_fondo = tk.Frame(ventana, bg="#050b1b")
        frame_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda la ventana
        BG2 = tk.Frame(ventana, bg="#050b1b",width=512,height=32)
        #BG1 = tk.Frame(ventana, bg=BG1color,width=80,height=256)
        #BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.1, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)


        etiqueta_derecha = tk.Label(BG2, text="©6to5ta - 2024", bg="#050b1b",fg="white",font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        frame_entry=tk.Frame(ventana,bg="#13191a", bd=2, relief="solid")
        frame_entry.place(relx = 0.11, rely = 0.03, anchor ='nw', relwidth=0.8, relheight=0.87)

        frame_entry.columnconfigure(0,weight=1)
        frame_entry.columnconfigure(1,weight=1)
        frame_entry.columnconfigure(2,weight=1)
        frame_entry.rowconfigure(0,weight=1)
        frame_entry.rowconfigure(1,weight=1)
        frame_entry.rowconfigure(2,weight=1)
        frame_entry.rowconfigure(3,weight=1)

        imagen_path = resource_path("Imagenes/logo HighRes.png")
        image = Image.open(imagen_path)
        photo = ImageTk.PhotoImage(image.resize((420, 420)))
        image_label = tk.Label(frame_entry,image=photo, bg='#13191a',highlightthickness=0, borderwidth=0)
        image_label.image = photo 

      
        # Etiquetas y campos de entrada
        label_titulo = tk.Label(frame_entry, text="Registrar Cuenta", bg="#13191a",fg="white", font=("Arial", 20,"bold"))
        
        label_usuario = tk.Label(frame_entry, text="Nombre de Usuario:", bg="#13191a",fg="white", font=("Arial", 12))
        entry_usuario = tk.Entry(frame_entry, font=("Arial", 10), width=39,bd=2, relief="flat",fg="white", bg="#13191a",borderwidth=0, insertbackground='white')
        entry_usuario.bind("<KeyRelease>", limite)
        
        label_email = tk.Label(frame_entry, text="Email:", bg="#13191a",fg="white", font=("Arial", 15))
        
        entry_email = tk.Entry(frame_entry, font=("Arial", 10), width=39,bd=2, relief="flat",fg="white", bg="#13191a",borderwidth=0, insertbackground='white')
        entry_email.bind("<FocusOut>", arroba,)
        entry_email.bind("KeyRelease", limite)

        label_contraseña = tk.Label(frame_entry, text="Contraseña:", bg="#13191a",fg="white", font=("Arial", 15))
        entry_contraseña = tk.Entry(frame_entry, font=("Arial", 10), width=39, show="*",bd=2,fg="white", relief="flat", bg="#13191a",borderwidth=0, insertbackground='white')
        entry_contraseña.bind("<KeyRelease>", limite)


        label_confirmar_contraseña = tk.Label(frame_entry, text="Confirmar Contraseña:", fg="white",bg="#13191a", font=("Helvetica", 15))
        entry_confirmar_contraseña = tk.Entry(frame_entry, font=("Arial", 10), width=39, show="*",bd=2,fg="white", relief="flat", bg="#13191a",borderwidth=0, insertbackground='white')

        

        tipos = [(3,"Administrador"),(2,"preceptor"),(1,"maestro")]
        tipos_combobox = []
        for i in tipos:
            tipos_combobox.append(i[1])

            
        label_tipo = tk.Label(frame_entry, text="Tipo de cuenta:", bg="#13191a",fg="white", font=("Helvetica", 10))
        entry_tipo = ttk.Combobox(frame_entry, values=tipos_combobox,state="enable", font=("Helvetica", 10), width=23)
        entry_tipo.set('Administrador')
        
 
        seleccionM = []
        print(valores)
        if valores[0]==True and valores[5]=="Maestro" and valores[7] is not None:
            listaM = list(valores[7].split(";"))
            for materia in listaM:
                materia = tuple(materia.split(","))
                seleccionM.append(materia)
        print(seleccionM)
  
        
        def add_line(frame, relx, rely):
         line = tk.Frame(frame, height=2, bg="white", bd=0)
         line.place(relx=relx, rely=rely, relwidth=0.25)
        def accionMaterias(var,boton,materia,curso,division):
            print(str(var.get()))
            print(materia,curso,division)
            seleccion=(materia,str(curso+"_"+division))
            if var.get() is True:
                if not seleccion in seleccionM:
                    seleccionM.append(seleccion)
            else:
                try:
                    seleccionM.remove(seleccion)
                except:
                    pass
            
            print(seleccionM)
     
        

        # Botón de registro
        boton_registrar = tk.Button(frame_entry, text="Registrar", font=("Arial", 12, "bold"), bg="#2979FF", fg="white", bd=0, width=27, cursor="hand2", command=registrar)
        boton_volver = tk.Button(frame_entry, text="Volver", font=("Arial", 10, "bold"), bg="#2979FF", fg="white", bd=0, width=15, cursor="hand2", command=volver)

        # Etiqueta para mostrar mensajes de error
        mensaje_error = tk.Label(frame_entry, text="\n",  fg="white", font=("Helvetica", 12))  # Cambia el tamaño de la fuente aquí

       
        # Título
        label_titulo.place(relx=0.35, rely=0.05)

        # Usuario
        label_usuario.place(relx=0.60, rely=0.2)
        entry_usuario.place(relx=0.70, rely=0.25)
        add_line(frame_entry, relx=0.70, rely=0.29)  

        # Email
        label_email.place(relx=0.60, rely=0.3)
        entry_email.place(relx=0.70, rely=0.35)
        add_line(frame_entry, relx=0.70, rely=0.39)  

        # Contraseña
        label_contraseña.place(relx=0.60, rely=0.4)
        entry_contraseña.place(relx=0.70, rely=0.45)
        add_line(frame_entry, relx=0.70, rely=0.49)  

        # Confirmar contraseña
        label_confirmar_contraseña.place(relx=0.60, rely=0.5)
        entry_confirmar_contraseña.place(relx=0.70, rely=0.55)
        add_line(frame_entry, relx=0.70, rely=0.59)  # Línea debajo del campo Confirmar Contraseña

        # Tipo de cuenta
        label_tipo.place(relx=0.60, rely=0.6)
        entry_tipo.place(relx=0.70, rely=0.65)

        # Botones
        boton_registrar.place(relx=0.65, rely=0.75)
        boton_volver.place(relx=0.88, rely=0.95)
        image_label.place(relx=0.1,rely=0.2)

       




        

"""
if __name__ == "__main__":
    sql = mysql.connector.connect(user='root',#usuario registrado en el mysql
                                  password='', #contraseña del usuario
                                  host='127.0.0.1', #IP del server mysql (en este caso localhost)
                                  autocommit=True #automaticamente aplicar cambios
                                  #database='pynotas' #Base de datos que se usara
                                  )
    cursor = sql.cursor()

    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("Registro")
    ventana.columnconfigure ((0,1,2,3,4,5,6), weight=1)
    ventana.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
    ventana.columnconfigure (0,minsize=80)

    

    # Establecer la resolución de la ventana
    ventana.geometry("712x480")
    
    registrar = registrar1(ventana)
    registrar.crear(ventana,3,"Admin","menuFunc","cuentasFunc")

    # Iniciar el bucle principal de la ventana
    ventana.mainloop()
"""