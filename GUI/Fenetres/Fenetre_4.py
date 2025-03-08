import tkinter as tk
from tkinter import ttk

class Fenetre_4:
	def __init__(self,GUI_parameters, list_matrix, intitule_lignes_matrix, intitule_colonne_matrix, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry(GUI_parameters["window_definition"])
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

		str_label1 = ""
		for k,line in enumerate(intitule_colonne_matrix):
			for i in range(k):
				str_label1+="|    "
			str_label1+= line + "\n"
		for i in range(k+1):
			str_label1+="|    "
		self.label1 = ttk.Label(frame1, text=str_label1)
		self.label1.grid(row=1,column=1, sticky=tk.SW, padx=5)

		self.text_var = tk.StringVar()

		self.text1 = tk.Text(
			frame1,
			font="TkDefaultFont", # malheureusement c'est du tk => pas de possibilité de changer avec Style=ttk.Style()
			height=len(list_matrix), #nb ligne
			width=60 # ? pas nb px, ni nb char sur la ligne
			)
		# _text_ = "Texte par défaut à afficher initialement et modifiable. Peut être transmis depuis le main par \napp = Fenetre_simple(\"texte_a_afficher\")\napp.run()\n\n et dans la fonction \ndef __init__(_text_)"
		
		str_matrix = ""
		for line in list_matrix:
			str_matrix+= line + "\n"
		self.text1.insert("0.0", str_matrix)
		self.text1.grid(row=2, column=1, sticky=tk.NW) # largeur selon width

		str_label2 = ""
		for line in intitule_lignes_matrix:
			str_label2+= line + "\n"
		self.label2 = ttk.Label(frame1, text=str_label2, justify=tk.RIGHT)
		self.label2.grid(row=2,column=0, sticky= tk.NE, pady=2, padx=5)

		str_label3 = "Dans cette fenêtre, il vous est possible d'affiner les réglages de volumes pour chacun des fichier audio.\n" \
			"Chaque ligne correspond à un fichier audio et chaque colonne correspond à une voix.\n"
		self.label3 = ttk.Label(frame1, text=str_label3)
		self.label3.grid(row=0,column=0, columnspan=2)
		

		cancel_button = ttk.Button(frame2,text='Cancel',command=self.cancel_btn_pressed)
		cancel_button.pack(padx=50,pady=5, expand=True, fill=tk.X, side=tk.LEFT)
		ok_button = ttk.Button(frame2, text='OK', command=self.ok_btn_pressed )
		ok_button.pack(padx=50, pady=5, expand=True, fill=tk.X, side=tk.LEFT )

		self.Fenetre.protocol("WM_DELETE_WINDOW", self.cancel_btn_pressed) # si on ferme la fenêtre avec le bouton de fermeture en haut à droite, le main s'arrête aussi

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


# app = Fenetre_simple("texte à afficher")
# app.run()
# texte_input = app.text_var.get()
# print(texte_input)