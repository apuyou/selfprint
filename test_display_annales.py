# -*- coding: utf-8 -*-

import kivy
kivy.require("1.2.0")

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import Property

import test_data_annales as data

COMMANDES_MAX = 8

class Messager():
    def __init__(self, kwargs):
        if (kwargs.has_key("message_handler")):
            self.send = kwargs["message_handler"]
        else:
            print "No message handler passed"

class ElementPanier(BoxLayout, Messager):
    uv = Property("UV inconnue")
    prix = Property(0)

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self)
        Messager.__init__(self, kwargs)

        if kwargs.has_key("uv"):
            self.uv = kwargs["uv"]

        if kwargs.has_key("pages"):
            self.prix = kwargs["pages"]

    def suppr_pressed(self):
        self.send(self)

class Panier(StackLayout, Messager):
    commandes = []
    prix = Property(0)

    def __init__(self, **kwargs):
        StackLayout.__init__(self)
        Messager.__init__(self, kwargs)

    def add_commande(self, uv, nb_pages):
        if (len(self.commandes)) < COMMANDES_MAX:
            w = ElementPanier(uv=uv, pages=nb_pages, message_handler=self.message_handler)
            self.add_widget(w)
            self.commandes.append(w)
            self.prix += nb_pages

    def get_commandes(self):
        toi = []
        for i in self.commandes:
            toi.append(i.uv)

        return toi

    def valider_commande(self):
        if len(self.commandes) > 0:
            self.send("valider_commande", None)

    def reset(self):
        for i in self.commandes:
            self.remove_widget(i)
        self.commandes = []
        self.prix = 0

    def message_handler(self, widget):
        print len(self.commandes)
        self.prix -= widget.prix
        self.remove_widget(widget)
        self.commandes.remove(widget)
        print len(self.commandes)

class RechercheUV(StackLayout, Messager):
    nb_uvs = 0
    nb_uvs_affichees = 0

    def __init__(self, **kwargs):
        StackLayout.__init__(self)
        Messager.__init__(self, kwargs)

        self.orientation = "lr-tb"
        self.spacing = 10

    def remplir(self):
        self.scroll = ScrollView(size_hint=(None, None), size=(600, 650), do_scroll_x=False)
        self.add_widget(self.scroll)

        txt_input = TextInput(multiline=False, focus=True, font_size=20, height=40)
        txt_input.bind(text=self.on_text_change)
        self.add_widget(txt_input)

        self.txt_input = txt_input
        self.uvs = data.update_liste_uvs()
        self.fill_tree("") # pas de filtre, on affiche tout

    def reset(self):
        self.txt_input.text = ""

    def on_text_change(self, widget, value):
        self.fill_tree(value)

    def fill_tree(self, filtre):
        self.scroll.clear_widgets()

        tree = TreeView(hide_root=True, size_hint_y=None)
        tree.bind(minimum_height=tree.setter('height'), selected_node=self.show_details)
        self.scroll.add_widget(tree)

        self.nb_uvs_affichees = 0

        for uv in self.uvs:
            if uv[0].startswith(filtre.upper()) and uv[1] != 0:
                tree.add_node(TreeViewLabel(text=u"%s         (%s €)" % (uv[0], uv[1]*0.06), font_size=20, size_hint_y=None, padding=(20,20)))
                self.nb_uvs_affichees += 1

    def show_details(self, instance, value):
        self.send("details", value.text[0:4])

