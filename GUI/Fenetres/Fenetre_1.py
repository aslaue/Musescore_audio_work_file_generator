import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
import os
import sys

class Fenetre_1:
	def __init__(self, GUI_parameters, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry(GUI_parameters["window_definition"])

		frame1 = ttk.Frame(self.Fenetre, padding = 30, borderwidth = 5, relief= 'groove', )
		
		frame2 = ttk.Frame(self.Fenetre, height = 200, padding = (60, 10), borderwidth = 5, relief= 'solid', )
		
		frame1.pack()
		frame2.pack(fill=tk.X,side=tk.BOTTOM)

		self.label1 = ttk.Label(frame1, text="Indiquer le nom du fichier partition mscz")
		self.label1.pack()

		frame3 = ttk.Frame( frame1, height = 200, padding = (60, 10) )
		frame3.pack()
		frame3.columnconfigure(0, weight=1) 
		frame3.columnconfigure(1, weight=5) 

		self.mscz_file_var = tk.StringVar()

		self.textbox_1 = ttk.Entry(frame3, textvariable=self.mscz_file_var)
		self.textbox_1.grid(row=0, column=0) # largeur selon width
		
		browse_1_button = ttk.Button(frame3, text='Browse ...', command=self.browse_1_btn_pressed)
		browse_1_button.grid(row=0, column=1)

		# json
		self.label2 = ttk.Label(frame1, text="WIP - Indiquer le nom du fichier de paramètre JSON (laisser vide s'il n'y en a pas)")
		self.label2.pack()

		frame4 = ttk.Frame( frame1, height = 200, padding = (60, 10) )
		frame4.pack()
		frame4.columnconfigure(0, weight=1) 
		frame4.columnconfigure(1, weight=5)

		self.json_file_var = tk.StringVar()

		self.textbox_2 = ttk.Entry(frame4, textvariable=self.json_file_var)
		self.textbox_2.grid(row=0, column=0) # largeur selon width

		browse_2_button = ttk.Button(frame4, text='Browse ...', command=self.browse_2_btn_pressed)
		browse_2_button.grid(row=0, column=1)

		cancel_button = ttk.Button(frame2,text='Cancel',command=self.cancel_btn_pressed)
		cancel_button.pack(padx=50,pady=5, expand=True, fill=tk.X, side=tk.LEFT)

		ok_button = ttk.Button(frame2, text='OK', command=self.ok_btn_pressed )
		ok_button.pack(padx=50, pady=5, expand=True, fill=tk.X, side=tk.LEFT )

		# self.Fenetre.bind("<Escape>", self.cancel_btn_pressed) # pas réussi à faire fonctionner

		self.mainwindow = self.Fenetre
		
	def ok_btn_pressed(self):
		self.get_modified_text()
		self.Fenetre.destroy()

	def cancel_btn_pressed(self):
		self.Fenetre.destroy()
		print("bouton cancel presse, arret du programme")
		sys.exit()
	
	def get_modified_text(self):
		modified_text = self.textbox_1.get()
		self.mscz_file_var.set(modified_text)  # Met a jour la variable avec le texte modifie

	def browse_1_btn_pressed(self):
		if sys.platform=="linux":
			initial_path= os.environ["HOME"] + "/Documents"
		elif "win" in sys.platform:
			initial_path = os.environ["USERPROFILE"] + "/Documents"
		file = askopenfile(mode ='r', filetypes =[('Musescore Files', '.mscz')], title='Sélectionner le fichier de partition', initialdir=initial_path).name
		self.mscz_file_var.set(file)
	
	def browse_2_btn_pressed(self):
		if sys.platform=="linux":
			initial_path= os.environ["HOME"] + "/Documents"
		elif "win" in sys.platform:
			initial_path = os.environ["USERPROFILE"] + "/Documents"
		file = askopenfile(mode ='r', filetypes =[('JSON Files', '.json')], title='Sélectionner le fichier de paramètre', initialdir=initial_path).name
		self.json_file_var.set(file)

	def run(self):
		self.mainwindow.mainloop()


# app = Fenetre_simple()
# app.run()
# texte_input = app.mscz_file_var.get()
# print(texte_input)