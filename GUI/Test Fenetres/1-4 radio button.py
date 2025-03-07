import tkinter as tk
from tkinter import ttk

class Fenetre_simple:
	def __init__(self, master=None):
		self.Fenetre = tk.Tk()
		self.Fenetre.title('Tkinter Window Demo')
		self.Fenetre.geometry('600x400+50+50')
		#self.Fenetre.resizable(False, False)

		style = ttk.Style()
		style.theme_use('alt')
		self.selected_option = tk.StringVar(value='1')
		options = (('option 1 disabled', '1'),
         ('option 2 disabled', '2'),
         ('option 3 disabled', '3'))

		for option in options:
			r = ttk.Radiobutton(
				self.Fenetre,
				text=option[0],
				value=option[1],
				state="disabled",
				variable=self.selected_option
    		)
			r.pack(fill='x', padx=5, pady=5)
		
		options = (('option 1', '1'),
         ('option 2', '2'),
         ('option 3', '3'))

		for option in options:
			r = ttk.Radiobutton(
				self.Fenetre,
				text=option[0],
				value=option[1],
				variable=self.selected_option
    		)
			r.pack(fill='x', padx=5, pady=5)


		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()
# list_selected_option = app.selected_option.get()
# print(list_selected_option)