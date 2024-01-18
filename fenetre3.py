#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class DesignOutilMusescoreApp_fenetre3(tk.Toplevel):
	def on_select(event, listbox):
		selected_indices = listbox.curselection()
		selected_options = [listbox.get(index) for index in selected_indices]
		# print(f"Options sélectionnées : {selected_options}")
    
	def __init__(self, nom_voix, master=None):
		# build ui
		self.Fenetre3 = tk.Tk() if master is None else tk.Toplevel(master)
		self.Fenetre3.configure(
			background="#ffffff",
			borderwidth=5,
			height=1000,
			width=1500)
		self.Fenetre3.geometry("1500x1000")
		# ~ self.Fenetre3.maxsize(1500, 1000)
		# self.Fenetre3.minsize(15, 10)
		# ~ self.Fenetre3.resizable(False, False)
		self.Fenetre3.title("Outil transformation MuseScore")
		# import sys
		# self.Fenetre3.protocol("WM_DELETE_WINDOW", sys.exit())

		
		self.header3 = ttk.Frame(self.Fenetre3)
		self.header3.configure(height=200, width=200)
		label10 = ttk.Label(self.header3)
		label10.configure(text='Sélection du fichier')
		label10.grid(column=0, padx=5, row=0)
		label11 = ttk.Label(self.header3)
		label11.configure(text='identification des voix')
		label11.grid(column=1, padx=5, row=0)
		label12 = ttk.Label(self.header3)
		label12.configure(font="TkCaptionFont", text='Paramètres généraux')
		label12.grid(column=2, padx=5, row=0)
		label13 = ttk.Label(self.header3)
		label13.configure(text='Paramètres avancés')
		label13.grid(column=3, padx=5, row=0, sticky="new")
		self.header3.pack()
		self.corps3 = ttk.Frame(self.Fenetre3)
		# self.corps3.configure(height=200, width=200)
		text6 = tk.Text(self.corps3)
		text6.configure(
			background="#dbd9e4",
			height=3,
			insertunfocussed="none",
			setgrid=True,
			state="normal",
			tabstyle="wordprocessor",
			takefocus=True,
			wrap="word")
		_text_ = '- voix principale: 100%\n- autres voix: 20%\n- accompagnement: 60%'
		text6.insert("0.0", _text_)
		text6.grid(column=0, row=1)
		label15 = ttk.Label(self.corps3)
		label15.configure(
			text="Par défaut, l'outil génère chaque fichier voix avec les volumes suivants:\n")
		label15.grid(column=0, row=0, sticky="w")
		separator2 = ttk.Separator(self.corps3)
		separator2.configure(orient="vertical")
		separator2.grid(column=0, pady="2 2", row=2, sticky="nsew")
		frame11 = ttk.Frame(self.corps3)
		frame11.configure(height=200, width=200)
		label16 = ttk.Label(frame11)
		label16.configure(text='Personnalisation')
		label16.grid(column=0, row=0, sticky="w")
		self.label_vol_prin = ttk.Label(frame11)
		self.label_vol_prin.configure(text='Volume voix principale')
		self.label_vol_prin.grid(column=0, row=1)
		self.label_vol_autre = ttk.Label(frame11)
		self.label_vol_autre.configure(text='Volume autres voix')
		self.label_vol_autre.grid(column=0, row=2)
		self.vol_acc = ttk.Label(frame11)
		self.vol_acc.configure(text='volume accompagnement')
		self.vol_acc.grid(column=0, row=4)
		text2 = tk.Text(frame11)
		text2.configure(height=10, width=50, wrap="word")
		_text_ = "Sélectionner la/les voix d'accomagnement \n(ne rien cocher pour ne pas avoir d'accompagnement sur les audios des voix)\n"
		text2.insert("0.0", _text_)
		text2.grid(column=0, row=3)
		#
		self.box_vol_voix_prin_var = tk.StringVar()
		self.box_vol_voix_prin = ttk.Spinbox(frame11)
		self.box_vol_voix_prin.grid(column=1, row=1)
		self.box_vol_voix_prin.configure(textvariable=self.box_vol_voix_prin_var)
		#
		self.box_vol_voix_acc_var=tk.StringVar()
		self.box_vol_voix_acc = ttk.Spinbox(frame11)
		self.box_vol_voix_acc.grid(column=1, row=2)
		self.box_vol_voix_acc.configure(textvariable=self.box_vol_voix_acc_var)
		#
		self.listbox1 = tk.Listbox(frame11, selectmode=tk.MULTIPLE) #attention à utiliser self.listbox1 et pas juste listbox1, car sinon listbox1 est une variable temporaire liée à __init__
		self.listbox1.grid(column=1, row=3)
		for i in nom_voix:
			self.listbox1.insert(tk.END, i)
		self.listbox1.bind("<<ListboxSelect>>", lambda event: DesignOutilMusescoreApp_fenetre3.on_select(event, self.listbox1))
		#
		self.box_vol_voix_autre_var=tk.StringVar()
		self.box_vol_voix_autre = ttk.Spinbox(frame11)
		self.box_vol_voix_autre.configure(textvariable=self.box_vol_voix_autre_var)
		self.box_vol_voix_autre.grid(column=1, row=4)
		#
		frame11.grid(column=0, row=3, sticky="nsew")
		separator3 = ttk.Separator(self.corps3)
		separator3.configure(orient="vertical")
		separator3.grid(column=0, padx=5, row=4, sticky="nsew")
		frame15 = ttk.Frame(self.corps3)
		frame15.configure(height=200, width=200)
		#
		self.checkbutton1_var=tk.BooleanVar()
		self.checkbutton1 = ttk.Checkbutton(frame15)
		self.checkbutton1.configure(text='Créer un audio tutti ?')
		self.checkbutton1.configure(variable=self.checkbutton1_var)
		#
		self.checkbutton1.grid(column=0, row=0)
		text3 = tk.Text(frame15)
		text3.configure(height=4, width=70, wrap="word")
		_text_ = "En cochant l'option Paramètres avancés ci-dessous, il est alors possible d'affiner les réglages de volumes individuels (Work in progress: ainsi que la personalisation des noms de fichiers)"
		text3.insert("0.0", _text_)
		text3.grid(column=0, row=1, sticky="ew")
		#
		self.checkbutton2_var = tk.BooleanVar()
		self.checkbutton2 = ttk.Checkbutton(frame15)
		self.checkbutton2.configure(
			text='Activer les paramètres avancés (prochain panneau)')
		self.checkbutton2.configure(variable=self.checkbutton2_var)
		self.checkbutton2.grid(column=0, row=2)
		#
		frame15.grid(column=0, row=5)
		self.corps3.place(
			anchor="center",
			relwidth=1,
			relx=0.5,
			rely=0.5,
			x=0,
			y=0)
		frame9 = ttk.Frame(self.Fenetre3)
		frame9.configure(height=200, width=200)
		self.cancel3 = ttk.Button(frame9)
		self.cancel3.configure(text='Cancel')
		self.cancel3.grid(column=0, padx=5, row=0, sticky="e")
		self.cancel3.configure(command=self.btn_cancel)
		self.next3 = ttk.Button(frame9)
		self.next3.configure(text='Next')
		self.next3.grid(column=2, padx=5, row=0)
		self.next3.configure(command=self.btn_next)
		self.back3 = ttk.Button(frame9)
		self.back3.configure(text='Back')
		self.back3.grid(column=1, row=0)
		self.back3.configure(command=self.btn_back)
		frame9.place(anchor="se", relx=1, rely=1, x=0, y=0)

		# Main widget
		self.mainwindow = self.Fenetre3

	def run(self):
		self.mainwindow.mainloop()

	def btn_cancel(self):
		self.Fenetre3.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()



	def btn_next(self):#, widget_id):
		selected_indices = self.listbox1.curselection()
		self.selected_options = [self.listbox1.get(index) for index in selected_indices]
		# print(self.selected_options)
		self.Fenetre3.destroy()

	def btn_back(self, widget_id):
		pass
