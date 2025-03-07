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

		self.label1 = ttk.Label(frame1, text="choix à choisir ")
		self.label1.pack()

		options = ["option 1", "option 2", "option 3"]

		self.var = tk.Variable(value=options)

		self.listbox1 = tk.Listbox(
			self.Fenetre,
			listvariable=self.var,
			height=len(options),
			selectmode=tk.MULTIPLE
			# selectmode=tk.EXTENDED
		)
		self.listbox1.pack()
		self.listbox1.bind("<<ListboxSelect>>", lambda event: Fenetre_simple.on_select(event, self.listbox1))
		self.listbox1.selection_set(1)
				

		cancel_button = ttk.Button(frame2,text='Cancel',command=self.cancel_btn_pressed)
		cancel_button.pack(padx=50,pady=5, expand=True, fill=tk.X, side=tk.LEFT)
		ok_button = ttk.Button(frame2, text='OK', command=self.ok_btn_pressed )
		ok_button.pack(padx=50, pady=5, expand=True, fill=tk.X, side=tk.LEFT )

		self.mainwindow = self.Fenetre
		
	def ok_btn_pressed(self):
		selected_indices = self.listbox1.curselection()
		self.selected_options = []
		for indice in selected_indices:
			self.selected_options.append(self.listbox1.get(indice))
		self.Fenetre.destroy()

	def cancel_btn_pressed(self):
		self.Fenetre.destroy()
		print("bouton cancel presse, arret du programme")
		import sys
		sys.exit()
	
 # Met a jour la variable avec le texte modifie

	def run(self):
		self.mainwindow.mainloop()

	def on_select(event, listbox):
		selected_indices = listbox.curselection()
		selected_options = [listbox.get(index) for index in selected_indices]


app = Fenetre_simple()
app.run()
texte_input = app.selected_options
print(texte_input)