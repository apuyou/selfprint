# -*- coding: utf-8 -*-

import httplib, urllib
import json

uvs = {}
types = {"p": "Partiel 1", "q": "Partiel 2", "m": "Médian", "f": "Final", "t": "Test 1", "u": "Test 2", "v": "Test 2"}
semestres = {"A":"Automne", "P":"Printemps"}

RACINE = "/polar-web/"

def update_liste_uvs():
    conn = httplib.HTTPConnection("localhost")
    conn.request("GET", RACINE+"annales/comm_borne?liste-annales")
    return json.loads(conn.getresponse().read())

def get_details(uv):
    #if uvs.has_key(uv):
    conn = httplib.HTTPConnection("localhost")
    conn.request("GET", RACINE+"annales/comm_borne?details-annale="+uv)
    return json.loads(conn.getresponse().read())
    #else:
    #    return []

def get_login_valide(login):
    conn = httplib.HTTPConnection("localhost")
    conn.request("GET", RACINE+"annales/comm_borne?verif-login="+login)
    return conn.getresponse().read() == "OUI" #on pourrait le faire avec du json aussi

def envoyer_commande(login, liste_uvs):
    print login, liste_uvs
    conn = httplib.HTTPConnection("localhost")
    params = {'login': login}

    i = 0
    for uv in liste_uvs:
        params["uv"+str(i)] = uv
        i += 1

    params_encoded = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    conn.request("POST", RACINE+"annales/comm_borne?commander", params_encoded, headers)
    return conn.getresponse().read()

if __name__ == "__main__":
    uvs = update_liste_uvs()
    print "Annales disponibles"
    for uv in uvs:
        print uv[0], " ("+str(uv[1])+" pages)"

    while 1:
        choix_uv = raw_input("\nAfficher les détails d'une annales : ")

        if choix_uv == "quit": quit()

        sujets = get_details(choix_uv);
        if sujets:
            print "\nSujets disponibles pour", choix_uv, "\n"
            prec = ""
            for sujet in sujets:
                if sujet[0] != prec:
                    print "\n====", types[sujet[0]], "===="
                    prec = sujet[0]
                print semestres[sujet[1]], 2000+sujet[2], ["", "+ Corrigé"][sujet[3]]
        else:
            print "Pas de sujets pour cette UV"
