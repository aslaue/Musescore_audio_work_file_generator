import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		frame1 = ttk.Frame(
			self.Fenetre,
			padding = 30,
			borderwidth = 5,
			relief= 'groove',
		)
		
		frame2 = ttk.Frame(
			self.Fenetre, 
			height = 200,
			padding = (60, 10),
			borderwidth = 5,
			relief= 'solid',
		)
		
		frame1.pack()
		frame2.pack(fill=tk.X,side=tk.BOTTOM)

		self.label1 = ttk.Label(
			frame1,
			text="Texte en grid, en position 0,0 \nrattaché à frame1 ",
			)
		self.label1.grid(column=0,row=0)
		self.label2 = ttk.Label(
			frame1,
			text="Texte en grid, en position 2,2 rattaché à frame1 avec padx=30, pady=15",
			)
		self.label2.grid(column=2,row=2, padx=30, pady=15)
		self.label3 = ttk.Label(
			frame1,
			text="Texte en grid, en position 1,1 rattaché à frame1",
			)
		self.label3.grid(column=1,row=1)
		

		cancel_button = ttk.Button(
			frame2,
			text='Cancel',
			command=lambda: self.Fenetre.quit()
		)
		cancel_button.pack(
			padx=50,
			pady=5,
			expand=True,
			fill=tk.X,
			side=tk.LEFT
		)
		ok_button = ttk.Button(
			frame2,
			text='OK',
			command=lambda: self.Fenetre.ok()
		)
		ok_button.pack(
			padx=50,
			pady=5,
			expand=True,
			fill=tk.X,
			side=tk.LEFT
		)

		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

	def quit(self):
		self.Fenetre.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()

	def ok(self):
		self.Fenetre.destroy()

app = Fenetre_simple()
app.run()