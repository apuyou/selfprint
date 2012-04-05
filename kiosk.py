#coding: utf-8

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import os, time

# chemin dans lequel les clés sont montées (/media en général)
path_to_watch = "media"

class PolarKiosque(FloatLayout):
	pass

class PreviewScreen(FloatLayout):
	def on_release_choix(self, instance, value):
		value._do_press()
		print 'iam'

class TreeViewLabelPath(TreeViewLabel):
	def __init__(self, path, **kwargs):
		super(TreeViewLabel, self).__init__(**kwargs)
		self.path = path


class PolarKiosqueApp(App):
	def on_select_node(self, instance, value):
		# ensure that any keybaord is released
		self.content.get_parent_window().release_keyboard()

		self.content.clear_widgets()
		try:
			w = getattr(self, 'show_%s' %
						value.text.lower().replace(' ', '_'))()
			self.content.add_widget(w)
		except Exception, e:
			print e

	def check_key(self, gloup):
		files = dict ([(f, None) for f in os.listdir (path_to_watch)])
		if len(files) > 0:
			self.content.clear_widgets()
			w = Label(text='Lecture de la clé')
			self.content.add_widget(w)
			Clock.schedule_once(self.show_key, .5/10) # VIRER LE /10
			return False
	
	def show_key(self, gloup):
		tree = TreeView(size_hint=(1, 1), hide_root=True,
				indent_level=20)

		def getReadableSize(size):
			units = ['o', 'Ko', 'Mo', 'Go']
			unit = 0
			while size > 1024 and unit < 3:
				size = size / 1024.0
				unit = unit + 1
			return "%.2f %s" % (size, units[unit])
				

		tree.bind(selected_node=self.show_file)
		
		self.content.clear_widgets()
		self.content.add_widget(tree)
		dirNodes = dict()
		
		# la racine
		dirNodes[path_to_watch] = tree.add_node(TreeViewLabel(
			text="Ordinateur", is_open=True, no_selection=True))
		
		for root, dirs, files in os.walk(path_to_watch):
			for diritem in dirs:
				fulldiritem = os.path.join(root, diritem)
				dirNodes[fulldiritem] = tree.add_node(TreeViewLabel(
					text=diritem, is_open=False, no_selection=True), dirNodes[root])
			for fileitem in files:
				(a, ext) = os.path.splitext(fileitem)
				if fileitem[0] !='.':
					label = "%s (%s)" % (fileitem, getReadableSize(os.path.getsize(os.path.join(root, fileitem)))) #FIXME Aligner à droite
					if ext == '.pdf':
						tree.add_node(TreeViewLabelPath(os.path.join(root, fileitem), text=label), dirNodes[root])
					else:
						tree.add_node(TreeViewLabel(text=label, no_selection=True), dirNodes[root]) # FIXME Faire du gris	
	
	def show_file(self, instance, value):
		ps = PreviewScreen()
		ps.path.text = 'Lecture de %s' % (value.path)
		
		self.content.clear_widgets()
		self.content.add_widget(ps)
	
	def build(self):
		root = BoxLayout(orientation='horizontal', padding=20, spacing=20)
		self.content = content = BoxLayout()
		root.add_widget(content)
		sc = PolarKiosque()
		sc.content.add_widget(root)
		

		self.content.clear_widgets()
		w = BoxLayout(spacing=10)
		w.add_widget(Label(text="Attente clé"))

		self.content.add_widget(w)
		
		Clock.schedule_interval(self.check_key, 1)
				
		return sc

	def show_standard_buttons(self):
		col = BoxLayout(spacing=10)
		col.add_widget(Button(text='Hello world'))
		col.add_widget(Button(text='Hello world', state='down'))
		return col

	def show_options_buttons(self):
		col = BoxLayout(spacing=10)
		col.add_widget(ToggleButton(text='Option 1', group='t1'))
		col.add_widget(ToggleButton(text='Option 2', group='t1'))
		col.add_widget(ToggleButton(text='Option 3', group='t1'))
		return col

	def show_horizontal_sliders(self):
		col = BoxLayout(orientation='vertical', spacing=10)
		col.add_widget(Slider())
		col.add_widget(Slider(value=50))
		return col

	def show_popup(self):
		btnclose = Button(text='Close this popup', size_hint_y=None, height=50)
		content = BoxLayout(orientation='vertical')
		content.add_widget(Label(text='Hello world'))
		content.add_widget(btnclose)
		popup = Popup(content=content, title='Modal popup example',
					  size_hint=(None, None), size=(300, 300),
					  auto_dismiss=False)
		btnclose.bind(on_release=popup.dismiss)
		button = Button(text='Open popup', size_hint=(None, None),
						size=(150, 70))
		button.bind(on_release=popup.open)
		popup.open()
		col = AnchorLayout()
		col.add_widget(button)
		return col



if __name__ in ('__main__', '__android__'):
	PolarKiosqueApp().run()

# 0 accueil
# 1 affichage fichiers et choix pdf
# 2 ouverture pdf, zoom, navigation, choix type
# 3 lancement
# 4 ejection
# afficher en bas Commencer > Choix du fichier > Impression > Fin
# tout le long : accueil, bouton ejection