import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, _text_, master=None):
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

		self.label1 = ttk.Label(frame1, text="Texte en grid, en position 0,0 \nrattaché à frame1 ")
		self.label1.pack()

		self.text_var = tk.StringVar()

		self.text1 = tk.Text(
			frame1,
			font="TkDefaultFont", # malheureusement c'est du tk => pas de possibilité de changer avec Style=ttk.Style()
			height=15, #nb ligne
			width=60 # ? pas nb px, ni nb char sur la ligne
			)
		# _text_ = "Texte par défaut à afficher initialement et modifiable. Peut être transmis depuis le main par \napp = Fenetre_simple(\"texte_a_afficher\")\napp.run()\n\n et dans la fonction \ndef __init__(_text_)"
		self.text1.insert("0.0", _text_)
		self.text1.pack() # largeur selon width
		

		cancel_button = ttk.Button(frame2,text='Cancel',command=self.cancel_btn_pressed)
		cancel_button.pack(padx=50,pady=5, expand=True, fill=tk.X, side=tk.LEFT)
		ok_button = ttk.Button(frame2, text='OK', command=self.ok_btn_pressed )
		ok_button.pack(padx=50, pady=5, expand=True, fill=tk.X, side=tk.LEFT )

		self.mainwindow = self.Fenetre
		
	def ok_btn_pressed(self):
		self.get_modified_text()
		self.Fenetre.destroy()

	def cancel_btn_pressed(self):
		self.Fenetre.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()
	
	def get_modified_text(self):
		modified_text = self.text1.get("1.0", tk.END)
		self.text_var.set(modified_text)  # Met a jour la variable avec le texte modifie

	def run(self):
		self.mainwindow.mainloop()


app = Fenetre_simple("texte à afficher")
app.run()
texte_input = app.text_var.get()
print(texte_input)