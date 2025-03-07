import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		
		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()