import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		
		self.label1 = ttk.Label(
			self.Fenetre,
			text="Texte packed, par défaut, rattaché à self.Fenetre",
			)
		self.label1.pack()
		self.label2 = ttk.Label(
			self.Fenetre,
			text="2è texte packed, par défaut, rattaché à self.Fenetre",
			)
		self.label2.pack()
		self.label3 = ttk.Label(
			self.Fenetre,
			text="texte packed side=tk.BOTTOM, rattaché à self.Fenetre",
			)
		self.label3.pack(side=tk.BOTTOM)
		
		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()