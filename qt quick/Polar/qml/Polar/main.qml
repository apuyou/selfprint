// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1
import "Client.js" as Data
import QtWebKit 1.0

Rectangle {
    id: page
    width: 1366
    height: 768
    color: "#090909"
    clip: true

    function loadUvDetail(UV, nbpages) {
        detailsDialog.uv = UV;
        detailsDialog.nbPagesUV = nbpages;
        modelSujets.clear();
        Data.getDetails(UV, function(result) {
                        result.forEach(function(sujet) {
                                           modelSujets.append({type: Data.types[sujet[0]], semestre: Data.semestres[sujet[1]], annee: sujet[2], corrige: sujet[3]});
                                       });
                    });
    }

    FocusScope {
        id: blurFocusScope
        x: 0
        y: 0
        width: parent.width
        height: parent.height
        focus: true
        z: 1

        Rectangle {
            id: blur
            color: "#e1000000"
            visible: false
            anchors.fill: parent
            property bool modal: false
            z: 0.5

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (!blur.modal)
                        page.state = ""
                }
            }

            Dialog {
                id: detailsDialog
                property string uv: ""
                property int nbPagesUV: 0
                titre: "Détail de l'annale " + uv

                ListView {
                    id: listeSujets
                    boundsBehavior: Flickable.DragOverBounds
                    clip: true
                    anchors.bottom: buttonCancel.top
                    anchors.bottomMargin: 10
                    anchors.top: parent.top
                    anchors.topMargin: parent.tailleTitre + 10
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    contentWidth: width

                    section.property: "type"
                    section.criteria: ViewSection.FullString
                    section.delegate: Rectangle {
                        width: parent.width
                        height: 40
                        color: "#444444"
                        Text {
                            width: parent.width
                            height: parent.height
                            color: "#ffffff"
                            text: section
                            font.bold: true
                            verticalAlignment: Text.AlignVCenter
                            font.pointSize: 28
                        }
                    }

                    delegate: Text {
                        width: parent.width
                        height: 40
                        color: "#ffffff"
                        text: semestre + " " + (2000+annee).toString() + (corrige ? " avec corrigé" : "")
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 20
                    }
                    model: ListModel {
                        id: modelSujets
                    }
                }

                Button {
                    id: buttonCancel
                    text: "Retour"
                    textSize: 30
                    width: parent.width/2 - 20
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    state: "cancel"
                    onClicked: page.state = ""
                }

                Button {
                    id: buttonAdd
                    text: "Ajouter au panier"
                    anchors.left: buttonCancel.right
                    anchors.leftMargin: 10
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    state: "ok"
                    onClicked: {
                        page.state = "";
                        filtre.reset();
                        if (modelPanier.count < 8) {
                            modelPanier.append({name: detailsDialog.uv, nbPages: detailsDialog.nbPagesUV});
                        }
                    }
                }
            }

            Dialog {
                id: sendDialog
                titre: "Finalisation de la commande"

                Text {
                    id: explication
                    color: "#ffffff"
                    text: qsTr("Entrez votre login, validez puis aller payer à la caisse muni de votre numéro de commande")
                    anchors.rightMargin: 10
                    anchors.topMargin: parent.tailleTitre + 10
                    anchors.top: parent.top
                    anchors.right: parent.right
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    wrapMode: Text.WordWrap
                    font.pixelSize: 20
                }

                FilterInput {
                    id: entryLogin
                    color: "#3c3c3c"
                    defaultText: qsTr("")
                    anchors.top: explication.bottom
                    anchors.topMargin: 20
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                }

                Text {
                    id: numText
                    color: "#ffffff"
                    text: qsTr("Numéro de commande")
                    horizontalAlignment: Text.AlignHCenter
                    anchors.top: explication.bottom
                    anchors.topMargin: 20
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    font.pixelSize: 30
                }

                Text {
                    id: numCommande
                    color: "#ffffff"
                    text: qsTr("12345")
                    verticalAlignment: Text.AlignVCenter
                    anchors.bottom: buttonCancel2.top
                    anchors.bottomMargin: 10
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    anchors.top: numText.bottom
                    anchors.topMargin: 0
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    font.pixelSize: 120
                }

                Button {
                    id: buttonCancel2
                    text: "Retour"
                    textSize: 30
                    anchors.right: parent.right
                    anchors.rightMargin: parent.width/2 - 20
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    state: "cancel"
                    onClicked: page.state = ""
                }

                Button {
                    id: buttonFinal
                    text: "Valider la commande"
                    anchors.left: buttonCancel2.right
                    anchors.leftMargin: 10
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    state: Data.validerLogin(entryLogin.filter) ? "ok" : "insensitive"
                    onClicked: {
                        var liste = [];
                        for (var i = 0; i<modelPanier.count; i++) {
                            liste.push(modelPanier.get(i).name);
                        }
                        Data.envoyerCommande(entryLogin.filter, liste, function (num) {
                                                 filtre.reset();
                                                 page.state = "sent";
                                                 entryLogin.reset();
                                                 numCommande.text = num.toString();
                                                 modelPanier.clear();
                                             });
                    }
                }
            }

            Dialog {
                id: connectDialog
                titre: "Connection au système de paiement"

                WebView {
                    id: webview1
                    url: "https://cas.utc.fr/cas/login?service=https://assos.utc.fr/polar/caisse/payutc"
                    preferredHeight: parent.height - anchors.bottomMargin - anchors.topMargin - parent.tailleTitre
                    preferredWidth: parent.width - anchors.leftMargin - anchors.rightMargin
                    anchors.top: parent.top
                    anchors.topMargin: parent.tailleTitre + 10
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    clip: true
                }
            }
        }
}
        FocusScope {
            id: mainFocusScope
            x: 0
            y: 0
            width: parent.width
            height: parent.height
            focus: true

        Flow {
            id: bigBox
            x: 20
            y: 0
            width: parent.width - 2*x
            height: parent.height - 10
            spacing: 10
            flow: Flow.TopToBottom

            Text {
                id: moduleTitre
                x: 138
                y: -160
                color: "#d7d7d7"
                text: qsTr("Le Polar - Commande d'annales")
                font.bold: true
                font.pixelSize: 40
            }

            Flow {
                id: paned
                x: 200
                y: 0
                width: parent.width
                height: parent.height - parent.spacing - moduleTitre.height
                spacing: 10

                Column {
                    id: liste
                    x: 184
                    y: -46
                    width: (parent.width - parent.spacing)/2
                    height: parent.height
                    spacing: 10
                    transformOrigin: Item.Center

                    Text {
                        id: titreUVs
                        color: "#ffffff"
                        text: qsTr("UVs disponibles")
                        anchors.top: parent.top
                        anchors.topMargin: 0
                        anchors.left: parent.left
                        anchors.leftMargin: 0
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        verticalAlignment: Text.AlignTop
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 23
                    }

                    ListView {
                        id: listeUVs
                        contentWidth: parent.width
                        anchors.bottomMargin: filtre.height + parent.spacing
                        anchors.topMargin: titreUVs.height + parent.spacing
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.leftMargin: 0
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        clip: true
                        contentHeight: 166
                        boundsBehavior: Flickable.StopAtBounds
                        model: filteredUVs
                        Component.onCompleted: {
                            Data.getUVS(function(result) {
                                            result.forEach(function(UV) {
                                                               modelUVs.addUV(UV[0], UV[1]);
                                                           });
                                        });
                            Data.loadLogins(function(result) {});
                            //page.state = "connection";
                        }

                        section.property: "name"
                        section.criteria: ViewSection.FirstCharacter
                        section.delegate: Rectangle {
                            width: parent.width
                            height: 40
                            color: "#444444"
                            Text {
                                width: parent.width
                                height: parent.height
                                color: "#ffffff"
                                text: section
                                font.bold: true
                                verticalAlignment: Text.AlignVCenter
                                font.pointSize: 28
                            }
                        }

                        delegate: Item {
                            id: item1
                            width: parent.width
                            height: 50
                            Row {
                                id: row1
                                height: 40
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 0

                                Rectangle {
                                    id: rectangle1
                                    color: "#c6c0c0"
                                    z: -1
                                }

                                Text {
                                    id: nomUV
                                    color: "#ffffff"
                                    text: name
                                    anchors.left: parent.left
                                    anchors.leftMargin: 0
                                    font.pointSize: 30
                                    anchors.verticalCenter: parent.verticalCenter
                                    font.bold: true
                                }

                                Text {
                                    id: text1
                                    y: 6
                                    color: "#ffffff"
                                    text: Data.priceStr(nbPages)
                                    anchors.left: parent.left
                                    anchors.leftMargin: 200
                                    font.bold: false
                                    font.pixelSize: 20
                                }

                            }

                            MouseArea {
                                id: mouse_area1
                                x: 363
                                y: 5
                                anchors.fill: parent
                                onClicked: function() {
                                               loadUvDetail(name, nbPages);
                                               page.state = "detailsUV";
                                           } ()
                            }
                        }

                    }

                FilterInput {
                    id: filtre
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    defaultText: qsTr("Recherche...")
                    validator: RegExpValidator { regExp: /[A-z]{2}\d\d/ }
                    onFilterChanged: {
                        filteredUVs.setFilterFixedString(filter.toUpperCase());
                    }
                }
}
                Flow {
                    id: panier
                    x: 444
                    y: -48
                    width: (parent.width - parent.spacing)/2
                    height: parent.height
                    spacing: 10

                    function removeElement(UV) {
                        for (var i = 0; i<modelPanier.count; i++) {
                            if (modelPanier.get(i).name === UV) {
                                modelPanier.remove(i);
                                return;
                            }
                        }
                    }

                    Text {
                        id: titrePanier
                        y: -60
                        color: "#ffffff"
                        text: qsTr("Panier")
                        anchors.left: parent.left
                        anchors.leftMargin: 0
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 23
                    }

                    ListView {
                        id: panierView
                        x: 193
                        y: 117
                        width: parent.width
                        height: parent.height - 2*parent.spacing - titrePanier.height - commandeBox.height
                        orientation: ListView.Vertical
                        spacing: 10
                        cacheBuffer: 0
                        snapMode: ListView.SnapToItem
                        contentWidth: parent.width
                        boundsBehavior: Flickable.StopAtBounds
                        clip: true
                        delegate: Item {
                            id: item3
                            x: 5
                            width: parent.width
                            height: 53
                            Row {
                                id: row2
                                anchors.left: parent.left
                                anchors.leftMargin: 0
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 10

                                Text {
                                    color: "#ffffff"
                                    text: name
                                    anchors.left: parent.left
                                    anchors.leftMargin: 0
                                    font.pointSize: 30
                                    anchors.verticalCenter: parent.verticalCenter
                                    font.bold: true
                                }

                                Button {
                                    text: "Enlever"
                                    anchors.right: parent.right
                                    anchors.rightMargin: 15
                                    anchors.verticalCenter: parent.verticalCenter
                                    textSize: 20
                                    state: "cancel"
                                    onClicked: { panier.removeElement(name); }
                                }
                            }
                        }
                        model: ListModel {
                            id: modelPanier
                        }
                    }

                    Flow {
                        id: commandeBox
                        x: 14
                        y: 649
                        width: parent.width
                        height: 50

                        Text {
                            id: text2
                            x: -5
                            y: 17
                            height: parent.height
                            color: "#ffffff"
                            text: qsTr("Total : ")
                            anchors.verticalCenter: parent.verticalCenter
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            font.pixelSize: 30
                        }

                        Text {
                            id: text4
                            x: 12
                            y: 27
                            color: "#fbfbfb"
                            text: {
                                var total = 0;
                                for (var i = 0; i<modelPanier.count; i++) {
                                        total += modelPanier.get(i).nbPages;
                                }
                                return Data.priceStr(total);
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            font.pixelSize: 30
                        }

                        Button {
                            text: qsTr("Valider la commande")
                            clip: false
                            anchors.top: parent.top
                            anchors.topMargin: 0
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            anchors.right: parent.right
                            anchors.rightMargin: 0
                            textSize: 30
                            state: "ok"
                            onClicked: {
                                if(modelPanier.count > 0)
                                    page.state = "send";
                            }
                        }

                    }
                }

            }
        }

    }
    states: [
        State {
            name: "detailsUV"

            PropertyChanges {
                target: blur
                visible: true
                modal: false
            }

            PropertyChanges {
                target: detailsDialog
                visible: true
                z: 1
            }
        },
        State {
            name: "send"

            PropertyChanges {
                target: blur
                visible: true
                modal: false
            }

            PropertyChanges {
                target: sendDialog
                visible: true
                z: 1
            }

            PropertyChanges {
                target: blurFocusScope
                focus: true
            }

            PropertyChanges {
                target: mainFocusScope
                focus: false
            }

            PropertyChanges {
                target: numCommande
                visible: false
            }

            PropertyChanges {
                target: numText
                visible: false
            }
        },
        State {
            name: "sent"

            PropertyChanges {
                target: blur
                visible: true
                modal: false
            }

            PropertyChanges {
                target: sendDialog
                visible: true
                z: 1
            }

            PropertyChanges {
                target: entryLogin
                visible: false
            }

            PropertyChanges {
                target: numCommande
                visible: true
            }

            PropertyChanges {
                target: numText
                visible: true
            }

            PropertyChanges {
                target: buttonFinal
                visible: false
            }

            PropertyChanges {
                target: buttonCancel2
                anchors.rightMargin: 10
            }
        },
        State {
            name: "connection"

            PropertyChanges {
                target: blur
                visible: true
                modal: true
            }

            PropertyChanges {
                target: connectDialog
                visible: true
                z: 1
            }

            PropertyChanges {
                target: webview1
                clip: false
            }

            PropertyChanges {
                target: flipable1
                clip: true
            }
        }
    ]

    /* C'est joli mais ça marche pas sur la borne
    transitions: [
        Transition {
            from: ""; to: "detailsUV"
            ParallelAnimation {
                PropertyAction { target: blur; property: "visible"; value: true }
                PropertyAction { target: detailsDialog; property: "visible"; value: true }
                NumberAnimation { properties: "y"; duration: 200; easing.type: Easing.OutCubic }
                ColorAnimation { duration: 200 }
            }
        },
        Transition {
            from: "detailsUV"; to: ""
            SequentialAnimation {
                ParallelAnimation {
                    NumberAnimation { properties: "y"; duration: 200; easing.type: Easing.OutCubic }
                    ColorAnimation { duration: 200 }
                }
                PropertyAction { target: blur; property: "visible"; value: false }
                PropertyAction { target: detailsDialog; property: "visible"; value: false }
            }
        }
    ]
    */
}
