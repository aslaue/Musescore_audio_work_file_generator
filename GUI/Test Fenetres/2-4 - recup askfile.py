import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
import os
import sys

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')

		frame1 = ttk.Frame(self.Fenetre, padding = 30, borderwidth = 5, relief= 'groove', )
		
		frame2 = ttk.Frame(self.Fenetre, height = 200, padding = (60, 10), borderwidth = 5, relief= 'solid', )
		
		frame1.pack()
		frame2.pack(fill=tk.X,side=tk.BOTTOM)

		self.label1 = ttk.Label(frame1, text="Indiquer le nom du fichier")
		self.label1.pack()

		frame3 = ttk.Frame( frame1, height = 200, padding = (60, 10) )
		frame3.pack()
		frame3.columnconfigure(0, weight=1) 
		frame3.columnconfigure(1, weight=5) 

		self.text_var = tk.StringVar()

		self.textbox = ttk.Entry(frame3, textvariable=self.text_var)
		self.textbox.grid(row=0, column=0) # largeur selon width
		
		browse_button = ttk.Button(frame3, text='Browse ...', command=self.browse_btn_pressed)
		browse_button.grid(row=0, column=1)

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
		sys.exit()
	
	def get_modified_text(self):
		modified_text = self.textbox.get()
		self.text_var.set(modified_text)  # Met a jour la variable avec le texte modifie

	def browse_btn_pressed(self):
		if sys.platform=="linux":
			initial_path= os.environ["HOME"] + "/Documents"
		elif "win" in sys.platform:
			initial_path = os.environ["USERPROFILE"] + "/Documents"
		file = askopenfile(mode ='r', filetypes =[('Musescore Files', '.mscz')], title='Sélectionner le fichier de partition', initialdir=initial_path).name
		self.text_var.set(file)

	def run(self):
		self.mainwindow.mainloop()


app = Fenetre_simple()
app.run()
texte_input = app.text_var.get()
print(texte_input)