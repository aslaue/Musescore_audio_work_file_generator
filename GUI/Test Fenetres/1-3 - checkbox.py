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
		style.configure("style_1.TCheckbutton", font=("Arial", 16))  # Définir la police et la taille

		self.var_checkbox_d_t = tk.IntVar(value=1)
		self.var_checkbox_d_f = tk.IntVar(value=0)
		self.var_checkbox_e_t = tk.IntVar(value=1)
		self.var_checkbox_e_f = tk.IntVar(value=0)

		checkbox_d_t = ttk.Checkbutton(self.Fenetre,
				text='I agree (disabled, true)',
				#command=agreement_changed,
				state = "disabled",
				variable=self.var_checkbox_d_t, # initialement True
				style="style_1.TCheckbutton") #reprend le style alt mais avec la modif de style_1
		checkbox_d_t.pack()
		#
		checkbox_d_f = ttk.Checkbutton(self.Fenetre,
				text='I agree (disabled, false)',
				#command=agreement_changed,
				state = "disabled",
				variable=self.var_checkbox_d_f,
				style="style_1.TCheckbutton")
		checkbox_d_f.pack()
		#
		#	
		checkbox_e_t = ttk.Checkbutton(self.Fenetre,
				text='I agree (enabled, True)',
				#command=agreement_changed, #execute a function when change
				variable=self.var_checkbox_e_t,
				state = "enabled")
		checkbox_e_t.pack()
		#
		checkbox_e_f = ttk.Checkbutton(self.Fenetre,
				text='I agree (enabled, False)',
				#command=agreement_changed, #execute a function when change
				variable=self.var_checkbox_e_f,
				state = "enabled")
		checkbox_e_f.pack()

		self.mainwindow = self.Fenetre
		
	def run(self):
		self.mainwindow.mainloop()

app = Fenetre_simple()
app.run()