import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import os,sys
from ttkthemes import ThemedStyle

#Hecho por Javier Correa Y contribuciones de Tobias Bonanno y valentino signorello
def eliminar(ventana):
        for elemento in ventana.winfo_children():
            elemento.destroy()

def resource_path(relative_path):
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
        base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
    return os.path.join(base_path, relative_path)
def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))
def botones_aulas(ventana,menuFunc,tipoCuenta,nombreCuenta):
    global imagen_eliminar,imagen_aula_ver,imagen_lab_ver,imagen_taller_ver,imagen_volver,imagen_taller_añadir,imagen_aula_añadir,imagen_lab_añadir,menufunc,tipodecuenta,nombrecuenta
    ventana.title("Pantalla de aulas")
    path = resource_path("Imagenes/Colegio_logo.ico")
    ventana.iconbitmap(path)
    menufunc=menuFunc
    tipodecuenta=tipoCuenta
    nombrecuenta=nombreCuenta
    BGcolor="#98c1d9"
    BG2color="#4A90E2"
    BG3color="#4A90E2"
    color_fondo = ventana.cget("bg")
    new_color = BGcolor if color_fondo != BG3color else BG3color
    color_label = BGcolor if new_color == BGcolor else BG3color
    nuevo_color = BG2color if new_color == BGcolor else "black"
    imagen_eliminar_path = resource_path("Imagenes/eliminar.png")
    imagen_lab_ver_path = resource_path("Imagenes/lab_ver.png")
    imagen_aula_ver_path = resource_path("Imagenes/aula_ver.png")
    imagen_taller_ver_path = resource_path("Imagenes/taller_ver.png")
    imagen_lab_añadir_path = resource_path("Imagenes/agregar_lab.png")
    imagen_aula_añadir_path = resource_path("Imagenes/prueba.png")
    imagen_taller_añadir_path = resource_path("Imagenes/taller_agregar_prueba.png")
    imagen_volver_path = resource_path("imagenes/volver.png")
    


    imagen_eliminar = ImageTk.PhotoImage(Image.open(imagen_eliminar_path).resize((15, 15)))
    imagen_lab_ver = ImageTk.PhotoImage(Image.open(imagen_lab_ver_path).resize((20, 20)))
    imagen_aula_ver = ImageTk.PhotoImage(Image.open(imagen_aula_ver_path).resize((20, 20)))
    imagen_taller_ver = ImageTk.PhotoImage(Image.open(imagen_taller_ver_path).resize((20, 20)))
    imagen_lab_añadir = ImageTk.PhotoImage(Image.open(imagen_lab_añadir_path).resize((20, 20)))
    imagen_aula_añadir = ImageTk.PhotoImage(Image.open(imagen_aula_añadir_path).resize((20, 20)))
    imagen_taller_añadir = ImageTk.PhotoImage(Image.open(imagen_taller_añadir_path).resize((20, 20)))
    imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))

    frame_pe = tk.Frame(ventana,bg=new_color)
    frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
    frame_pe.columnconfigure(0, weight=1)
    frame_pe.rowconfigure(0, weight=1)
    frame_pe.rowconfigure(1, weight=1)
    frame_pe.rowconfigure(2, weight=1)
        # Crear un frame para contener los perfiles de usuario

    frame_lab = tk.Label(frame_pe,bg=new_color)
    frame_lab.grid(sticky="nsew",column=0,row=1)
    BG2 = tk.Frame(ventana, bg=nuevo_color, width=512, height=32)
    BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
    etiqueta_derecha = tk.Label(BG2, text="©6°5 - 2024", bg=nuevo_color,fg="white",font=("Helvetica", 16))
    etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

    if  color_fondo== BG3color:
         style = ThemedStyle(frame_pe)
         style.set_theme("black")
    else : 
         style = ThemedStyle(frame_pe)
         style.set_theme("xpnative")



    frame_lab.columnconfigure(0, weight=1)
    frame_lab.columnconfigure(1, weight=1)
    frame_lab.rowconfigure(0, weight=1)
    frame_lab.rowconfigure(1, weight=1)
    frame_lab.rowconfigure(2, weight=1)


    tk.Label(frame_pe,text="  Pestaña de aulas",bg=color_label,fg="white" if color_label == BG3color else "black",border=1,font=("Monaco", 24, "bold")).grid(row=0,column=0,columnspan=3)

  
    tk.Button(frame_pe, text="Volver",image=imagen_volver,compound="left",borderwidth=0,relief="solid",height=30,width=200, command=lambda: volver_al_menu(ventana,menuFunc,tipoCuenta,nombreCuenta)).grid(row=2, column=0, padx=2, pady=2)
        

    tk.Button(frame_lab, text="Ver laboratorios",image=imagen_lab_ver,borderwidth=0,relief="solid",compound="left",height=30 , width=100, command=lambda:ver_aula(("Tipo de aula","Ubicacion","Numero"),("""SELECT * FROM aulas WHERE tipo_de_aula = "Laboratorio" """))).grid(row=0, column=0, padx=(300,10), pady=15,sticky="ew")
            

    añadir_lab = tk.Button(frame_lab, text="Añadir laboratorios",borderwidth=0,relief="solid",image=imagen_lab_añadir,compound="left",height=30 , width=100, command=lambda: agregar_aulas(("Tipo de aula", "Ubicacion", "Numero"), """SELECT * FROM aulas WHERE tipo_de_aula = "Laboratorio" """, "Laboratorio",(ventana)))
    añadir_lab.grid(row=0, column=1, padx=(10,300), pady=15, sticky="ew")
        
    tk.Button(frame_lab, text="Ver aulas",borderwidth=0,relief="solid",image=imagen_aula_ver,compound="left",height=30 , width=100, command=lambda:ver_aula(("Tipo de aula","Ubicacion","Numero"),("""SELECT * FROM aulas WHERE tipo_de_aula = "Aula" """))).grid(row=1, column=0, padx=(300,10), pady=15,sticky="ew")
            
            
    añadir_aula=tk.Button(frame_lab, text="Añadir aulas",image=imagen_aula_añadir,borderwidth=0,relief="solid",compound="left",height=30 , width=100, command=lambda: agregar_aulas(("Tipo de aula", "Ubicacion", "Numero"), """SELECT * FROM aulas WHERE tipo_de_aula = "Aula" """, "Aula",(ventana)))

    añadir_aula.grid(row=1, column=1, padx=(10,300), pady=15,sticky="ew")            
        

            

    tk.Button(frame_lab,borderwidth=0,relief="solid", text="Ver talleres",image=imagen_taller_ver,compound="left",height=30 , width=100, command=lambda:ver_aula(("Tipo de aula","Ubicacion","Numero"),("""SELECT * FROM aulas WHERE tipo_de_aula = "taller" """))).grid(row=2, column=0, padx=(300,10), pady=15,sticky="ew")
            
            
    añadir_taller= tk.Button(frame_lab, text="Añadir talleres",borderwidth=0,relief="solid",image=imagen_taller_añadir,compound="left",height=30 , width=100, command=lambda: agregar_aulas(("Tipo de aula", "Ubicacion", "Numero"), """SELECT * FROM aulas WHERE tipo_de_aula = "Taller" """, "Taller",(ventana)))

    añadir_taller.grid(row=2, column=1, padx=(10,300), pady=15,sticky="ew")
    for elemento in frame_lab.winfo_children():
        if isinstance(elemento, tk.Button):
            elemento['bg'] = "white"
            changeOnHover(elemento, "#A2AEE0", "white")
    
    if tipodecuenta==1:
        añadir_aula.configure(state="disabled")
        añadir_taller.configure(state="disabled")
        añadir_lab.configure(state="disabled")
    
