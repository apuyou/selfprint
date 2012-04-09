# -*- coding: utf-8 -*-

import httplib, urllib
import json

types = {"p": "Partiel 1", "q": "Partiel 2", "m": "Médian", "f": "Final", "t": "Test 1", "u": "Test 2", "v": "Test 2"}
semestres = {"A":"Automne", "P":"Printemps"}

RACINE = "/polar-web/"
HOST = "localhost"

#TODO : Vérification d'erreur

def get_something(args):
    conn = httplib.HTTPConnection(HOST)
    conn.request("GET", RACINE+"annales/borne?"+args)
    print RACINE+"annales/bornes?"+args

    try:
        resultat = conn.getresponse().read()
        return json.loads(resultat)
    except (ValueError):
        print "ERREUR : impossible de décoder l'objet json renvoyé"
        return [] # ça évalue à false donc ça passe même pour get_login_valide()

    # si il y pas de réseau ça plante monstrueusement
    # mais il a pas l'air de renvoyer une exception rattrapable

def update_liste_uvs():
    return get_something("liste-annales")

def get_details(uv):
    return get_something("details-annale="+uv)

def get_login_valide(login):
    return get_something("verif-login="+login)

def envoyer_commande(login, liste_uvs):
    conn = httplib.HTTPConnection(HOST)
    params = {'login': login}

    i = 0
    for uv in liste_uvs:
        params["uv"+str(i)] = uv
        i += 1

    params_encoded = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request("POST", RACINE+"annales/borne?commander", params_encoded, headers)
    return conn.getresponse().read()
