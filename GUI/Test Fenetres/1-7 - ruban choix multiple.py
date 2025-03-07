import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def on_select(event, listbox):
		selected_indices = listbox.curselection()
		selected_options = [listbox.get(index) for index in selected_indices]

	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)
		
		options = ["option 1", "option 2", "option 3"]


		var = tk.Variable(value=options)

		self.listbox1 = tk.Listbox(
			self.Fenetre,
			listvariable=var,
			height=len(options),
			selectmode=tk.MULTIPLE
			# selectmode=tk.EXTENDED
		)
		self.listbox1.pack()
		self.listbox1.bind("<<ListboxSelect>>", lambda event: Fenetre_simple.on_select(event, self.listbox1))
		self.listbox1.selection_set(1)

		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()
	
	# def exit(self):
	# 	selected_indices = self.listbox1.curselection()
	# 	selected_options = []
	# 	for indice in selected_indices:
	# 		selected_options.append(self.listbox1.get(indice))



app = Fenetre_simple()
app.run()
# list_options = app.selected_options