def volver_al_menu(ventana,menuFunc,tipoCuenta,nombreCuenta):
    eliminar(ventana)
    menuFunc(tipoCuenta,nombreCuenta)    

def validar50(P):
    valor = laboratorio_numero.get()
    if valor:

        numero = int(P)
        if  numero == 1 or numero <= 100:
            return True
        else:
            messagebox.showerror("Error", "El número no puede ser mayor que 100 ni menor que 1.")
            spinbox.set(1)
            return False
       


def agregar_aulas(columnas_aula,query,Tipo_aula,ver_aula):
        global clicked, clicked2, laboratorio_numero, arriba, tree_aula, spinbox
        eliminar(ver_aula)
        
        conectar_base_de_datos()
        cursor = cnx.cursor()
        frame_pe = ttk.Frame(ver_aula)
        frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        treeview_aula=ttk.Labelframe(frame_pe, text="Aulas")
        treeview_aula.grid(padx=10, pady=10, row=1, column=0, sticky="nsew")

        
        scrollbar = ttk.Scrollbar(treeview_aula)
        scrollbar.pack(side="right", fill="y")
        tree_aula = ttk.Treeview(treeview_aula, yscrollcommand=scrollbar.set, selectmode="extended")
        tree_aula.pack(expand=True, fill="both")
        scrollbar.config(command=tree_aula.yview)
        
        tree_aula["columns"]=(columnas_aula)
        tree_aula.column("#0", width=0,)
        for columna in columnas_aula:
            tree_aula.column(columna, anchor="center")
            tree_aula.heading(columna, text=columna)
        cursor.execute(query)
        data = cursor.fetchall()
        for index, values in enumerate(data):
            tree_aula.insert(parent='', index='end', iid=index, values=values)
        tree_aula.pack()
        arriba = ttk.LabelFrame(frame_pe, text="Añadir")
        arriba.grid(padx=10, pady=10, row=0, column=0, sticky="nsew")
        ttk.Button(arriba,  text="Volver",image=imagen_volver,compound="left",width=36, command=lambda: volver_aulas(ver_aula)).grid(row=1, column=3, padx=2, pady=2)
        boton_de_eliminaraulas = tk.Button(arriba, text="Eliminar",width=250,image=imagen_eliminar,compound="left",fg="white",bg="#960000", command=lambda: opciones_aula(2)).grid(row=2, column=3, padx=2, pady=2)       
        clicked = tk.StringVar()
        
    
        menu_tipo_texto= ttk.Label(arriba, text="Tipo de aula:")
        menu_tipo_texto.grid(column=0, row=0, padx=5, pady=5)
        
        clicked2 = tk.StringVar()
        clicked2.set("Planta_alta")
        
        ttk.OptionMenu(arriba, clicked2, "Planta_alta", "Planta_baja", "Planta_alta").grid(column=1, row=1, padx=5, pady=5)
        
        
    
        
        menu_ubicacion_texto= ttk.Label(arriba, text="Ubicacion:")
        menu_ubicacion_texto.grid(column=1, row=0, padx=5, pady=5)
        
        laboratorio_numero= tk.IntVar()
        
        spinbox=ttk.Spinbox(arriba, width=10, textvariable=laboratorio_numero,from_=1,to=100,increment=1,validate="key", state="readonly")
        spinbox.grid(column=2, row=1, padx=5, pady=5)
        spinbox.set(1)

        
        entry_numero_texto= ttk.Label(arriba, text="Numero:")
        entry_numero_texto.grid(column=2, row=0, padx=5, pady=5)
        
        boton_de_agregaraulas = ttk.Button(arriba, text="Agregar", command=lambda:opciones_aula(1))
        boton_de_agregaraulas.grid(column=3, row=0, padx=5, pady=5)
        try:
            menu_tipo_laboratorio= [Tipo_aula,Tipo_aula]
            
            ttk.OptionMenu(arriba, clicked,*menu_tipo_laboratorio).grid(column=0, row=1, padx=5, pady=5)
        
        except:    
            menu_tipo_laboratorio= ["Laboratorio", "Aula", "Taller","Laboratorio"]
            ttk.OptionMenu(arriba, clicked,*menu_tipo_laboratorio).grid(column=0, row=1, padx=5, pady=5)
        frame_pe.columnconfigure(0, weight=1)
        frame_pe.rowconfigure(1, weight=1)
        treeview_aula.columnconfigure(0, weight=1)
        treeview_aula.rowconfigure(1, weight=1)
        arriba.rowconfigure(0, weight=1)
        for x in range(3):
            arriba.columnconfigure(x, weight=1)
        cerrar_base_de_datos()
    
        
   
  
