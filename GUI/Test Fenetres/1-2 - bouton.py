import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		exit_button_d = ttk.Button(
			self.Fenetre,
			text='Exit disabled',
			command=lambda: self.Fenetre.quit()
			)
		exit_button_d.state(['disabled'])
		exit_button_d.pack(
			ipadx=5,
			ipady=5,
			#expand=True
		)
		exit_button_e = ttk.Button(
			self.Fenetre,
			text='Exit enabled',
			command=lambda: self.Fenetre.quit()
			)
		exit_button_e.state(['!disabled'])
		exit_button_e.pack(
			ipadx=5,
			ipady=5,
			expand=True
		)
		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()
	def quit(self):
		self.Fenetre2.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()

app = Fenetre_simple()
app.run()