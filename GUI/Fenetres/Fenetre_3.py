"""
3. volume    
    1. volume des voix secondaires
    2. volume de l'accompagnement
"""
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
import os
import sys

class Fenetre_3:
    def __init__(self, GUI_parameters,list_voix_accompagnement, master=None):
        self.Fenetre = tk.Tk()
        self.Fenetre.title('Tkinter Window Demo')
        self.Fenetre.geometry(GUI_parameters["window_definition"])

        frame1 = ttk.Frame(self.Fenetre, padding = 30, borderwidth = 5, relief= 'groove', )

        frame2 = ttk.Frame(self.Fenetre, height = 200, padding = (60, 10), borderwidth = 5, relief= 'solid', )

        frame1.pack()
        frame2.pack(fill=tk.X,side=tk.BOTTOM)

        self.label1 = ttk.Label(frame1, text="Indiquer le volume des voix secondaires")
        self.label1.grid(row=0,column=0, padx=10, pady=10)

        self.volume_voix_sec = tk.StringVar()

        self.textbox_1 = ttk.Entry(frame1, textvariable=self.volume_voix_sec)
        self.textbox_1.grid(row=0, column=1, padx=10, pady=10) # largeur selon width


        self.volume_voix_acc = tk.StringVar()

        self.textbox_2 = ttk.Entry(frame1, textvariable=self.volume_voix_acc)
        self.textbox_2.grid(row=1, column=1, padx=10, pady=10) # largeur selon width

        if len(list_voix_accompagnement)==0:
            self.textbox_2.config(state="disabled")
            label2_str = "Indiquer le volume des voix d'accompagnement\nedit: il n'y a pas de voix d'accompagnement, option désactivée"
        else:
            label2_str = "Indiquer le volume des voix d'accompagnement"
        
        self.label2 = ttk.Label(frame1, text=label2_str)
        self.label2.grid(row=1,column=0, padx=10, pady=10)

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
        modified_text = self.textbox_1.get()
        self.volume_voix_sec.set(modified_text)  # Met a jour la variable avec le texte modifie
        modified_text = self.textbox_2.get()
        self.volume_voix_acc.set(modified_text)  # Met a jour la variable avec le texte modifie

    def run(self):
        self.mainwindow.mainloop()