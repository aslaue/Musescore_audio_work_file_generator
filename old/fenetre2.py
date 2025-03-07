import tkinter as tk
import tkinter.ttk as ttk
# from fenetre3 import DesignOutilMusescoreApp_fenetre3

taille_fenetre_x = 1000
taille_fenetre_y = 1000

saved_option=[]
class DesignOutilMusescoreApp_fenetre2:
	def __init__(self, measure_nb, id_voix, nom_voix, texte_mis_en_page_voix, master=None):
		# build ui
		self.Fenetre2 = tk.Tk() if master is None else tk.Toplevel(master)
		self.Fenetre2.configure(
			background="#ffffff",
			borderwidth=5,
			height=500,
			width=1000)
		self.Fenetre2.geometry("1500x1000")
		# ~ self.Fenetre2.maxsize(1000, 500)
		# self.Fenetre2.minsize(taille_fenetre_x, taille_fenetre_y)
		# ~ self.Fenetre2.resizable(False, False)
		self.Fenetre2.title("Outil transformation MuseScore")
		frame4 = ttk.Frame(self.Fenetre2)
		frame4.configure(height=200, width=200)
		label6 = ttk.Label(frame4)
		label6.configure(text='Sélection du fichier')
		label6.grid(column=0, padx=5, row=0)
		label7 = ttk.Label(frame4)
		label7.configure(font="TkCaptionFont", text='identification des voix')
		label7.grid(column=1, padx=5, row=0)
		label8 = ttk.Label(frame4)
		label8.configure(text='Paramètres généraux')
		label8.grid(column=2, padx=5, row=0)
		label9 = ttk.Label(frame4)
		label9.configure(text='Paramètres avancés')
		label9.grid(column=3, padx=5, row=0, sticky="new")
		frame4.pack()
		frame7 = ttk.Frame(self.Fenetre2)
		frame7.configure(height=200, width=200)
		self.cancel2 = ttk.Button(frame7)
		self.cancel2.configure(text='Cancel')
		self.cancel2.grid(column=0, padx=5, row=0, sticky="e")
		self.cancel2.configure(command=self.btn_cancel)
		self.next2 = ttk.Button(frame7)
		self.next2.configure(text='Next')
		self.next2.grid(column=2, padx=5, row=0)
		self.next2.configure(command=lambda: self.btn_next(nom_voix))
		self.back2 = ttk.Button(frame7)
		self.back2.configure(text='Back')
		self.back2.grid(column=1, row=0)
		self.back2.configure(command=self.btn_back)
		frame7.place(anchor="se", relx=1, rely=1, x=0, y=0)
		frame8 = ttk.Frame(self.Fenetre2)
		frame8.configure(height=200, width=200)
		label14 = ttk.Label(frame8)
		label14.configure(
			text='Le programme a détecté un total de {} mesures et {} voix dans le fichier\n'.format(measure_nb, len(id_voix)))
		label14.pack(side="top")
		text1 = tk.Text(frame8)
		text1.configure(height=10, width=50)
		# _text_ = 'Texte à automatiser'
		_text_ = texte_mis_en_page_voix
		text1.insert("0.0", _text_)
		text1.pack(side="top")
		frame8.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)

		# Main widget
		self.mainwindow = self.Fenetre2

	def run(self):
		self.mainwindow.mainloop()

	def btn_cancel(self):
		self.Fenetre2.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()
		pass

	def btn_next(self, nom_voix):#, widget_id):
		self.Fenetre2.destroy()
		# fenetre3=DesignOutilMusescoreApp_fenetre3(nom_voix)
		# fenetre3.run()
		
		# DesignOutilMusescoreApp_fenetre3(nom_voix)
		# print("ok")
		# print(DesignOutilMusescoreApp_fenetre3().selected_options)
		# self.data_from_fenetre3 = DesignOutilMusescoreApp_fenetre3().get_data()
		# print(self.data_from_fenetre3)
		
		pass

	def btn_back(self):
		pass

if __name__ == "__main__":
	print("ok")
	app = DesignOutilMusescoreApp_fenetre2()
	app.run()