class Details(Popup, Messager):
    def __init__(self, **kwargs):
        Popup.__init__(self)
        Messager.__init__(self, kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.size = (900, 700)

    def remplir(self, uv):
        self.title = u"Détail des annales de "+uv
        self.content = StackLayout(size_hint=(1, 1), spacing = 15, padding = 15)

        scroll = ScrollView(size_hint=(None,None), do_scroll_x=False, size=(850, 485))
        self.content.add_widget(scroll)
        self.tree = TreeView(hide_root=True, size_hint_y=None)
        self.tree.bind(minimum_height=self.tree.setter('height'))
        scroll.add_widget(self.tree)
        self.fill_treeview(uv)

        box = BoxLayout(orientation="horizontal", spacing = 15)
        self.content.add_widget(box)
        commander = Button(text=u"Ajouter à la commande", background_color=[0,181/255.,38/255.,1], font_size=25)
        box.add_widget(commander)

        def commander_pressed(a):
            self.dismiss()
            self.send("commander", uv)
        commander.bind(on_release=commander_pressed)

        close = Button(text=u"Retour", background_color=[220/255.,12/255.,12/255.,1], font_size=25)
        box.add_widget(close)
        close.bind(on_release=self.dismiss)

    def fill_treeview(self, uv):
        liste = data.get_details(uv)
        print liste

        p_node = TreeViewLabel(text="")
        for sujet in liste:
            if (data.types[sujet[0]] != p_node.text):
                p_node = TreeViewLabel(text=data.types[sujet[0]], font_size=20, is_open=True, no_selection=True)
                self.tree.add_node(p_node)
            titre_sujet = data.semestres[sujet[1]] + " " + str(2000+sujet[2]) + " " + ["", "+ Corrigé"][sujet[3]]
            self.tree.add_node(TreeViewLabel(text=titre_sujet, size_hint_y=None, font_size=15, no_selection=True), p_node)
            print titre_sujet

def find_nb_pages(liste, uv):
    for i in liste:
        if i[0] == uv:
            return i[1]

class Login(Popup, Messager):
    correct_login = False

    def __init__(self, **kwargs):
        Popup.__init__(self)
        Messager.__init__(self, kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.size = (900, 700)

    def remplir(self):
        self.title = u"Finalisation de la commande"
        self.content = StackLayout(size_hint=(1, 1), spacing = 15, padding = 15)

        txt_input = TextInput(multiline=False, focus=True, font_size=20, height=40)
        txt_input.bind(text=self.on_text_change)
        self.content.add_widget(txt_input)
        self.login = txt_input

        self.txt = Label(text="", font_size = 20)
        self.content.add_widget(self.txt)

        self.void = Label(text=" ", font_size=150) # s'pas joli ça!
        self.content.add_widget(self.void)
        void = Label(text=" ", font_size=150) # s'pas joli ça!
        self.content.add_widget(void)
        void = Label(text=" ", font_size=150) # s'pas joli ça!
        self.content.add_widget(void)

        box = BoxLayout(orientation="horizontal", spacing = 15)
        self.content.add_widget(box)
        commander = Button(text=u"Valider et Envoyer", background_color=[0,181/255.,38/255.,1], font_size=25)
        box.add_widget(commander)
        commander.bind(on_release=self.commander_pressed)
        self.bouton_commander = commander
        self.box = box

        close = Button(text=u"Retour", background_color=[220/255.,12/255.,12/255.,1], font_size=25)
        box.add_widget(close)
        close.bind(on_release=self.dismiss)

    def commander_pressed(self, a):
        if self.login_correct:
            self.send("envoyer", self.login.text)

    def on_text_change(self, a, valeur):
        if (len(valeur) > 5): #parceque y a des chinois qu'on des login super courts
            #on envoie un message à comm_borne pour vérifer le login
            if (data.get_login_valide(valeur)):
                self.txt.text = "Login valide !"
                self.login_correct = True
            else:
                self.txt.text = ""
                self.login_correct = False

class AnnalesApp(App):
    def reception_message(self, type_, valeur):
        if (type_ == "details"):
            details = Details(message_handler=self.reception_message, attach_to=self.root)
            details.remplir(valeur)
            details.open()
        elif (type_ == "commander"):
            self.panier.add_commande(valeur, find_nb_pages(self.recherche.uvs, valeur))
            self.recherche.reset()
        elif (type_ == "valider_commande"):
            self.ask_login = Login(message_handler=self.reception_message, attach_to=self.root)
            self.ask_login.remplir()
            self.ask_login.open()
        elif (type_ =="envoyer"):
            num_commande = data.envoyer_commande(valeur, self.panier.get_commandes())
            self.ask_login.txt.text = "Commande validée! Vous pouvez noter votre numéro de commande"
            self.ask_login.void.text = num_commande
            self.ask_login.box.remove_widget(self.ask_login.bouton_commander)
            self.panier.reset()
            self.recherche.reset()

    def build(self):
        self.root = FloatLayout()
        bigbox = BoxLayout(orientation="horizontal", padding=20, spacing=20)
        self.panier = Panier(message_handler=self.reception_message)
        bigbox.add_widget(self.panier)
        self.recherche = RechercheUV(message_handler=self.reception_message)
        self.recherche.remplir()
        bigbox.add_widget(self.recherche)

        self.root.add_widget(bigbox)

        #Clock.schedule_once(lambda a: self.root.get_parent_window().toggle_fullscreen())
        return self.root

if __name__ == "__main__":
    AnnalesApp().run()
