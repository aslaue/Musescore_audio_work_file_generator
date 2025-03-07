#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class DesignOutilMusescoreApp_fenetre4:
	def get_modified_text(self):
		modified_text = self.text1.get("1.0", tk.END)
		self.text_var.set(modified_text)  # Met a jour la variable avec le texte modifie
		
	def __init__(self, liste_des_voies, texte_matrix, master=None):
		# print("liste_des_voies",liste_des_voies)
		# build ui
		self.Fenetre4 = tk.Tk() if master is None else tk.Toplevel(master)
		self.Fenetre4.configure(
			background="#ffffff",
			borderwidth=5,
			height=500,
			width=1000)
		self.Fenetre4.geometry("1500x1000")
		# self.Fenetre4.maxsize(1000, 500)
		# self.Fenetre4.minsize(1000, 500)
		# self.Fenetre4.resizable(False, False)
		self.Fenetre4.title("Outil transformation MuseScore")
		frame16 = ttk.Frame(self.Fenetre4)
		frame16.configure(height=200, width=200)
		label21 = ttk.Label(frame16)
		label21.configure(text='Selection du fichier')
		label21.grid(column=0, padx=5, row=0)
		label22 = ttk.Label(frame16)
		label22.configure(text='identification des voix')
		label22.grid(column=1, padx=5, row=0)
		label23 = ttk.Label(frame16)
		label23.configure(text='Parametres generaux')
		label23.grid(column=2, padx=5, row=0)
		label24 = ttk.Label(frame16)
		label24.configure(font="TkCaptionFont", text='Parametres avances')
		label24.grid(column=3, padx=5, row=0, sticky="new")
		frame16.pack()
		frame5 = ttk.Frame(self.Fenetre4)
		frame5.configure(height=400, width=640)
		self.corps4 = ttk.Frame(frame5, name="corps4")
		self.corps4.configure(height=200, width=200)
		label25 = ttk.Label(self.corps4)
		label25.configure(text='Selon les choix de la page precedente, la matrice de volume est la suivante\n(chaque ligne correspond a un fichier audio)\nSi vous le souhaitez, vous pouvez modifier la matrice pour affiner les choix de volume \n(attention cependant a ne pas supprimer de ligne et de respecter les espacements sous forme de tab')
		label25.pack(side="top")
		label19 = ttk.Label(self.corps4)
		label19.configure(font="TkDefaultFont",text=liste_des_voies)
		label19.pack(fill="x", side="top")

		#
		self.text_var = tk.StringVar()
		self.text1 = tk.Text(self.corps4)
		self.text1.configure(font="TkDefaultFont",height=15, width=60)
		_text_ = texte_matrix
		self.text1.insert("0.0", _text_)
		self.text1.pack(fill="x", side="top")
		#
		self.corps4.pack(side="top")
		frame6 = ttk.Frame(frame5)
		frame6.configure(height=200, width=200)
		checkbutton3 = ttk.Checkbutton(frame6)
		self.delete_temp_folder = tk.BooleanVar()
		checkbutton3.configure(
			text='Supprimer le dossier temporaire et les fichiers musicxml en fin de processus ?',
			variable=self.delete_temp_folder)
		checkbutton3.pack(side="top")
		checkbutton4 = ttk.Checkbutton(frame6)
		self.clean_up_temp_folder = tk.BooleanVar()
		checkbutton4.configure(
			text='Supprimer les eventuels fichiers deja present dans le dossier temporaire ?',
			variable=self.clean_up_temp_folder)
		checkbutton4.pack(side="top")
		checkbutton5 = ttk.Checkbutton(frame6)
		self.clean_up_output_folder = tk.BooleanVar()
		checkbutton5.configure(
			text='Supprimer les eventuels fichiers deja presents dans le dossier output ?',
			variable=self.clean_up_output_folder)
		checkbutton5.pack(side="top")
		frame6.pack(expand=True, fill="x", side="top")
		#
		# frame10 = ttk.Frame(frame5)
		# frame10.configure(height=50, width=200)
		# label20 = ttk.Label(frame10)
		# label20.configure(text='texte a completer nom fichier ')
		# label20.pack(side="top")
		# entry2 = ttk.Entry(frame10) # ne s'affiche pas ??
		# self.nom_fichier_autre = tk.StringVar()
		# entry2.configure(textvariable=self.nom_fichier_autre)
		# frame10.pack(fill="x", pady=5, side="top")
		#
		frame5.pack(pady=10, side="top")
		frame17 = ttk.Frame(self.Fenetre4)
		frame17.configure(height=200, width=200)
		self.cancel4 = ttk.Button(frame17, name="cancel4")
		self.cancel4.configure(text='Cancel')
		self.cancel4.grid(column=0, padx=5, row=0, sticky="e")
		self.cancel4.configure(command=self.btn_cancel)
		self.Finish4 = ttk.Button(frame17, name="finish4")
		self.Finish4.configure(text='Finish')
		self.Finish4.grid(column=2, padx=5, row=0)
		self.Finish4.configure(command=self.btn_finish)
		self.back4 = ttk.Button(frame17, name="back4")
		self.back4.configure(text='Back')
		self.back4.grid(column=1, row=0)
		self.back4.configure(command=self.btn_back)
		frame17.place(anchor="se", relx=1, rely=1, x=0, y=0)

		# Main widget
		self.mainwindow = self.Fenetre4

	def run(self):
		self.mainwindow.mainloop()

	def btn_cancel(self):
		self.Fenetre4.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()
		pass

	def btn_finish(self):
		self.get_modified_text()
		self.Fenetre4.destroy()
		pass

	def btn_back(self):
		pass


# if __name__ == "__main__":
    # app = DesignOutilMusescoreApp_fenetre4()
    # app.run()
