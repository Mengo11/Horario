import tkinter as tk
from tkinter import ttk

def eliminar(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def volver_docentes(ventana):
    ventana.destroy()

def filtrar_asistencias(tree, filtro):
    """Filtra las filas del Treeview por el número de legajo proporcionado."""
    for item in tree.get_children():
        tree.delete(item)

    # Datos de ejemplo
    datos_ejemplo = [
        (1, "12345", "2024-12-01", "08:00", "08:05", "Sí", "No", "N/A", "16:00", "No", "No"),
        (2, "67890", "2024-12-01", "08:00", "08:10", "Sí", "Sí", "Médico", "16:00", "No", "No"),
        (3, "23456", "2024-12-01", "08:15", "08:20", "No", "No", "N/A", "16:00", "Sí", "No"),
        (4, "78901", "2024-12-01", "08:30", "08:35", "Sí", "No", "N/A", "16:00", "Sí", "Sí"),
        (5, "11223", "2024-12-01", "08:00", "08:05", "Sí", "Sí", "Médico", "16:00", "No", "No"),
    ]

    # Filtrar datos
    if filtro:
        datos_filtrados = [fila for fila in datos_ejemplo if filtro in fila[1]]
    else:
        datos_filtrados = datos_ejemplo

    # Insertar datos filtrados
    for index, values in enumerate(datos_filtrados):
        tree.insert(parent="", index="end", iid=index, values=values)

def ver_asistencias(ver_Asistencias, eliminar_b):
    global tree_Asistencia, frame_pe_asistencia

    if eliminar_b == 1:
        eliminar(ver_Asistencias)
        frame_pe_asistencia = ttk.Frame(ver_Asistencias)
        frame_pe_asistencia.place(x=0, y=0, relwidth=1, relheight=1)

    # Configuración de la ventana
    ver_Asistencias.title("Asistencias")

    # Botón "Volver" separado y en la parte superior
    frame_volver = ttk.Frame(frame_pe_asistencia)
    frame_volver.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    ttk.Button(
        frame_volver,
        text="Volver",
        command=lambda: volver_docentes(ver_Asistencias),
    ).grid(row=0, column=0, padx=5, pady=5)

    # Frame para los filtros
    frame_filtros = ttk.Frame(frame_pe_asistencia)
    frame_filtros.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Etiqueta y entrada de filtro
    ttk.Label(frame_filtros, text="Filtrar por Número de Legajo:").grid(row=0, column=0, padx=5, pady=5)
    filtro_entrada = ttk.Entry(frame_filtros)
    filtro_entrada.grid(row=0, column=1, padx=5, pady=5)

    # Botón de filtrar
    ttk.Button(
        frame_filtros,
        text="Filtrar",
        command=lambda: filtrar_asistencias(tree_Asistencia, filtro_entrada.get()),
    ).grid(row=0, column=2, padx=5, pady=5)

    # Botón "Quitar Filtro"
    ttk.Button(
        frame_filtros,
        text="Quitar Filtro",
        command=lambda: [filtro_entrada.delete(0, tk.END), filtrar_asistencias(tree_Asistencia, "")],
    ).grid(row=0, column=3, padx=5, pady=5)

    # Frame del Treeview
    treeview_Asistencia = ttk.Frame(frame_pe_asistencia)
    treeview_Asistencia.grid(padx=10, pady=10, row=2, column=0, sticky="nsew")

    # Scrollbars
    scrollbar_y = ttk.Scrollbar(treeview_Asistencia)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_x = ttk.Scrollbar(treeview_Asistencia, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Configuración del Treeview
    tree_Asistencia = ttk.Treeview(
        treeview_Asistencia,
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
        selectmode="extended",
    )
    tree_Asistencia.pack(expand=True, fill="both")

    # Asignar scrollbars al Treeview
    scrollbar_y.config(command=tree_Asistencia.yview)
    scrollbar_x.config(command=tree_Asistencia.xview)

    # Definir las columnas
    columnas_asistencias = (
        "ID",
        "Num_legajo",
        "Fecha",
        "Hora_entrada",
        "Horario_llegada",
        "Llegada_tarde",
        "Justificado",
        "Tipo_justificacion",
        "Hora_retiro",
        "Retiro",
        "Inasistencia",
    )

    tree_Asistencia["columns"] = columnas_asistencias
    tree_Asistencia.column("#0", width=0, stretch=0)

    for columna in columnas_asistencias:
        tree_Asistencia.column(columna, anchor="center", width=100)
        tree_Asistencia.heading(columna, text=columna)

    # Insertar todos los datos inicialmente
    filtrar_asistencias(tree_Asistencia, filtro="")

    # Configuración de pesos para ajustar el diseño
    treeview_Asistencia.columnconfigure(0, weight=1)
    treeview_Asistencia.rowconfigure(1, weight=1)
    frame_pe_asistencia.columnconfigure(0, weight=1)
    frame_pe_asistencia.rowconfigure(2, weight=1)

# Prueba de la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba Ver Asistencias")
    root.geometry("900x600")
    ver_asistencias(root, eliminar_b=1)
    root.mainloop()
