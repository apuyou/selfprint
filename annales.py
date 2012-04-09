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

import borne as data

COMMANDES_MAX = 8

# ===================================
# Côté gauche de l'UI : Panier et validation de la commande

class ElementPanier(BoxLayout):
    uv = Property("UV inconnue")
    prix = Property(0)

    def __init__(self, **kwargs):
        super(ElementPanier, self).__init__(**kwargs)

        self.register_event_type("on_remove")

        if kwargs.has_key("uv"):
            self.uv = kwargs["uv"]

        if kwargs.has_key("pages"):
            self.prix = kwargs["pages"]

    def suppr_pressed(self):
        self.dispatch("on_remove")

    def on_remove(self):
        pass

class Panier(StackLayout):
    commandes = []
    prix = Property(0)

    def __init__(self, **kwargs):
        super(Panier, self).__init__(**kwargs)

        self.register_event_type("on_valider_commande")

    def add_commande(self, uv, nb_pages):
        if (len(self.commandes)) < COMMANDES_MAX:
            w = ElementPanier(uv=uv, pages=nb_pages)
            w.bind(on_remove=self.remove_commande)
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
            self.dispatch("on_valider_commande")

    def reset(self):
        for i in self.commandes:
            self.remove_widget(i)
        self.commandes = []
        self.prix = 0

    def remove_commande(self, widget):
        print len(self.commandes)
        self.prix -= widget.prix
        self.remove_widget(widget)
        self.commandes.remove(widget)
        print len(self.commandes)

    def on_valider_commande(self):
        pass

# ===================================
# Côté droit de l'UI: recherche d'UV

class RechercheUV(StackLayout):
    nb_uvs = 0
    nb_uvs_affichees = 0

    def __init__(self, **kwargs):
        super(RechercheUV, self).__init__(**kwargs)

        self.register_event_type("on_row_selected")

        self.uvs = data.update_liste_uvs()

    def reset(self):
        self.txt_input.text = ""

    def on_text_change(self, valeur):
        self.fill_tree(valeur)

    def fill_tree(self, filtre):
        self.scroll.clear_widgets()

        tree = TreeView(hide_root=True, size_hint_y=None)
        tree.bind(minimum_height=tree.setter('height'),
                  selected_node=self.show_details)
        self.scroll.add_widget(tree)

        self.nb_uvs_affichees = 0

        for uv in self.uvs:
            if uv[0].startswith(filtre.upper()) and uv[1] != 0:
                tree.add_node(TreeViewLabel(text=u"%s   (%s €)" % (uv[0],
                                                                   uv[1]*0.06),
                                            font_size=20, size_hint_y=None,
                                            padding=(20,20)))
                self.nb_uvs_affichees += 1

    def show_details(self, instance, value):
        self.dispatch("on_row_selected", value.text[0:4])

    def on_row_selected(self, uv):
        pass

# ===================================
# Popup pour afficher le détail d'une UV et ajouter au panier

class DetailsContent(StackLayout):

    def __init__(self, **kwargs):
        StackLayout.__init__(self)
        self.parent_ = kwargs["papa_popup"]

        self.tree.bind(minimum_height=self.tree.setter('height'))

    def commander_pressed(self):
        self.parent_.dismiss()
        self.parent_.dispatch("on_commander", self.uv)

    def fill_treeview(self, uv):
        self.uv = uv

        liste = data.get_details(uv)

        p_node = TreeViewLabel(text="")
        for sujet in liste:
            if (data.types[sujet[0]] != p_node.text): # On crée un nouveau noeud quand on change de type de sujet
                p_node = TreeViewLabel(text=data.types[sujet[0]],
                                       font_size=20, is_open=True,
                                       no_selection=True)
                self.tree.add_node(p_node)

            titre_sujet = data.semestres[sujet[1]] + " \
" +str(2000+sujet[2]) + " " + ["", "+ Corrigé"][sujet[3]]
            self.tree.add_node(TreeViewLabel(text=titre_sujet,
                                             size_hint_y=None,
                                             font_size=15,
                                             no_selection=True),
                               p_node)

class Details(Popup):
    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)

        self.register_event_type("on_commander")

        self.content = DetailsContent(papa_popup=self)

        uv = kwargs["uv"]
        self.title = u"Détail des annales de "+uv

        self.content.fill_treeview(uv)

    def on_commander(self, uv):
        pass

# ===================================
# Popup pour entrer le login et valider la commande

class LoginContent(StackLayout):
    """On ne peut pas modifier un popup directement
    depuis les fichiers kv donc faut modifier le contenu"""

    correct_login = False
    nb_commande = Property("")

    def __init__(self, **kwargs):
        StackLayout.__init__(self)
        self.parent_ = kwargs["papa_popup"]

    def commande_ok(self, nb_commande):
        self.nb_commande = nb_commande
        self.txt.text = "Commande validée! Vous pouvez noter votre numéro de commande"
        self.buttonsbox.remove_widget(self.bouton_commander)

    def commander_pressed(self):
        if self.login_correct:
            self.parent_.dispatch("on_envoyer", self.login.text)

    def on_text_change(self):
        valeur = self.login.text
        if (len(valeur) > 5): #parceque y a des chinois qu'ont des login super courts
            #on envoie un message à comm_borne pour vérifer le login
            if (data.get_login_valide(valeur)):
                self.txt.text = "Login valide !"
                self.login_correct = True
            else:
                self.txt.text = ""
                self.login_correct = False

class LoginPopup(Popup):

    def __init__(self, **kwargs):
        super(LoginPopup, self).__init__(**kwargs)

        self.register_event_type("on_envoyer")

	self.title = "Validation de la commande"

        self.content = LoginContent(papa_popup=self)

    def commande_ok(self, nb_commande):
        self.content.commande_ok(nb_commande)
        Clock.schedule_once(self.dismiss, 15)

    def on_envoyer(self, login):
        pass

# ===================================
# Application

def find_nb_pages(liste, uv):
    for i in liste:
        if i[0] == uv:
            return i[1]

class AnnalesApp(App):

    def on_row_selected(self, widget, uv):
        details = Details(uv=uv, attach_to=self.root)
        details.bind(on_commander=self.add_commande)
        details.open()

    def add_commande(self, widget, uv):
        self.panier.add_commande(uv, find_nb_pages(self.recherche.uvs,
                                                   uv))
        self.recherche.reset()

    def valider_commande(self, widget):
        ask_login = LoginPopup(attach_to=self.root)
        ask_login.bind(on_envoyer=self.envoyer)
        ask_login.open()

    def envoyer(self, widget, login):
        num_commande = data.envoyer_commande(login, self.panier.get_commandes())
        widget.commande_ok(num_commande)
        self.panier.reset()
        self.recherche.reset()

    def build(self):
        self.root = FloatLayout()

        bigbox = BoxLayout(orientation="horizontal", padding=20, spacing=20)
        self.root.add_widget(bigbox)

        self.panier = Panier()
        self.panier.bind(on_valider_commande=self.valider_commande)
        bigbox.add_widget(self.panier)

        self.recherche = RechercheUV()
        self.recherche.bind(on_row_selected=self.on_row_selected)
        bigbox.add_widget(self.recherche)

        #Clock.schedule_once(lambda a: self.root.get_parent_window().toggle_fullscreen())
        return self.root

if __name__ == "__main__":
    AnnalesApp().run()
