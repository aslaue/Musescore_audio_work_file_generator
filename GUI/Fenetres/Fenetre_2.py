import tkinter as tk
from tkinter import ttk

# """
# 2. Voix détectées 
#     1. voix d'accompagnement
#     2. WIP - voix à faire entendre dans l'audio et pour laquelle ne pas générer de fichier audio
#     3. WIP - Voulez-vous créer un fichier tutti ?
# """

class Fenetre_2:
    def __init__(self,GUI_parameters, list_voices, master=None):
        self.Fenetre = tk.Tk()
        self.Fenetre.title('Fenêtre 2 - Sélection des paramètres généraux')
        self.Fenetre.geometry(GUI_parameters["window_definition"])
        #self.Fenetre.resizable(False, False)
        frame1 = ttk.Frame( self.Fenetre, padding = 30, borderwidth = 5, relief= 'groove')
        frame2 = ttk.Frame( self.Fenetre,  height = 200, padding = (60, 10), borderwidth = 5, relief= 'solid', )

        frame1.pack()
        frame2.pack(fill=tk.X,side=tk.BOTTOM)
        ## frame_1
        self.label1 = ttk.Label(frame1, text="choix à choisir ")
        self.label1.pack()

        frame3 = ttk.Frame( frame1, padding = 30 )
        frame3.pack()

        self.label2 = ttk.Label(frame3, text="Indiquer dans la liste ci-contre les voix d'accompagnement\n(Les voix d'accompagnement auront un volume spécial, ne seront pas séparées et n'auront pas de fichier de travail généré)")
        self.label2.grid(column=0,row=0,padx=10,pady=10)

        options = list_voices
        # print(options)
        self.var = tk.Variable(value=options)
        self.listbox1 = tk.Listbox( frame3, listvariable=self.var, height=len(options), selectmode=tk.MULTIPLE ) # selectmode=tk.EXTENDED
        self.listbox1.grid(column=1,row=0, padx=10,pady=10)
        # self.listbox1.bind("<<ListboxSelect>>", lambda event: Fenetre_simple.on_select(event, self.listbox1))
        # self.listbox1.selection_set(1)

        self.label3 = ttk.Label(frame3, text="WIP - Indiquer dans la liste ci-contre les voix qui (en plus des voix d'accompagnement) n'auront pas de fichier de travail généré\nproblème autre: Il n'est pas possible d'avoir 2 listes à choix multiple sur la même fenêtre, sélectionner à 1 endroit annule l'autre")
        self.label3.grid(column=0,row=1,padx=10,pady=10)

        self.var_2 = tk.Variable(value=options)
        self.listbox2 = tk.Listbox( frame3, listvariable=self.var_2, height=len(options), selectmode=tk.MULTIPLE ) # selectmode=tk.EXTENDED
        self.listbox2.grid(column=1,row=1, padx=10,pady=10)
        self.listbox2.config(state=tk.DISABLED)


        frame4 = ttk.Frame( frame1, padding = 30 )
        frame4.pack()

        style = ttk.Style()
        style.theme_use('alt')
        self.var_checkbox_gen_tutti = tk.IntVar(value=1)

        checkbox_gen_tutti = ttk.Checkbutton(self.Fenetre,
            text='WIP - Voulez-vous créer un fichier tutti ?',
            state = "disabled",
            variable=self.var_checkbox_gen_tutti, # initialement True
        )
        checkbox_gen_tutti.pack()

        ## frame 2
        cancel_button = ttk.Button(frame2,text='Cancel',command=self.cancel_btn_pressed)
        cancel_button.pack(padx=50,pady=5, expand=True, fill=tk.X, side=tk.LEFT)
        ok_button = ttk.Button(frame2, text='OK', command=self.ok_btn_pressed )
        ok_button.pack(padx=50, pady=5, expand=True, fill=tk.X, side=tk.LEFT )

        self.Fenetre.protocol("WM_DELETE_WINDOW", self.cancel_btn_pressed) # si on ferme la fenêtre avec le bouton de fermeture en haut à droite, le main s'arrête aussi

        self.mainwindow = self.Fenetre
        
    def ok_btn_pressed(self):
        selected_indices = self.listbox1.curselection()
        self.selected_options = []
        for indice in selected_indices:
            self.selected_options.append(self.listbox1.get(indice))
        #
        selected_indices_2 = self.listbox2.curselection()
        self.selected_options_2 = []
        for indice in selected_indices_2:
            self.selected_options_2.append(self.listbox2.get(indice))
        self.Fenetre.destroy()

    def cancel_btn_pressed(self):
        self.Fenetre.destroy()
        print("bouton cancel presse, arret du programme")
        import sys
        sys.exit()

    def on_select(event, listbox):
        selected_indices = listbox.curselection()
        selected_options = [listbox.get(index) for index in selected_indices]

    def run(self):
        self.mainwindow.mainloop()



# app = Fenetre_simple()
# app.run()
# texte_input = app.selected_options
# print(texte_input)