import tkinter as tk
import mysql.connector
from tkinter import messagebox,ttk

def conectar_base_de_datos():
    global cursor, cnx
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='tecnica_2023'
    )
    cursor = cnx.cursor()

def cerrar_base_de_datos():
    cursor.close()
    cnx.close()

def eliminar_usuarios2():
    conectar_base_de_datos()
    try:
        cursor.execute("SELECT Usuario, Contraseña, Admin FROM usuarios")
        data = cursor.fetchall()
        Ver_usuarios = tk.Toplevel()
        Ver_usuarios.title("Profesores")
        Ver_usuarios.minsize(1000, 400)

        ttk.Label(Ver_usuarios, text="Elegir usuarios a eliminar:").grid(padx=10, pady=10, row=0, column=0)

        treeview_Profe = ttk.Labelframe(Ver_usuarios, text="Profesores")
        treeview_Profe.grid(padx=10, pady=10, row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(treeview_Profe)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree_usu = ttk.Treeview(treeview_Profe, yscrollcommand=scrollbar.set, selectmode="extended")
        tree_usu.pack(expand=True, fill="both")
        scrollbar.config(command=tree_usu.yview)

        tree_usu["columns"] = ("Usuario", "Contraseña", "Admin")
        tree_usu.column("#0", width=0, stretch=0)
        tree_usu.column("Usuario", anchor="n", width=200)
        tree_usu.column("Contraseña", anchor="center", width=200)
        tree_usu.column("Admin", anchor="center", width=200)

        for columna in ("Usuario", "Contraseña", "Admin"):
            tree_usu.column(columna, anchor="center")
            tree_usu.heading(columna, text=columna)

        for index, values in enumerate(data):
            tree_usu.insert(parent='', index='end', iid=index, values=values)

        tree_usu.pack()

        ttk.Button(Ver_usuarios, text="Eliminar", command=lambda: eliminar(tree_usu)).grid(column=0, row=2, padx=5, pady=5, sticky="nsew")

        Ver_usuarios.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    finally:
        cerrar_base_de_datos()

def eliminar(tree_usu):
    conectar_base_de_datos()
    eleccion = tree_usu.selection()
    if not eleccion:
        messagebox.showerror("Error", "Seleccione al menos un usuario")
    else:
        try:
            cursor = cnx.cursor()
            for ele in eleccion:
                usuario = tree_usu.item(ele, "values")[0]
                cursor.execute("DELETE FROM usuarios WHERE Usuario = %s", (usuario,))
                tree_usu.delete(ele)
            cnx.commit()
            cursor.close()
            messagebox.showinfo("Usuarios eliminados", f"{len(eleccion)} Usuarios exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
        finally:
            cerrar_base_de_datos()