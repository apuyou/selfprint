# -*- coding: utf-8 -*-

import httplib, urllib
import json

types = {"p": "Partiel 1", "q": "Partiel 2", "m": "Médian", "f": "Final", "t": "Test 1", "u": "Test 2", "v": "Test 2"}
semestres = {"A":"Automne", "P":"Printemps"}

RACINE = "/polar-web/"
HOST = "localhost"

#TODO : Vérification d'erreur

def update_liste_uvs():
    conn = httplib.HTTPConnection("localhost")
    conn.request("GET", RACINE+"annales/borne?liste-annales")
    print RACINE+"annales/comm_borne?liste-annales"
    return json.loads(conn.getresponse().read())

def get_details(uv):
    conn = httplib.HTTPConnection(HOST)
    conn.request("GET", RACINE+"annales/borne?details-annale="+uv)
    return json.loads(conn.getresponse().read())

def get_login_valide(login):
    conn = httplib.HTTPConnection(HOST)
    conn.request("GET", RACINE+"annales/borne?verif-login="+login)
    return conn.getresponse().read() == "OUI" #on pourrait le faire avec du json aussi

def envoyer_commande(login, liste_uvs):
    conn = httplib.HTTPConnection(HOST)
    params = {'login': login}

    i = 0
    for uv in liste_uvs:
        params["uv"+str(i)] = uv
        i += 1

    params_encoded = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request("POST", RACINE+"annales/comm_borne?commander", params_encoded, headers)
    return conn.getresponse().read()
