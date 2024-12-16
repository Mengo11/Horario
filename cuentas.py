try:
    from tkinter import *
    from tkinter import ttk,messagebox
    from tkcalendar import Calendar
    from PIL import ImageTk, Image

    import mysql.connector
    from datetime import datetime
    import os,sys
    
except:
    print("no se encuentran librerias nesesarias")
    exit()


from registrar import registrar1

BGcolor="#c9daf8"  #Celeste muy claro
BG1color="#212121" #Negro
BG2color="#6D9EEB" #Celeste
BG3color="#A4C2F4" #Celeste claro
BG4color="#6FA8DC" #Cyan
BG5color="#9E9E9E" #gris claro

  
class cuentas1:
  
    def __init__(self, tk):
        self.registrar=registrar1()
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
    def crear(self,tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc):
        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()
        def volver():
            eliminar()
            menuFunc(tipoCuenta,nombreCuenta)
            return
        
        def funcregistrar():
            eliminar()
            self.registrar.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)


        

        checkbox_var = BooleanVar()
        checkbox_var.set(False)

        def eliminarCuenta(lista):
            seleccion = lista.selection()
            print(seleccion)
            if len(seleccion)<=0:
                messagebox.showinfo(message="No se ha seleccionado\nninguna usuario", title="Error")
            else:
                opcion = messagebox.askyesno(message="esta usted seguro?\nse eliminaran los usuarios seleccionados", title="Advertencia",icon='warning')
                if opcion==True:
                    for i in seleccion:
                        fila = lista.item(i)
                        fila = fila.get("values")
                        print(fila)
                        print(fila[0])
                        self.conectar_mysql()
                        self.cursor.execute(f"DELETE FROM usuarios WHERE ID='{fila[0]}' LIMIT 1")
                        self.sql.commit()
                        self.cerrar_mysql()
                    ObtenerLista(UltimoTipo)


        #tk.grid_columnconfigure(0, weight=1)

        FrameTOP = Frame(tk,bg=BGcolor)
        FrameTOP.place(relx = 0.0, rely = 0.0, anchor ='nw', relwidth=1.0, relheight=0.15)

        FrameBotones=Frame(FrameTOP,bg=BGcolor)
        FrameBotones.place(relx = 1.0, rely = 0.5, anchor ='e', relwidth=1.0, relheight=0.8)

        FrameCurso=Frame(FrameTOP, bg=BGcolor, highlightbackground=BG1color, highlightthickness=1)
        FrameCurso.place(relx = 0.0, rely = 0.48, anchor ='sw', relwidth=0.74, relheight=0.4)

        FrameCurso.columnconfigure(tuple(range(0,4)), weight=1)
        FrameCurso.rowconfigure(0, weight=1)

        FrameLabel1 = Frame(FrameCurso,bg=BG2color, highlightbackground=BG1color, highlightthickness=0.5)
        FrameLabel1.grid(row=0,column=0,columnspan=2,sticky="news")



        LabelAÑO = Label(FrameCurso, bg=BG2color, text="Tipo de Cuenta:")
        LabelAÑO.grid(row=0,column=0,columnspan=2)

        BotonTipo0 = Button(FrameCurso,text="Todos",bg=BG3color,relief="solid",borderwidth=1,width=8, command=lambda: SeleccionTipo(0))
        BotonTipo0.grid(row=0,column=2,columnspan=2,sticky="news")

    

        FrameBotones.columnconfigure(tuple(range(0,8)), weight=1)
        FrameBotones.rowconfigure((0,1), weight=1)
        #iconos de botones
        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
        imagen_eliminar_path = resource_path("imagenes/eliminar.png")
        imagen_volver_path = resource_path("imagenes/volver.png")
        imagen_editar_path = resource_path("imagenes/editar.png")
        imagen_imprimir_path = resource_path("imagenes/imprimir.png")
        self.imagen_eliminar =ImageTk.PhotoImage(Image.open(imagen_eliminar_path).resize((20, 20), Image.LANCZOS))
        self.imagen_volver =ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20), Image.LANCZOS))
        self.imagen_editar =ImageTk.PhotoImage(Image.open(imagen_editar_path).resize((15, 15), Image.LANCZOS))
        self.imagen_imprimir = ImageTk.PhotoImage(Image.open(imagen_imprimir_path).resize((20, 20), Image.LANCZOS))
        
        
        Botones = [(0, BotonTipo0)]


        OcultarContraseña = BooleanVar(value=True)

        #BotonPeticion = Button(FrameBotones, text ="Enviar Peticion",width=20)#, command = lambda: accion.actualizar(0,lista))
        BotonImprimir = Button(FrameBotones, text ="Imprimir",image=self.imagen_imprimir,compound="left",width=40)#, command = lambda: accion.actualizar(0,lista))
        BotonVolver   = Button(FrameBotones, text ="Volver",image=self.imagen_volver,compound="left",width=60, command = lambda: volver())
        BotonCuenta   = Button(FrameBotones, text ="Registrar Cuenta",width=20, command = lambda: funcregistrar())
        BotonContraseña= Checkbutton(FrameBotones, text="Ocultar Contraseñas",width=20,variable=OcultarContraseña,bg=BGcolor,activebackground=BGcolor,command=lambda: ObtenerLista(UltimoTipo))

        BotonImprimir["state"] = "disabled"

        #BotonPeticion.grid(row=0,column=0,columnspan=2,padx=4,pady=(0,1),sticky="news")
        BotonImprimir.grid(row=0,column=7,columnspan=1,padx=(4,1),pady=(0,1),sticky="news")
        BotonVolver.grid(row=0,column=8,columnspan=1,padx=(1,4),pady=(0,1),sticky="news")
        BotonCuenta.grid(row=1,column=7,columnspan=2,padx=4,pady=(1,0),sticky="news")
        BotonContraseña.grid(row=1,column=0,columnspan=3,padx=4,pady=(1,0),sticky="news")
        



        lista = ttk.Treeview(tk, columns=("c1","c2","c3","c4","c5"), show='headings', selectmode='extended')

        #lista.column("#0",anchor=CENTER, stretch=NO, width=0, minwidth=0)
        lista.column("#1",anchor=CENTER, width=20, minwidth=20)
        lista.column("#2",anchor=CENTER, width=90, minwidth=100)
        lista.column("#3",anchor=CENTER, width=120, minwidth=100)
        lista.column("#4",anchor=CENTER, width=90, minwidth=100)
        lista.column("#5",anchor=CENTER, width=60, minwidth=20)
        #lista.column("#6",anchor=CENTER, stretch=YES, width=100, minwidth=100)
        #lista.heading('#0', text='\n') #para mas lineas de texto en el heading, agregar mas "\n"
        lista.heading('#1', text='ID')
        lista.heading('#2', text='Usuario')
        lista.heading("#3", text="Email")
        lista.heading('#4', text='Contraseña')
        lista.heading('#5', text='Tipo de Cuenta')
        #lista.heading('#6', text='DNI')
        lista.place(relx = 0.0, rely = 0.15, anchor ='nw', relwidth=1.0, relheight=0.78)


        #Fondo
        BG2 = Frame(tk, bg=BG2color,width=512,height=32)
        #BG1 = Frame(tk, bg=BG1color,width=80,height=256)
        #BG1.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=0.1, relheight=1.0)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)

        etiqueta_derecha = Label(BG2, text="©6to5ta - 2024", bg=BG2color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=BG2color,font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')

        subfix = " > Cuentas"
        if tipoCuenta==1:
            etiqueta_izquierda.config(text=str("Profesor"+subfix))
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text=str("Preceptor"+subfix))
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text=str("Administrador"+subfix))


        
        def EditarCuenta():
            filaSeleccion = lista.selection()
            print(filaSeleccion)
            if len(filaSeleccion)<=0:
                messagebox.showinfo(message="No se ha seleccionado\nninguna usuario", title="Error")
            elif len(filaSeleccion)>1:
                messagebox.showinfo(message="Seleccione solo 1 usuario", title="Error")
            else:
                ocultar = OcultarContraseña.get()
                listaSeleccion = lista.item(filaSeleccion)
                seleccion = listaSeleccion['values']
                print(seleccion)
                eliminar()
                self.conectar_mysql()
                if ocultar is True:
                    self.cursor.execute(f"SELECT contraseña FROM usuarios WHERE ID={seleccion[0]}")
                    seleccion[3] = self.cursor.fetchone()[0]
                if seleccion[4]=="Maestro":
                    self.cursor.execute(f"SELECT MATERIAS FROM usuarios WHERE ID={seleccion[0]}")
                    seleccion.append(self.cursor.fetchone()[0])
                    self.registrar.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc,[True,ocultar,seleccion[1],seleccion[2],seleccion[3],seleccion[4],seleccion[0], seleccion[5]])
                else:
                    self.registrar.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc,[True,ocultar,seleccion[1],seleccion[2],seleccion[3],seleccion[4],seleccion[0]])
                self.cerrar_mysql()

        
        #obtener notas de cuenta en cuestion
        def ObtenerLista(tipo):
            global UltimoTipo
            UltimoTipo=tipo
            ocultar = OcultarContraseña.get()
            lista.delete(*lista.get_children()) #Limpiar lista antes de insertar nuevos elementos
            self.conectar_mysql()
            if tipo==0:
                self.cursor.execute("SELECT ID, usuario, email, contraseña, tipo FROM usuarios")
            else:
                self.cursor.execute(f"SELECT ID, usuario, email, contraseña, tipo FROM usuarios WHERE tipo={tipo}")
            cuentas = self.cursor.fetchall()
            self.cerrar_mysql()
            for cuenta in cuentas:
                cuenta = list(cuenta)
                if ocultar==True:
                    cuenta[3] = '*' * len(cuenta[3])
                print(cuenta)
                
                if cuenta[4]==1:
                    cuenta[4]="Maestro"
                elif cuenta[4]==2:
                    cuenta[4]="Preceptor"
                elif cuenta[4]==3:
                    cuenta[4]="Administrador"
                else:
                    cuenta[4]="Desconocido"
                
                lista.insert('',END,values=cuenta)
        def SeleccionTipo(tipo):
            for btn in Botones:
                if btn[0] == tipo:
                    btn[1].config(relief="sunken",bg=BG4color)
                    ObtenerLista(tipo)
                else:
                    btn[1].config(relief="solid",bg=BG3color)
        
        SeleccionTipo(0)
if __name__=="__main__":
    #ventana principal
    tk = Tk()
    tk.title("pyNotas")
    tk.geometry("1200x680")
    #tk.resizable(0,0)
    tk.configure(bg=BGcolor)

    #--ARREGLO BUG DE TKINTER--
    def fixed_map(option):
        return [elm for elm in style.map('Treeview', query_opt=option) if
        elm[:2] != ('!disabled', '!selected')]
    style = ttk.Style()
    style.map('Treeview', foreground=fixed_map('foreground'),
    background=fixed_map('background'))
    for columna in range(10):
        tk.grid_columnconfigure(columna,weight=1)
    for fila in range(10):
        tk.grid_rowconfigure(fila,weight=1)

    def funcExit(a,b):
        exit()

    cuentas = cuentas1(tk)
    def cuentasFunc1(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc):
        cuentas.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)

    cuentasFunc1(tk,3,"test",funcExit,cuentasFunc1)

    tk.mainloop()