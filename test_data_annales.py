# -*- coding: utf-8 -*-

import borne

if __name__ == "__main__":
    uvs = borne.update_liste_uvs()
    print "Annales disponibles"
    for uv in uvs:
        print uv[0], " ("+str(uv[1])+" pages)"

    while 1:
        choix_uv = raw_input("\nAfficher les détails d'une annales : ")

        if choix_uv == "quit": quit()

        sujets = borne.get_details(choix_uv);
        if sujets:
            print "\nSujets disponibles pour", choix_uv, "\n"
            prec = ""
            for sujet in sujets:
                if sujet[0] != prec:
                    print "\n====", borne.types[sujet[0]], "===="
                    prec = sujet[0]
                print borne.semestres[sujet[1]], 2000+sujet[2], ["", "+ Corrigé"][sujet[3]]
        else:
            print "Pas de sujets pour cette UV"
