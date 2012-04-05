# -*- coding: utf-8 -*-

import httplib
import json

uvs = {}
types = {"p": "Partiel 1", "q": "Partiel 2", "m": "Médian", "f": "Final", "t": "Test 1", "u": "Test 2", "v": "Test 2"}
semestres = {"A":"Automne", "P":"Printemps"}

def update_liste_uvs():
    conn = httplib.HTTPConnection("localhost")
    conn.request("GET", "/polar-web/annales/comm_borne?liste-annales")
    return json.loads(conn.getresponse().read())

def get_details(uv):
    if uvs.has_key(uv):
        conn = httplib.HTTPConnection("localhost")
        conn.request("GET", "/polar-web/annales/comm_borne?details-annale="+uv)
        return json.loads(conn.getresponse().read())
    else:
        return []

if __name__ == "__main__":
    uvs = update_liste_uvs()
    print "Annales disponibles"
    for key in uvs:
        print key, " ("+str(uvs[key])+" pages)"

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
