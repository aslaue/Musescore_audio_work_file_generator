import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		# self.Fenetre.resizable(False, False)
		
		# self.Fenetre.columnconfigure(1, weight=1) # la colonne 1 est 2x plus grosse que les autres
		# self.Fenetre.rowconfigure(2, weight=1) # la ligne 2 est 3x plus grande que les autres

		self.label1 = ttk.Label(
			self.Fenetre,
			text="Texte en grid, en position 0,0 \nrattaché à Fenêtre avec padx=5, pady=5",
			)
		self.label1.grid(column=0,row=0, padx=5, pady=5)
		self.label2 = ttk.Label(
			self.Fenetre,
			text="Texte en grid, en position 3,3 rattaché à Fenêtre avec padx=30, pady=15",
			)
		self.label2.grid(column=3,row=3, padx=30, pady=15)
		self.label3 = ttk.Label(
			self.Fenetre,
			text="Texte en grid, en position 1,1 rattaché à Fenêtre",
			)
		self.label3.grid(column=1,row=1)
		self.label4 = ttk.Label(
			self.Fenetre,
			text="Texte en grid, en position 2,2 rattaché à Fenêtre",
			)
		self.label4.grid(column=2,row=2)

		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()