import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		

		self.text_var = tk.StringVar()
		self.text1 = tk.Text(
			self.Fenetre,
			font="TkDefaultFont", # malheureusement c'est du tk => pas de possibilité de changer avec Style=ttk.Style()
			height=15, #nb ligne
			width=60 # ? pas nb px, ni nb char sur la ligne
			)
		_text_ = "Texte par défaut à afficher initialement et modifiable. Peut être transmis depuis le main par \napp = Fenetre_simple(\"texte_a_afficher\")\napp.run()\n\n et dans la fonction \ndef __init__(_text_)"
		self.text1.insert("0.0", _text_)
		self.text1.pack() # largeur selon width
		# self.text1.pack(fill="x") # étiré sur toute la largeur

		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()