def opciones_aula(option):
    conectar_base_de_datos()
    if option == 1:
        global nuevo_valor, valor_actual
            
        obtenertipo = (clicked.get())  
        obtenerubicacion = (clicked2.get())  
        obtenernumero = laboratorio_numero.get()
        if not obtenernumero:
            messagebox.showerror("Error", "Debe ingresar todos los datos.")
            return False         
        try:
            obtenernumero = int(obtenernumero)
        except ValueError:
            messagebox.showerror("Error", "El número debe ser un valor numérico.")
            return
        


        # Verificar si la fila ya existe en la base de datos
        select_query = "SELECT * FROM aulas WHERE Tipo_de_aula = %s AND Ubicacion = %s AND Numero = %s"
        data_verificar = (obtenertipo, obtenerubicacion, obtenernumero)
                
        cursor = cnx.cursor()
        cursor.execute(select_query, data_verificar)
        existing_row = cursor.fetchone()
            
        if existing_row:
            messagebox.showerror("Error", "La fila ya existe en la base de datos.")
            return     
        valor_actual = int(laboratorio_numero.get())
        if valor_actual >= 1 or valor_actual == 99:
            nuevo_valor = valor_actual + 1
            laboratorio_numero.set(nuevo_valor)
            insert_query = "INSERT INTO aulas (Tipo_de_aula, Ubicacion, Numero) VALUES (%s, %s, %s)"
            dataagregar = (obtenertipo, obtenerubicacion, obtenernumero)
                    
                    
            cursor = cnx.cursor()
            cursor.execute(insert_query, dataagregar)
            cnx.commit()  # Importante: Confirmar los cambios en la base de datos
                    
            cursor.close()
            cnx.close()
        
            messagebox.showinfo("Aviso", "Aula agregada correctamente")
            
            tree_aula.insert(parent='', index='end', values=(obtenertipo, obtenerubicacion, obtenernumero)) 
            cerrar_base_de_datos()
        else:
            messagebox.showerror("Error", "El número no puede ser mayor a 100 ni menor a 1")
            return False






        
        
    elif option==2:
        
        respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de eliminar estos datos?")
        if respuesta:
            conectar_base_de_datos()
            eleccion = tree_aula.selection()
            if not eleccion:
                messagebox.showerror("Error", "Seleccione al menos un aula")
            else:
                try:
                    cursor = cnx.cursor()
                    for ele in eleccion:
                        obtenertipo = tree_aula.item(ele, "values")
                        cursor.execute("DELETE FROM aulas WHERE Tipo_de_aula = %s AND Ubicacion = %s AND Numero = %s",(obtenertipo[0], obtenertipo[1], obtenertipo[2]))
                        tree_aula.delete(ele)
                    cnx.commit()
                    cursor.close()
            
                    if len(eleccion) == 1:
                        messagebox.showinfo("eliminar", "eliminado exitosamente")
                    else:
                        messagebox.showinfo("eliminar", f"{len(eleccion)} opciones eliminadas exitosamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
                finally:
                    cerrar_base_de_datos()

def ver_aula(columnas_aula,query):
    ver_aula = tk.Toplevel()
    conectar_base_de_datos()
    scrollbar = ttk.Scrollbar(ver_aula)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_aula = ttk.Treeview(ver_aula, yscrollcommand=scrollbar.set, selectmode="extended")
    tree_aula.pack(expand=True, fill="both")
    scrollbar.config(command=tree_aula.yview)
    
    tree_aula["columns"]=(columnas_aula)
    tree_aula.column("#0", width=0, stretch=tk.NO)
    for columna in columnas_aula:
        tree_aula.column(columna, anchor=tk.CENTER)
        tree_aula.heading(columna, text=columna)
    cursor.execute(query)
    data = cursor.fetchall()
    try:
        data.sort(key=lambda x: x[2])
    except IndexError:
        pass
    for index, values in enumerate(data):
        tree_aula.insert(parent='', index='end', iid=index, values=values)
    tree_aula.pack()
    cerrar_base_de_datos()
    
def conectar_base_de_datos():
    global cursor
    global cnx
    cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
    )
    # Crear un cursor para ejecutar consultas
    cursor = cnx.cursor()
def cerrar_base_de_datos():
    cursor.close()
    cnx.close()    
    
def volver_aulas(ventana):
    eliminar(ventana)
    botones_aulas(ventana,menufunc,tipodecuenta,nombrecuenta)

if __name__ == "__main__":
    tkw=tk.Tk()
    botones_aulas(tkw)
    tkw.mainloop()
