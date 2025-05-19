import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
    def __init__(self, str1, master=None):
        self.Fenetre = tk.Tk()
        self.Fenetre.title('Tkinter Window Demo')
        self.Fenetre.geometry('600x400+50+50')
        self.Fenetre.resizable(False, False)

        self.label1 = ttk.Label(
            self.Fenetre,
            text=str1,
            )
        self.label1.pack()        
                
        self.mainwindow = self.Fenetre
        
    def run(self)
        self.mainwindow.mainloop()

str1 = 'Texte à afficher'
app = Fenetre_simple(str1)
app.run()
