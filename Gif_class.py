import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GifPlayer(tk.Label):
    def __init__(self, master, gif_path):
        tk.Label.__init__(self, master)
        
        # Cargar la imagen GIF
        self.gif = Image.open(gif_path)
        self.frames = []
        
        try:
            while True:
                frame = ImageTk.PhotoImage(self.gif.copy())
                self.frames.append(frame)
                self.gif.seek(len(self.frames))  # Mover al siguiente frame
        except EOFError:
            pass  # Fin del archivo GIF
        
        self.frame_index = 0
        self.update_gif()
    
    def update_gif(self):
        frame = self.frames[self.frame_index]
        self.configure(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.update_gif)  # Cambiar el frame cada 100 ms (ajustar según la velocidad deseada)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GIF en Tkinter")
    
    gif_path = "Imagenes/Qr_scan.gif"  # Reemplazar con la ruta de tu GIF
    player = GifPlayer(root, gif_path)
    player.pack()
    
    root.mainloop()
