"""
Librerias nesesarias:
pip install tk
pip install mysql-connector-python
pip install Pillow
pip install datetime
pip install tkcalendar
pip install win10toast
pip install FPDF
pip install ttkthemes
pip install qrcode
"""

from tkinter import *
from tkinter import ttk
from login import login1
from menu import menu1
import mysql.connector
from datetime import datetime
import os,sys
#ventana principal
tk=Tk()
tk.title("TecBoletines")
tk.geometry("1200x680")
tk.state('zoomed')
tk.minsize(1024, 600)

def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
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
    
login=login1()
menu=menu1(tk)

def cerrarSesion():
    login.crear(tk,menuFunc)
def menuFunc(tipoCuenta,nombreCuenta):
    menu.crear(tk, tipoCuenta, nombreCuenta, cerrarSesion, menuFunc)
login.crear(tk,menuFunc)

tk.mainloop()
